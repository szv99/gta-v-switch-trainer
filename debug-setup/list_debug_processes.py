"""Query the Atmosphere GDB stub without attaching or suspending a process."""
import socket
import sys
from pathlib import Path

def packet(sock, command):
    data = command.encode('ascii')
    sock.sendall(b'$' + data + b'#' + f'{sum(data) & 255:02x}'.encode())
    return receive(sock)

def receive(sock):
    while True:
        first = sock.recv(1)
        if not first:
            raise EOFError('Debugger closed connection')
        if first == b'-':
            raise RuntimeError('Packet rejected')
        if first == b'$':
            break
    wire = bytearray()
    while True:
        char = sock.recv(1)
        if not char:
            raise EOFError('Incomplete packet')
        if char == b'#':
            break
        wire.extend(char)
    checksum = b''
    while len(checksum) < 2:
        chunk = sock.recv(2 - len(checksum))
        if not chunk:
            raise EOFError('Incomplete checksum')
        checksum += chunk
    if sum(wire) & 255 != int(checksum, 16):
        sock.sendall(b'-')
        raise RuntimeError('Checksum mismatch')
    sock.sendall(b'+')
    decoded = bytearray()
    i = 0
    while i < len(wire):
        value = wire[i]
        if value == 0x7d:
            i += 1
            decoded.append(wire[i] ^ 0x20)
        elif value == 0x2a:
            i += 1
            decoded.extend(bytes([decoded[-1]]) * (wire[i] - 29))
        else:
            decoded.append(value)
        i += 1
    return bytes(decoded)

def main():
    host = sys.argv[1] if len(sys.argv) > 1 else '192.168.0.122'
    with socket.create_connection((host, 22225), 5) as sock:
        sock.settimeout(8)
        print('Features:', packet(sock, 'qSupported:multiprocess+').decode())
        contents = bytearray()
        for _ in range(256):
            response = packet(sock, f'qXfer:osdata:read:processes:{len(contents):x},800')
            if not response or response[:1] not in (b'm', b'l'):
                raise RuntimeError(f'Process query failed: {response!r}')
            contents.extend(response[1:])
            if response[:1] == b'l':
                break
        else:
            raise RuntimeError('Process listing exceeded size limit')
        print(contents.decode('utf-8', errors='replace'))
        Path(__file__).with_name('debug-processes.xml').write_bytes(contents)

if __name__ == '__main__':
    main()
