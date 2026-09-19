"""Temporary, backed-up in-memory HUD probe; restore after 15 seconds."""
import socket,struct,json,time,datetime,argparse
from pathlib import Path
from list_debug_processes import packet

root=Path(__file__).parent
base=0xe7d605000
pid=0x8e
thread=0x73e755dfa0
program=0x3aa7e78000
parser=argparse.ArgumentParser()
parser.add_argument('--mode',choices=['probe','trainer'],default='probe')
parser.add_argument('--duration',type=int,default=15)
args=parser.parse_args()
assert 1<=args.duration<=120
folder=root.parent/('probe-out' if args.mode=='probe' else 'live-out')
payload=(folder/'trainer-2699.nsc').read_bytes()
native_map=json.loads((folder/'native-map.json').read_text())
handlers=json.loads((root/'native-registrations.json').read_text())
u32=lambda b,o:struct.unpack_from('<I',b,o)[0]
u64=lambda b,o:struct.unpack_from('<Q',b,o)[0]
ptr=lambda o:u64(payload,o)&0xffffff
code=payload[ptr(ptr(16)):ptr(ptr(16))+u32(payload,28)]
strings=payload[ptr(ptr(104)):ptr(ptr(104))+u32(payload,112)]
statics=payload[ptr(48):ptr(48)+u32(payload,36)*8]
assert len(code)<16384 and len(strings)<16384 and u32(payload,36)<=95
backup=[]
changes=[]
def connect():
    s=socket.create_connection(('192.168.0.122',22225),5);s.settimeout(8)
    packet(s,'qSupported:multiprocess+');packet(s,'!')
    if not packet(s,f'vAttach;{pid:x}').startswith(b'T'):
        s.close();raise RuntimeError('Attach failed')
    return s
def read(s,a,n):
    r=packet(s,f'm{a:x},{n:x}')
    if r.startswith(b'E'):raise RuntimeError((hex(a),r))
    data=bytes.fromhex(r.decode());assert len(data)==n
    return data
def write(s,a,data):
    assert packet(s,f'M{a:x},{len(data):x}:'+data.hex())==b'OK'
    assert read(s,a,len(data))==data
def detach(s):
    try: print('Detach',packet(s,f'D;{pid:x}'),flush=True)
    finally:s.close()
stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
backup_path=root/f'live-{args.mode}-backup-{stamp}.json'
s=connect()
applied=False
try:
    info=packet(s,'qRcmd,'+b'get info'.hex())
    assert b'0100b00b51230000' in bytes.fromhex(info.decode())
    header=read(s,program,128)
    context=read(s,thread,0x120)
    assert u32(header,88)==0xafd9916d and u32(header,24)==0x94c75b53
    assert context[0xd4:].startswith(b'cheat_controller\0') and u32(context,8)==53
    assert u32(context,16)==1, 'Wait for sleeping controller'
    stack=u64(context,0xb0)
    assert u32(context,24)>=95 and u32(context,28)>=95
    codepage=u64(read(s,u64(header,16),8),0)
    stringpage=u64(read(s,u64(header,104),8),0)
    native_table=u64(header,64)
    assert u32(header,28)>=len(code) and u32(header,112)>=len(strings)
    assert u32(header,44)>=len(native_map)
    native_data=b''.join(struct.pack('<Q',base+handlers[n['build2699']]) for n in native_map)
    original_nso=(root.parents[1]/'trainer-research/main-uncompressed.nso').read_bytes()
    for n in native_map:
        offset=handlers[n['build2699']]
        assert read(s,base+offset,8)==original_nso[offset+256:offset+264],n['name']
    # Preserve the complete stack region the small probe can touch.
    backup.append((stack,read(s,stack,0x800)))
    changes=[(codepage,code),(stringpage,strings),(native_table,native_data),
             (program+28,struct.pack('<I',len(code))),
             (program+44,struct.pack('<I',len(native_map))),
             (program+112,struct.pack('<I',len(strings))),
             (thread+16,struct.pack('<IIII',0,0,95,95))]
    if statics:changes.insert(0,(stack,statics))
    for a,data in changes:backup.append((a,read(s,a,len(data))))
    backup_path.write_text(json.dumps({'pid':pid,'thread':thread,'program':program,'base':base,'regions':[{'address':a,'data':b.hex()} for a,b in backup]},indent=2))
    applied=True
    for a,data in changes:write(s,a,data)
    print(args.mode,'installed in RAM; original bytes saved to',backup_path,flush=True)
except Exception:
    if applied:
        for a,data in reversed(backup):write(s,a,data)
    raise
finally:detach(s)
time.sleep(args.duration)
s=connect()
try:
    context=read(s,thread,0x30)
    print('Probe thread state/IP/FP/SP:',struct.unpack_from('<IIII',context,16),flush=True)
    assert u32(context,8)==53 and u32(context,12)==0xafd9916d
    for a,data in [(codepage,code),(stringpage,strings),(native_table,native_data)]:
        assert read(s,a,len(data))==data,'Unexpected change; inspect before restore'
    for a,data in reversed(backup):write(s,a,data)
    print('All original bytes restored and verified',flush=True)
finally:detach(s)
