"""Read-only snapshot of verified network-state fields; no fake sign-in flags."""
import sys,json,datetime
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from trainer import locked
from nxtrainer.transport import Remote
from nxtrainer.runtime import Profile,identity,applications,require,U32,U64,atomic_json

with locked():
    remote=Remote('192.168.0.122')
    try:
        pids=list(applications(remote));require(len(pids)==1,'Expected GTA application')
        with remote.attached(pids[0]):
            base=identity(remote);profile=Profile();profile.verify(remote,base)
            for offset,length in [(0x10a1fcc,0x50),(0x10a3ce0,0x3c),(0x1d97d88,0x5c)]:
                require(remote.read(base+offset,length)==profile.code[offset:offset+length],'Network code differs')
            guard=U32(remote.read(base+0x308cee0,4))
            flags=remote.read(base+0x3d7b7cc,1)[0]
            access_gate=remote.read(base+0x38b0f88,1)[0]
            in_progress=remote.read(base+0x3abd444,1)[0]
            session_pointer=U64(remote.read(base+0x3a71618,8))
            active_value=U32(remote.read(session_pointer+0x82fc,4)) if session_pointer else 0
            signed_in=guard==0 and bool(flags&2)
            signed_online=guard==0 and bool(flags&4)
            inferred_reason=3 if access_gate&1 else 6 if not signed_in else 7 if not signed_online else None
            report=dict(timestamp=datetime.datetime.now().isoformat(),pid=pids[0],base=hex(base),
                        guard=guard,raw_signin_flags=flags,access_gate=access_gate,
                        signed_in=signed_in,signed_online=signed_online,
                        network_game_in_progress=bool(in_progress),network_session_active=bool(active_value),
                        inferred_access_reason=inferred_reason,
                        note='Read fields and verified handler code. Access reason inferred; native was not invoked.')
            atomic_json(Path(__file__).with_name('online-runtime.json'),report)
            print(json.dumps(report,indent=2))
    finally:remote.close()
