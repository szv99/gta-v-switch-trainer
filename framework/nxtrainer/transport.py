"""Small synchronous GDB RSP transport. Every attachment must be detached."""
import socket
from contextlib import contextmanager

class ProtocolError(RuntimeError):
    pass

class Remote:
    def __init__(self, host, port=22225):
        self.sock = socket.create_connection((host, port), 5)
        self.sock.settimeout(8)
        self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.buffer = bytearray()
        self.pid = None
        try:
            self.features = self.command('qSupported:multiprocess+')
            self.expect('!', b'OK')
        except BaseException:
            self.sock.close()
            raise

    def byte(self):
        if not self.buffer:
            data = self.sock.recv(8192)
            if not data:
                raise EOFError('Debugger disconnected')
            self.buffer.extend(data)
        value = self.buffer[0]
        del self.buffer[0]
        return value

    def receive(self):
        while True:
            value = self.byte()
            if value == ord('$'):
                break
            if value == ord('-'):
                raise ProtocolError('Debugger rejected packet')
        wire = bytearray()
        while True:
            value = self.byte()
            if value == ord('#'):
                break
            wire.append(value)
            if len(wire) > 0x100000:
                raise ProtocolError('Oversized packet')
        check = bytes([self.byte(), self.byte()])
        if (sum(wire) & 255) != int(check, 16):
            self.sock.sendall(b'-')
            raise ProtocolError('Checksum mismatch')
        self.sock.sendall(b'+')
        output = bytearray()
        i = 0
        while i < len(wire):
            value = wire[i]
            if value in (ord('}'), ord('*')):
                i += 1
                if i >= len(wire):
                    raise ProtocolError('Truncated escape')
                if value == ord('}'):
                    output.append(wire[i] ^ 0x20)
                else:
                    if not output or wire[i] < 29:
                        raise ProtocolError('Invalid run length')
                    output.extend(bytes([output[-1]]) * (wire[i] - 29))
            else:
                output.append(value)
            i += 1
        return bytes(output)

    def command(self, command):
        data = command.encode('ascii')
        self.sock.sendall(b'$' + data + b'#' + f'{sum(data)&255:02x}'.encode())
        return self.receive()

    def expect(self, command, expected):
        response = self.command(command)
        if response != expected:
            raise ProtocolError(f'{command.split(":")[0]}: {response!r}')

    def xfer(self, obj, annex=''):
        output = bytearray()
        for _ in range(512):
            response = self.command(f'qXfer:{obj}:read:{annex}:{len(output):x},1800')
            if response[:1] not in (b'l', b'm'):
                raise ProtocolError(f'{obj}: {response!r}')
            output.extend(response[1:])
            if response[:1] == b'l':
                return bytes(output)
        raise ProtocolError('Transfer limit exceeded')

    def monitor(self, text):
        response = self.command('qRcmd,' + text.encode().hex())
        output = bytearray()
        for _ in range(512):
            if response == b'OK':
                return bytes(output).decode()
            if response.startswith(b'O'):
                output.extend(bytes.fromhex(response[1:].decode()))
                response = self.receive()
            else:
                if response.startswith(b'E'):
                    raise ProtocolError(f'Monitor: {response!r}')
                return bytes.fromhex(response.decode()).decode()
        raise ProtocolError('Monitor limit exceeded')

    @contextmanager
    def attached(self, pid):
        if self.pid is not None:
            raise ProtocolError('Already attached')
        self.pid = pid
        try:
            response = self.command(f'vAttach;{pid:x}')
            if response[:1] not in (b'T', b'S'):
                raise ProtocolError(f'Attach: {response!r}')
            yield self
        finally:
            try:
                self.expect(f'D;{pid:x}', b'OK')
            finally:
                self.pid = None

    def read(self, address, size):
        if not 0 <= size <= 0x100000:
            raise ValueError('Invalid read size')
        output = bytearray()
        while len(output) < size:
            count = min(0x1000, size-len(output))
            response = self.command(f'm{address+len(output):x},{count:x}')
            if response.startswith(b'E'):
                raise ProtocolError(f'Read {address:#x}: {response!r}')
            data = bytes.fromhex(response.decode())
            if len(data) != count:
                raise ProtocolError('Short memory read')
            output.extend(data)
        return bytes(output)

    def write(self, address, data):
        for offset in range(0, len(data), 0x1000):
            chunk = data[offset:offset+0x1000]
            self.expect(f'M{address+offset:x},{len(chunk):x}:' + chunk.hex(), b'OK')
        if self.read(address, len(data)) != data:
            raise ProtocolError('Memory write verification failed')

    def close(self):
        self.sock.close()
