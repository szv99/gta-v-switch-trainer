import socket,struct,json,datetime
from pathlib import Path
from list_debug_processes import packet
root=Path(__file__).parent
result=[]
with socket.create_connection(('192.168.0.122',22225),5) as s:
    s.settimeout(8)
    packet(s,'qSupported:multiprocess+'); packet(s,'!')
    try:
        response=packet(s,'vAttach;8e')
        if not response.startswith(b'T'):raise RuntimeError(response)
        def read(address,size):
            response=packet(s,f'm{address:x},{size:x}')
            if response.startswith(b'E'):raise RuntimeError(response)
            data=bytes.fromhex(response.decode())
            assert len(data)==size
            return data
        base=0xe7d605000
        # Validate the exact native which exposes the script thread array.
        raw=(root.parents[1]/'trainer-research'/'main-uncompressed.nso').read_bytes()
        assert read(base+0x1148110,0x68)==raw[0x1148210:0x1148278]
        pointer,count,capacity=struct.unpack('<QHH',read(base+0x3dd61e8,12))
        assert 0<count<=capacity<=4096,(pointer,count,capacity)
        print('Script table',hex(pointer),'count',count,'capacity',capacity,flush=True)
        table=read(pointer,count*8)
        for index in range(count):
            address=struct.unpack_from('<Q',table,index*8)[0]
            if not address:continue
            data=read(address,0x120)
            ident,hashvalue,state,ip=struct.unpack_from('<IIII',data,8)
            if not ident:continue
            name=data[0xd4:0x114].split(b'\0')[0].decode('ascii',errors='replace')
            row=dict(index=index,address=hex(address),id=ident,hash=hex(hashvalue),state=state,ip=hex(ip),name=name,raw=data.hex())
            result.append(row)
            print({k:v for k,v in row.items() if k!='raw'},flush=True)
    finally:
        print('Detach',packet(s,'D;8e'),flush=True)
        stamp=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        (root/f'script-threads-{stamp}.json').write_text(json.dumps(result,indent=2))
