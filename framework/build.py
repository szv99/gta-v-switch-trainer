"""Compile, translate VM/native format, and publish a checked payload manifest."""
import hashlib,json,re,subprocess,sys,struct
from pathlib import Path
from nxtrainer.runtime import ROOT,DEV,Profile,atomic_json,require
sys.path.insert(0,str(DEV))
from vm_format import instructions,validate

def analyze_call_graph(code, static_count=95, native_slack=32):
    funcs = {}
    for i, op, n in instructions(code):
        if op == 45:
            params = code[i+1]
            frame = struct.unpack_from('<H', code, i+2)[0]
            name_len = code[i+4]
            name = code[i+5:i+5+name_len].decode('ascii', 'replace')
            funcs[i] = (name, frame, params)

    calls = {off: set() for off in funcs}
    curr_func = None
    for i, op, n in instructions(code):
        if op == 45:
            curr_func = i
        elif op == 93:
            target = int.from_bytes(code[i+1:i+4], 'little')
            if target in funcs and curr_func in calls:
                calls[curr_func].add(target)

    def max_path_frames(func_off, visited):
        if func_off in visited:
            raise RuntimeError(f'Recursion detected in script call graph at {func_off:#x}')
        visited.add(func_off)
        frame = funcs[func_off][1]
        children = calls.get(func_off, set())
        child_max = max((max_path_frames(c, visited.copy()) for c in children), default=0)
        return frame + child_max

    top_entries = [off for off in funcs if off not in {c for s in calls.values() for c in s}]
    if not top_entries:
        top_entries = list(funcs.keys())
    call_graph_peak = max((max_path_frames(e, set()) for e in top_entries), default=0)
    conservative_sum = sum(f[1] for f in funcs.values())
    return dict(
        conservative_frames=conservative_sum,
        conservative_stack_slots=static_count + conservative_sum + native_slack,
        call_graph_peak_frames=call_graph_peak,
        call_graph_stack_slots=static_count + call_graph_peak + native_slack
    )

def main():
    output=ROOT/'build'
    output.mkdir(exist_ok=True)
    compiler=DEV/'SC-CL-SampleProject-master/bin/SC-CL-local-PC.exe'
    source=ROOT/'script/trainer.c'
    subprocess.run([str(compiler),'-platform=PC','-target=GTAV','-no-rsc7','-emit-asm',
                    '-out-dir='+str(output)+'\\',str(source),'--','-I',
                    str(DEV/'SC-CL-SampleProject-master/include')],check=True)
    subprocess.run([sys.executable,str(DEV/'map2699.py'),'framework/build'],check=True)
    raw=(output/'trainer-2699.nsc').read_bytes()
    asm=(output/'trainer.ysa2').read_text()
    symbols={name:int(index) for index,name in re.findall(r'^SetStaticName (\d+) (\w+)$',asm,re.M)}
    required=['protocolMagic','protocolVersion','runtimeStatus','heartbeat','remoteCommand','remoteArg',
              'remoteSequence','acknowledgedSequence','lastResult','lastVehicle','spawnCount',
              'invincible','previousPed','pendingModel','menuOpen',
              'networkSignedIn','networkSignedOnline','networkCanAccess','networkAccessReason',
              'networkGameInProgress','networkSessionActive']
    require(all(name in symbols for name in required),'Compiler omitted a mailbox field')
    pointer=lambda offset:struct.unpack_from('<Q',raw,offset)[0]&0xffffff
    code_size=struct.unpack_from('<I',raw,28)[0]
    code=raw[pointer(pointer(16)):pointer(pointer(16))+code_size]
    validate(code)
    # Perform exact call graph stack analysis
    stack_stats = analyze_call_graph(code, static_count=95, native_slack=32)
    require(stack_stats['call_graph_stack_slots'] <= 256, 'Payload exceeds verified call-graph stack budget')
    profile=Profile()
    natives=json.loads((output/'native-map.json').read_text())
    require(all(n['build2699'] in profile.handlers for n in natives),'Unmapped native')
    manifest=dict(version='0.1.0',protocol=1,sha256=hashlib.sha256(raw).hexdigest(),
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                  executable_sha256=profile.fingerprint,expected_build_id=profile.build,
                  symbols=symbols,code_bytes=code_size,natives=len(natives),
                  conservative_stack_slots=stack_stats['conservative_stack_slots'],
                  call_graph_stack_slots=stack_stats['call_graph_stack_slots'])
    atomic_json(output/'manifest.json',manifest)
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':main()
