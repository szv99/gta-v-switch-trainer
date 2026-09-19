import json,sys,tempfile,unittest
from unittest.mock import patch
from contextlib import contextmanager
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nxtrainer.runtime import apply_transaction,restore_regions,atomic_json,Payload
from nxtrainer.transport import Remote,ProtocolError
import trainer

class Memory:
    def __init__(self,fail=None):
        self.data=bytearray(b'original context')
        self.calls=0;self.fail=fail
    def write(self,address,data):
        self.calls+=1
        if self.calls==self.fail:
            self.data[address:address+1]=data[:1]
            raise OSError('Simulated partial transfer')
        self.data[address:address+len(data)]=data

class TransactionTests(unittest.TestCase):
    def state(self):
        return {'regions':[dict(name='code',address=0,before=b'original'.hex(),after=b'modified'.hex()),
                           dict(name='context',address=9,before=b'context'.hex(),after=b'changed'.hex())]}
    def test_success_and_restore(self):
        with tempfile.TemporaryDirectory() as folder:
            memory=Memory();state=self.state();path=Path(folder)/'active.json'
            apply_transaction(memory,state,path)
            self.assertEqual(json.loads(path.read_text())['phase'],'active')
            restore_regions(memory,state['regions'])
            self.assertEqual(memory.data,b'original context')
    def test_partial_write_is_rolled_back(self):
        for fail in (1,2):
            with self.subTest(fail=fail),tempfile.TemporaryDirectory() as folder:
                memory=Memory(fail);state=self.state();path=Path(folder)/'active.json'
                with self.assertRaises(OSError):apply_transaction(memory,state,path)
                self.assertEqual(memory.data,b'original context')
                self.assertEqual(json.loads(path.read_text())['phase'],'restored')
    def test_restore_failure_retains_recovery_journal(self):
        class Broken(Memory):
            def write(self,address,data):raise OSError('Disconnected')
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'active.json'
            with self.assertRaises(OSError):apply_transaction(Broken(),self.state(),path)
            self.assertEqual(json.loads(path.read_text())['phase'],'recovery_required')
            self.assertEqual(json.loads(path.read_text())['regions'],self.state()['regions'])
    def test_manifest_rejects_changed_payload(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)
            atomic_json(path/'manifest.json',{'sha256':'wrong'})
            (path/'trainer-2699.nsc').write_bytes(b'changed')
            with self.assertRaisesRegex(RuntimeError,'checksum'):Payload(path)

class Socket:
    def __init__(self,chunks):self.chunks=list(chunks);self.sent=[]
    def recv(self,n):return self.chunks.pop(0) if self.chunks else b''
    def sendall(self,data):self.sent.append(data)

class ProtocolTests(unittest.TestCase):
    def remote(self,wire):
        obj=object.__new__(Remote);obj.sock=Socket([bytes([x]) for x in wire]);obj.buffer=bytearray();return obj
    def test_fragmented_escaped_response(self):
        wire=b'A}'+bytes([ord('$')^32])+b'B'
        remote=self.remote(b'+$'+wire+b'#'+f'{sum(wire)&255:02x}'.encode())
        self.assertEqual(remote.receive(),b'A$B')
        self.assertEqual(remote.sock.sent,[b'+'])
    def test_bad_checksum(self):
        remote=self.remote(b'$OK#00')
        with self.assertRaisesRegex(ProtocolError,'Checksum'):remote.receive()
    def test_disconnect(self):
        remote=self.remote(b'$incomplete')
        with self.assertRaises(EOFError):remote.receive()

class LifecycleTests(unittest.TestCase):
    def test_cleanup_timeout_never_restores_memory(self):
        class Connection:
            @contextmanager
            def attached(self,pid):yield
        with patch.object(trainer,'verify_session'),patch.object(trainer,'telemetry',return_value={'runtimeStatus':1}),\
             patch.object(trainer,'send_command'),patch.object(trainer,'status',return_value={'runtimeStatus':1}),\
             patch.object(trainer.time,'sleep'),patch.object(trainer,'restore_regions') as restore:
            with self.assertRaisesRegex(RuntimeError,'Cleanup not acknowledged'):
                trainer.stop(Connection(),None,{'phase':'active','pid':1})
            restore.assert_not_called()
    def test_restart_rejects_old_addresses(self):
        from nxtrainer.runtime import verify_session
        with patch('nxtrainer.runtime.identity',return_value=0x9999):
            with self.assertRaisesRegex(RuntimeError,'restarted'):
                verify_session(None,{'base':0x1111},None)

class PlanDualModeTests(unittest.TestCase):
    def setUp(self):
        import struct
        self.base = 0x10000000
        self.host = {'thread': 0x73d5a22000, 'thread_id': 53, 'program': 0x3aa7e78000, 'stack': 0x73d61b6000}
        # Build valid context: state=1 (sleep), FP=95, SP=95
        ctx = bytearray(0x120)
        struct.pack_into('<IIIIII', ctx, 8, 53, 0xafd9916d, 1, 0x100, 95, 95)
        struct.pack_into('<Q', ctx, 0xb0, self.host['stack'])
        self.context = bytes(ctx)
        # Build valid header: magic=0x94c75b53, code_cap=15830, static_count=95, native_cap=151, string_cap=1551
        hdr = bytearray(128)
        struct.pack_into('<Q', hdr, 16, 0x3aa7e7bea0)  # code_pages ptr addr
        struct.pack_into('<II', hdr, 24, 0x94c75b53, 15830) # magic, code_size
        struct.pack_into('<I', hdr, 36, 95)             # static_count
        struct.pack_into('<I', hdr, 44, 151)            # native_count
        struct.pack_into('<Q', hdr, 48, 0x3aa9480ad0)  # statics ptr
        struct.pack_into('<Q', hdr, 64, 0x3aa9480610)  # native_table ptr
        struct.pack_into('<I', hdr, 88, 0xafd9916d)    # hash
        struct.pack_into('<Q', hdr, 104, 0x3aa7e7beb0) # string_pages ptr addr
        struct.pack_into('<I', hdr, 112, 1551)          # string_size
        self.header = bytes(hdr)

        # Mock memory storage
        self.mem_store = {
            0x3aa7e7bea0: struct.pack('<Q', 0x3aa7e7c080), # code_page
            0x3aa7e7beb0: struct.pack('<Q', 0x3aa9480000), # string_page
            self.host['stack']: bytes(0x800),
            self.host['program'] + 64: struct.pack('<Q', 0x3aa9480610),
            self.host['program'] + 28: struct.pack('<I', 15830),
            self.host['program'] + 44: struct.pack('<I', 151),
            self.host['program'] + 112: struct.pack('<I', 1551),
            self.host['thread'] + 8: bytes(0xa8),
            0x3aa7e7c080: bytes(1000),
            0x3aa9480000: bytes(3528),
            0x3aa9480610: bytes(151 * 8),
            self.base + 0x1000: b'\x00\x00\x00\x00\x00\x00\x00\x00',
        }
        self.remote = type('MockRemote', (), {
            'read': lambda s, addr, sz: self.mem_store.get(addr, bytes(sz))[:sz] if addr in self.mem_store else bytes(sz),
            'write': lambda s, addr, data: self.mem_store.__setitem__(addr, bytearray(data))
        })()
        self.profile = type('MockProfile', (), {
            'handlers': {'0x1234': 0x1000},
            'code': bytes(0x2000)
        })()

    def test_plan_inplace_mode_when_strings_fit(self):
        from nxtrainer.runtime import plan
        payload = type('MockPayload', (), {
            'code': b'\x2e\x00\x00',
            'strings': b'hello\0',
            'statics': bytes(95 * 8),
            'natives': [{'build2699': '0x1234', 'name': 'TEST'}]
        })()
        regions = plan(self.remote, self.profile, self.base, self.host, self.context, self.header, payload)
        reg_names = {r['name'] for r in regions}
        self.assertIn('strings', reg_names)
        self.assertIn('natives', reg_names)
        self.assertNotIn('native_ptr', reg_names)
        self.assertNotIn('string_page_ptr', reg_names)
        # Check that strings target is original 0x3aa9480000
        string_reg = [r for r in regions if r['name'] == 'strings'][0]
        self.assertEqual(string_reg['address'], 0x3aa9480000)

    def test_plan_decoupled_relocation_when_strings_exceed_inplace_capacity(self):
        from nxtrainer.runtime import plan
        # Create strings larger than 1551 bytes
        large_strings = b'A' * 1800
        payload = type('MockPayload', (), {
            'code': b'\x2e\x00\x00',
            'strings': large_strings,
            'statics': bytes(95 * 8),
            'natives': [{'build2699': '0x1234', 'name': 'TEST'}]
        })()
        regions = plan(self.remote, self.profile, self.base, self.host, self.context, self.header, payload)
        reg_names = {r['name'] for r in regions}
        self.assertIn('native_ptr', reg_names)
        self.assertIn('string_page_ptr', reg_names)
        # Check that native table is relocated to base of resource pool (0x3aa9480000)
        native_reg = [r for r in regions if r['name'] == 'natives'][0]
        self.assertEqual(native_reg['address'], 0x3aa9480000)
        # Check string target starts after native data (aligned to 16 bytes: 8 -> 16 bytes = 0x3aa9480010)
        string_reg = [r for r in regions if r['name'] == 'strings'][0]
        self.assertEqual(string_reg['address'], 0x3aa9480010)

    def test_decoupled_relocation_restores_cleanly(self):
        import struct
        from nxtrainer.runtime import plan, restore_regions
        large_strings = b'B' * 1800
        payload = type('MockPayload', (), {
            'code': b'\x2e\x00\x00',
            'strings': large_strings,
            'statics': bytes(95 * 8),
            'natives': [{'build2699': '0x1234', 'name': 'TEST'}]
        })()
        regions = plan(self.remote, self.profile, self.base, self.host, self.context, self.header, payload)
        # Apply changes to mem_store
        for r in regions:
            self.mem_store[r['address']] = bytearray(bytes.fromhex(r['after']))
        # Verify pointers are updated
        native_ptr_val = struct.unpack_from('<Q', self.mem_store[self.host['program'] + 64])[0]
        self.assertEqual(native_ptr_val, 0x3aa9480000)
        # Now restore regions
        restore_regions(self.remote, regions)
        # Verify original pointers are restored without dangling pointers
        restored_native_ptr = struct.unpack_from('<Q', self.mem_store[self.host['program'] + 64])[0]
        self.assertEqual(restored_native_ptr, 0x3aa9480610)
        restored_str_page_ptr = struct.unpack_from('<Q', self.mem_store[0x3aa7e7beb0])[0]
        self.assertEqual(restored_str_page_ptr, 0x3aa9480000)

if __name__=='__main__':unittest.main()
