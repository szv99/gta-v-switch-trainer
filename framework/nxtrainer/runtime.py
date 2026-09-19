"""Version-specific discovery, payload planning, and journalled RAM changes."""
import hashlib
import json
import os
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT.parent
TITLE = '0100b00b51230000'
HOST_HASH = 0xafd9916d
U32 = lambda b, o=0: struct.unpack_from('<I', b, o)[0]
U64 = lambda b, o=0: struct.unpack_from('<Q', b, o)[0]

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix+'.tmp')
    with temp.open('w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)
        file.flush()
        os.fsync(file.fileno())
    os.replace(temp, path)

class Profile:
    def __init__(self):
        raw = (DEV.parent/'trainer-research/main-uncompressed.nso').read_bytes()
        self.build = raw[0x40:0x60].hex()
        require(self.build.startswith('6e3e9b3af5746e74b615bd981080c9271bc226620'), 'Wrong local executable')
        fileoff, memoff, size = struct.unpack_from('<III', raw, 0x10)
        require(memoff == 0, 'Unsupported executable layout')
        self.code = raw[fileoff:fileoff+size]
        self.handlers = json.loads((DEV/'debug-setup/native-registrations.json').read_text())
        self.fingerprint = hashlib.sha256(raw).hexdigest()

    def verify(self, remote, base):
        for offset, count in ((0x1148110, 0x68), (0x26385c4, 0x58), (0x1147cd0, 0x70)):
            require(remote.read(base+offset, count) == self.code[offset:offset+count],
                    'Unsupported running build: executable fingerprint differs')

def applications(remote):
    tree = ET.fromstring(remote.xfer('osdata', 'processes'))
    for item in tree:
        columns = {x.attrib['name']:x.text for x in item}
        if columns.get('command') == 'Application':
            yield int(columns['pid'])

def identity(remote):
    text = remote.monitor('get info')
    require(re.search(r'Program Id:\s+0x0*'+TITLE.lstrip('0')+r'\b', text, re.I), 'Application is not GTA')
    libraries = ET.fromstring(remote.xfer('libraries'))
    matches = [int(x.find('segment').attrib['address'],16) for x in libraries
               if x.attrib.get('name') == 'game_nx_master.nss']
    require(len(matches) == 1, 'Missing or ambiguous GTA executable')
    return matches[0]

def find_host(remote, base):
    array, count, capacity = struct.unpack('<QHH', remote.read(base+0x3dd61e8,12))
    require(0<count<=capacity<=4096, 'Invalid script thread table')
    table = remote.read(array,count*8)
    addresses = sorted(set(U64(table,i*8) for i in range(count)) - {0})
    # Batch adjacent objects to avoid pausing the game for hundreds of round trips.
    groups = []
    for address in addresses:
        if not groups or address+0x120-groups[-1][0]>0x6000:
            groups.append([address,address+0x120, [address]])
        else:
            groups[-1][1]=address+0x120
            groups[-1][2].append(address)
    found=[]
    for start,end,members in groups:
        data=remote.read(start,end-start)
        for address in members:
            context=data[address-start:address-start+0x120]
            if U32(context,8) and U32(context,12)==HOST_HASH:
                require(context[0xd4:].startswith(b'cheat_controller\0'), 'Host name mismatch')
                found.append((address,context))
    require(len(found)==1, 'Expected one active cheat_controller; enter Story Mode first')
    thread,context=found[0]
    data=remote.read(base+0x397e100,0x90)
    nodes,buckets=struct.unpack_from('<QQ',data,0x68)
    buckets_count=U32(data,0x78)
    require(0<buckets_count<100000,'Invalid streaming hash table')
    index=struct.unpack('<i',remote.read(buckets+(HOST_HASH%buckets_count)*4,4))[0]
    visited=set()
    for _ in range(100):
        require(index>=0 and index not in visited,'Host script missing or hash chain corrupt')
        visited.add(index)
        hashed,slot,index=struct.unpack('<Iii',remote.read(nodes+index*12,12))
        if hashed==HOST_HASH:
            break
    else:
        raise RuntimeError('Hash lookup limit')
    stride=U32(data,0x44)
    require(0<=slot<100000 and stride==16,'Unsupported script pool layout')
    program=U64(remote.read(U64(data,0x30)+slot*stride,8))
    header=remote.read(program,128)
    require(U32(header,88)==HOST_HASH and U32(header,24)==0x94c75b53,'Wrong script program')
    return dict(thread=thread,thread_id=U32(context,8),program=program,
                stack=U64(context,0xb0)),context,header

class Payload:
    def __init__(self, directory):
        directory=Path(directory)
        self.meta=json.loads((directory/'manifest.json').read_text())
        self.raw=(directory/'trainer-2699.nsc').read_bytes()
        require(hashlib.sha256(self.raw).hexdigest()==self.meta['sha256'],'Payload checksum mismatch')
        pointer=lambda offset:U64(self.raw,offset)&0xffffff
        self.code=self.raw[pointer(pointer(16)):pointer(pointer(16))+U32(self.raw,28)]
        self.strings=self.raw[pointer(pointer(104)):pointer(pointer(104))+U32(self.raw,112)]
        self.statics=self.raw[pointer(48):pointer(48)+U32(self.raw,36)*8]
        self.natives=json.loads((directory/'native-map.json').read_text())
        require(len(self.code)==U32(self.raw,28)<16384 and len(self.strings)==U32(self.raw,112)<16384,'Payload must fit one code/string page')

def plan(remote, profile, base, host, context, header, payload):
    require(U32(context,16)==1,'Host script is not sleeping; retry shortly')
    static_count=U32(header,36)
    require(static_count==95 and len(payload.statics)<=static_count*8,'Static capacity mismatch')
    host_code_cap = U32(header,28)
    host_string_cap = U32(header,112)
    host_native_cap = U32(header,44)
    require(len(payload.code)<=host_code_cap, 'Payload code exceeds host capacity')
    require(U32(context,24)>=static_count and U32(context,28)*8<=0x800, 'Unsupported host stack state')
    native_data=bytearray()
    for native in payload.natives:
        offset=profile.handlers.get(native['build2699'])
        require(offset is not None,'Unknown native '+native['name'])
        require(remote.read(base+offset,8)==profile.code[offset:offset+8], 'Native mismatch '+native['name'])
        native_data.extend(struct.pack('<Q',base+offset))
    code_page=U64(remote.read(U64(header,16),8))
    string_page_ptr_addr = U64(header,104)
    string_page=U64(remote.read(string_page_ptr_addr,8))
    native_table_ptr_addr = host['program'] + 64
    orig_native_table = U64(header,64)

    # Journal a non-overlapping union. Context includes scheduler timers and flags.
    new_context=bytearray(context[8:0xb0])
    struct.pack_into('<IIII',new_context,8,0,0,static_count,static_count)
    stack=bytearray(remote.read(host['stack'],0x800))
    stack[:len(payload.statics)]=payload.statics

    specs=[('stack',host['stack'],bytes(stack),False),
           ('code',code_page,payload.code,True)]

    # Dual-mode hosting: In-Place Mode vs Decoupled Relocation Mode
    base_pool = (host_string_cap + 1) + (host_native_cap * 8) + (static_count * 8)
    extra_cap = 0
    needed = len(payload.strings) + len(native_data)
    if needed > base_pool:
        probe_len = (needed - base_pool + 255) & ~255
        probe_addr = string_page + base_pool
        probe_data = remote.read(probe_addr, probe_len)
        zero_count = 0
        for b in probe_data:
            if b != 0: break
            zero_count += 1
        if zero_count >= needed - base_pool:
            extra_cap = zero_count & ~15
    total_resource_pool = base_pool + extra_cap
    if len(payload.strings) <= host_string_cap and len(payload.natives) <= host_native_cap:
        # Mode 1: Legacy in-place fallback
        specs.extend([
            ('strings', string_page, payload.strings, True),
            ('natives', orig_native_table, bytes(native_data), True),
        ])
    else:
        # Mode 2: Decoupled relocated layout within the pooled resource buffer
        require(len(payload.strings) + len(native_data) <= total_resource_pool,
                f'Payload exceeds decoupled resource capacity ({total_resource_pool} B)')
        native_table_addr = string_page
        native_len_aligned = (len(native_data) + 15) & ~15
        string_target_addr = string_page + native_len_aligned
        specs.extend([
            ('native_ptr', native_table_ptr_addr, struct.pack('<Q', native_table_addr), True),
            ('string_page_ptr', string_page_ptr_addr, struct.pack('<Q', string_target_addr), True),
            ('natives', native_table_addr, bytes(native_data), True),
            ('strings', string_target_addr, payload.strings, True),
        ])

    specs.extend([
        ('code_size',host['program']+28,struct.pack('<I',len(payload.code)),True),
        ('native_count',host['program']+44,struct.pack('<I',len(payload.natives)),True),
        ('string_size',host['program']+112,struct.pack('<I',len(payload.strings)),True),
        ('context',host['thread']+8,bytes(new_context),False)
    ])
    return [dict(name=name,address=address,before=remote.read(address,len(after)).hex(),
                 after=after.hex(),immutable=immutable) for name,address,after,immutable in specs]

def restore_regions(remote, regions):
    # The process is suspended throughout; context is restored last.
    ordered=[r for r in regions if r['name']!='context']+[r for r in regions if r['name']=='context']
    for region in ordered:
        remote.write(region['address'],bytes.fromhex(region['before']))

def apply_transaction(remote, state, path):
    state['phase']='prepared'
    atomic_json(path,state)
    try:
        state['phase']='applying'
        atomic_json(path,state)
        for region in state['regions']:
            remote.write(region['address'],bytes.fromhex(region['after']))
        state['phase']='active'
        atomic_json(path,state)
    except BaseException:
        state['phase']='recovery_required'
        atomic_json(path,state)
        try:
            restore_regions(remote,state['regions'])
            state['phase']='restored'
            atomic_json(path,state)
        except BaseException:
            pass
        raise

def verify_session(remote, state, profile, immutable=True):
    base=identity(remote)
    require(base==state['base'],'Game restarted: old session addresses cannot be reused')
    profile.verify(remote,base)
    host=state['host']
    context=remote.read(host['thread'],0x120)
    require(U32(context,8)==host['thread_id'] and U32(context,12)==HOST_HASH
            and U64(context,0xb0)==host['stack'],'Host thread changed: refusing writes')
    require(U32(remote.read(host['program']+88,4))==HOST_HASH,'Host program changed')
    if immutable:
        for region in state['regions']:
            if region['immutable']:
                require(remote.read(region['address'],len(bytes.fromhex(region['after'])))==bytes.fromhex(region['after']),
                        'Session content changed: '+region['name'])
    return context

def telemetry(remote, state):
    symbols=state['symbols']
    count=max(symbols.values())+1
    data=remote.read(state['host']['stack'],count*8)
    values={name:U32(data,index*8) for name,index in symbols.items()}
    result=values['lastResult']
    values['lastResult']=result if result<0x80000000 else result-0x100000000
    if 'networkAccessReason' in values:
        reason=values['networkAccessReason']
        values['networkAccessReason']=reason if reason<0x80000000 else reason-0x100000000
    values['resultLabel']={0:'idle',1:'loading',2:'vehicle spawned',3:'healed',4:'wanted cleared',
                           5:'vehicle repaired',6:'invincibility changed',7:'stopped',8:'network status sampled',
                           9:'transitioning to freemode',10:'hosting online session',11:'hosting solo session',
                           12:'locating ground',13:'teleported',14:'vehicle cleaned',15:'vehicle uprighted',
                           16:'tuned',17:'vehicle deleted',18:'time updated',19:'weather applied',
                           20:'weather reset',21:'never wanted enabled',22:'never wanted disabled',
                           24:'clothes cleaned',25:'invisibility changed',26:'ragdoll changed',27:'suicide executed',
                           28:'vehicle godmode changed',29:'boosted',30:'doors toggled',31:'resprayed',32:'plate updated',
                           33:'weapons given',34:'ammo maxed',35:'infinite ammo changed',36:'never reload changed',
                           37:'parachute given',38:'weapons removed',39:'blackout changed',40:'speed updated',
                           41:'fast swim changed',42:'infinite stamina changed',43:'police ignore changed',
                           44:'thermal vision changed',45:'night vision changed',46:'tyres fixed',
                           47:'engine keep-alive changed',48:'tyres bulletproofed',49:'vehicle stopped',
                           50:'forward teleported',51:'explosive ammo changed',52:'fire ammo changed',
                           53:'explosive melee changed',54:'super damage changed',55:'heavy arsenal given',
                           56:'gravity changed',57:'peds cleared',58:'vehicles cleared',59:'cops cleared',
                           60:'neons toggled',61:'neon colour updated',62:'extra toggled',
                           63:'window tint applied',64:'wheel type changed',65:'custom respray applied',
                           66:'ped model changed',67:'outfit reset',68:'component varied',
                           69:'scenario started',70:'tasks cleared',
                           71:'object spawned',72:'object attached',73:'object freeze toggled',74:'object deleted',
                           75:'vehicle jumped',76:'drift mode changed',77:'rocket boost applied',
                           78:'air strike triggered',79:'seatbelt changed',80:'ragdoll triggered',
                           81:'bodyguard recruited',82:'bodyguard dismissed',83:'cash maxed',
                           84:'stunt ramp spawned',85:'rainbow paint toggled',86:'auto repair toggled',
                            87:'horn boost toggled',88:'vehicle weapons toggled',89:'teleport gun toggled',
                            90:'riot mode toggled',91:'flying car toggled',
                            92:'explosion gun toggled',93:'wanted level maxed',94:'vehicle invisibility toggled',
                            95:'vehicle 180 executed',96:'forcefield toggled',97:'bullet time toggled',
                            98:'sky launch executed',
                            99:'warped to nearest vehicle',100:'drunk mode toggled',
                            101:'autopilot toggled',102:'siren toggled',103:'vehicle self-destructed',
                           -1:'player unavailable',-2:'model unavailable',-3:'model timeout',
                           -4:'creation failed',-5:'not in a vehicle',-6:'request busy',
                           -9:'freemode transition failed',-10:'session host failed',-11:'solo host failed',
                           -12:'no waypoint',-13:'ground timeout',
                           -19:'maintransition start failed',-29:'maintransition load timeout',-39:'engine transition failed',
                           -49:'online prerequisites unavailable; transition not started'}.get(values['lastResult'],'unknown')
    require(values['protocolMagic']==0x4e585431 and values['protocolVersion']==1,'Mailbox ABI mismatch')
    return values

def send_command(remote,state,command,arg=0):
    values=telemetry(remote,state)
    require(values['remoteCommand']==0,'Previous command is still pending')
    require(values['runtimeStatus']==1,'Trainer is not ready for commands')
    stack=state['host']['stack']; symbols=state['symbols']
    sequence=(values['remoteSequence']+1)&0x7fffffff
    for key,value in [('remoteArg',arg),('remoteSequence',sequence),('remoteCommand',command)]:
        remote.write(stack+symbols[key]*8,struct.pack('<Q',value&0xffffffff))
    return sequence
