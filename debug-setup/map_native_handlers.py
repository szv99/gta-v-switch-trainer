from pathlib import Path
import struct, json, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

root=Path(__file__).parents[2]/'trainer-research'
raw=(root/'main-uncompressed.nso').read_bytes()
textoff,textva,textsize=struct.unpack_from('<III',raw,0x10)
code=raw[textoff:textoff+textsize]
md=Cs(CS_ARCH_ARM64,CS_MODE_ARM)
registrations={}
for off in range(0,len(code)-3,4):
    instruction=struct.unpack_from('<I',code,off)[0]
    if instruction>>26 != 0b100101:
        continue
    imm=instruction&0x3ffffff
    if imm&(1<<25): imm-=1<<26
    if textva+off+imm*4 != 0x2635d08:
        continue
    regs={}
    for ins in md.disasm(code[max(0,off-96):off],textva+max(0,off-96)):
        op=ins.op_str
        m=re.fullmatch(r'([xw][01]), #(-?0x[0-9a-f]+|-?\d+)(?:, lsl #(\d+))?',op)
        if m and ins.mnemonic in ('mov','movk','movz','adr','adrp'):
            reg=m[1][-1]; value=int(m[2],0); shift=int(m[3] or 0)
            if ins.mnemonic=='movk':
                if reg in regs: regs[reg]=(regs[reg]&~(0xffff<<shift))|(value<<shift)
            else: regs[reg]=value<<shift
        elif ins.mnemonic=='add':
            a=re.fullmatch(r'x([01]), x([01]), #(0x[0-9a-f]+|\d+)',op)
            if a and a[2] in regs: regs[a[1]]=regs[a[2]]+int(a[3],0)
        elif ins.mnemonic=='bl': regs={}
    if '0' in regs and '1' in regs:
        registrations[f'{regs["0"]&((1<<64)-1):016X}']=regs['1']
rows=[re.findall(r'0x[0-9A-Fa-f]+',l) for l in (root/'CrossMapping_Universal.h').read_text().splitlines()]
mapping={int(h,16):int(r[25],16) for r in rows if len(r)==28 for h in r if int(h,16)}
db=json.loads((root/'natives.json').read_text())
wanted=['SCRIPT','PLAYER_PED_ID','SET_ENTITY_INVINCIBLE','CREATE_VEHICLE','GET_GAME_TIMER']
report=[]
for group in db.values():
    for h,v in group.items():
        if not any(w in v['name'] for w in wanted):continue
        hashed=mapping.get(int(h,16),int(h,16))
        handler=registrations.get(f'{hashed:016X}')
        if handler is not None:report.append(dict(name=v['name'],hash=f'{hashed:016X}',handler=hex(handler)))
dest=Path(__file__).parent
(dest/'native-registrations.json').write_text(json.dumps(registrations,indent=2))
(dest/'script-native-handlers.json').write_text(json.dumps(report,indent=2))
print('Mapped',len(registrations),'handlers')
for r in report: print(r)
