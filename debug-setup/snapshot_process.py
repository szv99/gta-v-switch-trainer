"""Briefly attach, collect diagnostic metadata, then detach to resume."""
import socket
import sys
import datetime
import xml.etree.ElementTree as ET
from pathlib import Path
from list_debug_processes import packet, receive

pid = int(sys.argv[1])
log = []
def record(label, value):
    text = value.decode('utf-8', errors='replace') if isinstance(value, bytes) else str(value)
    log.append(label + '\n' + text)
    print(label, text, flush=True)

def transfer(sock, name):
    data = bytearray()
    for _ in range(128):
        response = packet(sock, f'qXfer:{name}:read::{len(data):x},1800')
        if response[:1] not in (b'm', b'l'):
            return response
        data.extend(response[1:])
        if response[:1] == b'l':
            return bytes(data)
    raise RuntimeError('Transfer too large')

with socket.create_connection(('192.168.0.122',22225), 5) as sock:
    sock.settimeout(10)
    attached = False
    try:
        record('Features', packet(sock, 'qSupported:multiprocess+'))
        record('Extended', packet(sock, '!'))
        attached = True
        response = packet(sock, f'vAttach;{pid:x}')
        record('Attach', response)
        if response[:1] not in (b'T', b'S'):
            raise RuntimeError('Attach failed')
        response = packet(sock, 'qRcmd,' + b'get info'.hex())
        output = bytearray()
        for _ in range(128):
            if response == b'OK' or response[:1] != b'O':
                break
            output.extend(bytes.fromhex(response[1:].decode()))
            response = receive(sock)
        if not output and response not in (b'OK', b'') and not response.startswith(b'E'):
            try:
                output = bytes.fromhex(response.decode())
            except ValueError:
                pass
        record('Process info', bytes(output))
        record('Monitor result', response)
        threads = transfer(sock, 'threads')
        record('Threads', threads)
        libraries = transfer(sock, 'libraries')
        record('Libraries', libraries)
        for thread in ET.fromstring(threads):
            name = thread.attrib.get('name', '')
            if name not in ('[RAGE] Main Application Thread', 'ResourcePlacementThread', '[RAGE] RenderThread'):
                continue
            record('Select ' + name, packet(sock, 'Hg' + thread.attrib['id']))
            regs = bytes.fromhex(packet(sock, 'g').decode())
            values = [int.from_bytes(regs[i:i+8], 'little') for i in range(0, 33*8, 8)]
            record(name + ' registers', {k:hex(values[n]) for k,n in [('FP',29),('LR',30),('SP',31),('PC',32)]})
            record(name + ' stack', packet(sock, f'm{values[31]:x},100'))
        if b'0100b00b51230000' in bytes(output):
            modules = ET.fromstring(libraries)
            base = next(int(m.find('segment').attrib['address'], 16) for m in modules if m.attrib['name'] == 'game_nx_master.nss')
            for label, offset, size in [('signin guard',0x308cee0,4),('signin flags',0x3d7b7cc,4),('game in progress',0x3abd444,1)]:
                record(label, packet(sock, f'm{base+offset:x},{size:x}'))
    finally:
        if attached:
            record('Detach', packet(sock, f'D;{pid:x}'))
        stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
        Path(__file__).with_name(f'snapshot-{pid}-{stamp}.txt').write_text('\n\n'.join(log), encoding='utf-8')
