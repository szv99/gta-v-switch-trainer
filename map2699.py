from pathlib import Path
import hashlib,json,re,struct
import sys
from vm_format import translate,validate
root=Path(__file__).parent
research=root.parent/'trainer-research'
rows=[list(map(lambda v:int(v,16),re.findall(r'0x[0-9A-Fa-f]+',line))) for line in (research/'CrossMapping_Universal.h').read_text().splitlines()]
rows=[r for r in rows if len(r)==28]
mapping={h:r[25] for r in rows for h in r if h and r[25]}
db=json.loads((research/'natives.json').read_text())
names={int(k,16):v['name'] for group in db.values() for k,v in group.items()}
folder=root/(sys.argv[1] if len(sys.argv)>1 else 'out')
d=bytearray((folder/'trainer.ysc').read_bytes())
u32=lambda off:struct.unpack_from('<I',d,off)[0]
ptr=lambda off:struct.unpack_from('<Q',d,off)[0]&0xffffff
size=u32(28);count=u32(44);base=ptr(64);mask=(1<<64)-1
assert base+count*8<=len(d)
report=[]
for i in range(count):
    r=(size+i)%64;encoded=struct.unpack_from('<Q',d,base+8*i)[0]
    old=((encoded<<r)|(encoded>>((64-r)%64)))&mask
    if old not in mapping:raise RuntimeError(f'Unmapped native {old:016X}')
    new=mapping[old]
    struct.pack_into('<Q',d,base+8*i,((new>>r)|(new<<((64-r)%64)))&mask)
    report.append(dict(name=names.get(old,'unknown'),original=f'{old:016X}',build2699=f'{new:016X}'))
for table,length in ((ptr(16),size),(ptr(104),u32(112))):
    for i in range((length+16383)//16384):
        off=ptr(table+8*i);assert off+min(16384,length-i*16384)<=len(d)
table=ptr(16)
code=b''.join(d[ptr(table+8*i):ptr(table+8*i)+min(16384,size-i*16384)] for i in range((size+16383)//16384))
converted=translate(code)
for i in range((size+16383)//16384):
    off=ptr(table+8*i);chunk=converted[i*16384:(i+1)*16384];d[off:off+len(chunk)]=chunk
print('Validated translated VM instructions:',validate(converted))
out=folder/'trainer-2699.nsc';out.write_bytes(d)
(folder/'native-map.json').write_text(json.dumps(report,indent=2))
print(f'Generated {out.name}: {len(d)} bytes, {size} code bytes, all {count} natives mapped to column 25')
print('SHA256 '+hashlib.sha256(d).hexdigest())
