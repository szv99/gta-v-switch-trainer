import socket,struct,json
from pathlib import Path
from list_debug_processes import packet
root=Path(__file__).parent
report={}
with socket.create_connection(('192.168.0.122',22225),5) as s:
    s.settimeout(8)
    packet(s,'qSupported:multiprocess+');packet(s,'!')
    try:
        assert packet(s,'vAttach;8e').startswith(b'T')
        def read(a,n):
            r=packet(s,f'm{a:x},{n:x}')
            if r.startswith(b'E'):raise RuntimeError((hex(a),r))
            return bytes.fromhex(r.decode())
        base=0xe7d605000
        data=read(base+0x397e100,0x90)
        report['streaming_global']=data.hex()
        nodes,buckets=struct.unpack_from('<QQ',data,0x68)
        nbuckets=struct.unpack_from('<I',data,0x78)[0]
        assert 0<nbuckets<100000
        pool,flags=struct.unpack_from('<QQ',data,0x30)
        stride=struct.unpack_from('<I',data,0x44)[0]
        for name,h in [('cheat_controller',0xafd9916d),('main_persistent',0x5700179c)]:
            index=struct.unpack('<i',read(buckets+(h%nbuckets)*4,4))[0]
            for _ in range(100):
                assert index>=0
                hashvalue,slot,nextindex=struct.unpack('<Iii',read(nodes+index*12,12))
                if hashvalue==h:break
                index=nextindex
            else:raise RuntimeError('Hash lookup exhausted')
            entry=pool+slot*stride
            chunk=read(entry,min(stride,256))
            row=dict(slot=slot,entry=hex(entry),stride=stride,data=chunk.hex())
            if len(chunk)>=8:
                pointer=struct.unpack_from('<Q',chunk)[0]
                if 0x800000000<=pointer<0x8000000000:
                    row['first_pointer']=hex(pointer)
                    row['pointed_data']=read(pointer,128).hex()
            report[name]=row
            print(name,row,flush=True)
        print('Factory pointer',read(base+0x308e398,8).hex(),flush=True)
    finally:
        print('Detach',packet(s,'D;8e'),flush=True)
        (root/'script-program-probe.json').write_text(json.dumps(report,indent=2))
