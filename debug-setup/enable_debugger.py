from ftplib import FTP
from pathlib import Path
from io import BytesIO
import re
import hashlib

root = Path(__file__).parent
remote = '/atmosphere/config/system_settings.ini'
backup = '/atmosphere/config/system_settings.before-gtav-debug.ini'
temp = remote + '.gtav-debug.tmp'
f = FTP()
f.connect('192.168.0.122', 5000, timeout=20)
f.login()
def read(path):
    out = BytesIO()
    f.retrbinary('RETR ' + path, out.write)
    return out.getvalue()
try:
    original = read(remote)
    (root / 'system_settings.before-debug-current.ini').write_bytes(original)
    text = original.decode('utf-8-sig')
    newline = '\r\n' if '\r\n' in text else '\n'
    lines = text.splitlines()
    start = next(i for i, line in enumerate(lines) if line.strip() == '[atmosphere]')
    end = next((i for i in range(start+1, len(lines)) if lines[i].strip().startswith('[')), len(lines))
    section = [line for line in lines[start+1:end] if not re.match(r'^\s*(enable_htc|enable_standalone_gdbstub)\s*=', line)]
    section += ['; GTA live diagnostics', 'enable_htc = u8!0x0', 'enable_standalone_gdbstub = u8!0x1']
    updated = (newline.join(lines[:start+1] + section + lines[end:]) + newline).encode('utf-8')
    (root / 'system_settings.debug.ini').write_bytes(updated)
    names = [p.rsplit('/', 1)[-1] for p in f.nlst('/atmosphere/config')]
    if backup.rsplit('/', 1)[-1] not in names:
        f.storbinary('STOR ' + backup, BytesIO(original))
        assert read(backup) == original, 'Backup mismatch'
    f.storbinary('STOR ' + temp, BytesIO(updated))
    assert read(temp) == updated, 'Staged settings mismatch'
    swap = remote + '.before-debug-swap'
    if swap.rsplit('/', 1)[-1] in names:
        raise RuntimeError('Previous swap exists; inspect before continuing')
    f.rename(remote, swap)
    try:
        f.rename(temp, remote)
    except Exception:
        f.rename(swap, remote)
        raise
    assert read(remote) == updated, 'Live settings mismatch'
    f.voidcmd('TYPE I')
    size = f.size('/atmosphere/contents/0100b00b51230000/romfs/update/update2.rpf')
    print('Debugger settings uploaded and read-back verified. SHA256:', hashlib.sha256(updated).hexdigest())
    print('Current update2.rpf bytes:', size)
    print('Settings backup:', backup)
finally:
    f.close()
