import struct
def instructions(code,old=False):
    i=0
    while i<len(code):
        raw=code[i];op=raw+3 if old and raw>=94 else raw
        if op>130:raise ValueError(f'Invalid opcode {raw:#x} at {i:#x}')
        n=1
        if op==37 or 52<=op<=62 or 64<=op<=66 or 104<=op<=107:n=2
        elif op==38 or op==46 or 67<=op<=92:n=3
        elif op==39 or op==44 or 93<=op<=100:n=4
        elif op in (40,41):n=5
        elif op==45:n=5+code[i+4]
        elif op==101:n=2+6*code[i+1]
        if i+n>len(code):raise ValueError('Truncated instruction')
        yield i,op,n
        i+=n

def translate(code):
    out=bytearray(code)
    for off,op,n in instructions(code,True):out[off]=op
    validate(out)
    return bytes(out)

def validate(code):
    ins=list(instructions(code));bounds={i for i,_,_ in ins};targets=[]
    for i,op,n in ins:
        if 85<=op<=92:targets.append(i+n+struct.unpack_from('<h',code,i+1)[0])
        elif op==93:
            target=int.from_bytes(code[i+1:i+4],'little');targets.append(target)
            if target>=len(code):raise ValueError('CALL outside code')
        elif op==101:
            for k in range(code[i+1]):
                off=i+2+k*6+4;targets.append(off+2+struct.unpack_from('<h',code,off)[0])
    if any(t not in bounds for t in targets):raise ValueError('Branch target not instruction boundary')
    return len(ins)

