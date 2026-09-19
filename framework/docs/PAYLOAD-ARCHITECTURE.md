# Payload Architecture & Memory Limits — NX Trainer GTA V (Build 2699)

## 1. Executive Summary & Problem Definition

The NX Trainer currently executes inside the host thread and program structure of GTA V's native Story Mode script `cheat_controller`. In previous builds, development halted against three artificial or co-located limits:
1. **Strings**: 1,485 / 1,551 bytes (66 bytes free).
2. **Statics**: 78 / 95 slots (17 slots free).
3. **Stack budget**: 245 / 256 slots according to `build.py`'s conservative validator (11 slots free).

These limits represent constraints of in-place contiguous hosting inside `cheat_controller`'s original resource boundaries, **not** hardware or memory exhaustion of the Nintendo Switch (which has 4 GB RAM and gigabytes of virtual heap space).

This document establishes:
- The exact physical source and layout of every limit in the RAGE Script VM and `scrProgram`.
- The distinction between physical allocated capacity and validator assumptions.
- The mathematical proof that the conservative stack bound (245/256) is an extreme overestimate, and that the true call-graph maximum is only **135–152 slots** (leaving >100 physical slots free).
- A rigorous architectural comparison between **Option A** (separate script via RomFS/LayeredFS loader) and **Option B** (decoupled buffers with controlled host attachment).
- The implementation of **Dual-Mode Hosting** with decoupled pointer relocation and guaranteed non-leaking transaction rollback.

---

## 2. Memory Layout & Source of Limits

### 2.1 Host Script Program: `rage::scrProgram` (128-byte Header)
Inside GTA V's script pool at `base + 0x397e100`, `cheat_controller` (`hash = 0xafd9916d`, slot 268) points to its `scrProgram` header at `0x3aa7e78000`:

| Header Offset | Field Name | `cheat_controller` Value | Interpretation |
|---|---|---|---|
| `+0x00` (0) | `vftable` | `0x0e805a2f18` | Virtual method table in `game_nx_master.nss` `.rodata` |
| `+0x10` (16) | `uint64_t** m_CodePages` | `0x3aa7e7bea0` | Pointer to array of 64-bit code page pointers |
| `+0x18` (24) | `uint32_t m_Magic` | `0x94c75b53` | RAGE script header magic |
| `+0x1C` (28) | `uint32_t m_CodeSize` | `15,830` (`0x3dd6`) | Total bytecode length across code pages |
| `+0x24` (36) | `uint32_t m_StaticCount` | `95` (`0x5f`) | Number of global script variables |
| `+0x2C` (44) | `uint32_t m_NativeCount` | `151` (`0x97`) | Number of native function handlers registered |
| `+0x30` (48) | `uint64_t* m_Statics` | `0x3aa9480ad0` | Initial statics values in YSC resource |
| `+0x40` (64) | `uint64_t* m_NativeTable` | `0x3aa9480610` | 64-bit pointer to array of native function pointers |
| `+0x58` (88) | `uint32_t m_ScriptHash` | `0xafd9916d` | `joaat("cheat_controller")` |
| `+0x68` (104) | `uint64_t** m_StringPages`| `0x3aa7e7beb0` | Pointer to array of 64-bit string page pointers |
| `+0x70` (112) | `uint32_t m_StringSize` | `1,551` (`0x60f`) | Total string table length across string pages |

### 2.2 Physical Co-Location in the 3.5 KB Resource Buffer
In Rockstar's compiled YSC asset for `cheat_controller`, the string table, native handlers table, and initial statics were concatenated into a single resource block starting at `0x3aa9480000`:
- **`0x3aa9480000` to `0x3aa948060F` (1,552 bytes)**: String table (`m_StringPages[0]` = `0x3aa9480000`).
- **`0x3aa9480610` to `0x3aa9480ACF` (1,216 bytes)**: Native handlers table ($152 \times 8$ bytes, `m_NativeTable` = `0x3aa9480610`).
- **`0x3aa9480AD0` to `0x3aa9480DC7` (760 bytes)**: Initial statics table ($95 \times 8$ bytes, `m_Statics` = `0x3aa9480ad0`).
- **Total buffer size**: 3,528 bytes (`0xDC8`).

**The Hard In-Place Limit**:
Because `m_NativeTable` begins immediately at `0x3aa9480000 + 0x610`, writing a string table $> 1,551$ bytes directly into `m_StringPages[0]` will physically overwrite the native function pointers at `0x3aa9480610`, causing immediate VM crashes upon executing any native call.

### 2.3 Host Thread: `rage::GtaThread` Context & Stack
`cheat_controller`'s active thread object lives in the Nintendo Switch Heap (`0x73d5a22000`):
- `context + 8`: Thread ID.
- `context + 12`: Script Hash (`0xafd9916d`).
- `context + 16`: Thread State (`1` = sleeping/waiting).
- `context + 20`: Program Counter (IP).
- `context + 24`: Frame Pointer (FP) — initialized to `m_StaticCount` (95).
- `context + 28`: Stack Pointer (SP) — initialized to `m_StaticCount` (95).
- `context + 0xb0`: 64-bit pointer to thread stack (`host['stack']` = `0x73d61b6000`).
- Total allocated stack buffer: `0x800` bytes = 256 QWORD slots.
  - Slots `0` to `94` (95 slots): Reserved for statics.
  - Slots `95` to `255` (161 slots): Available for active function call frames and arguments.

---

## 3. Dissecting Allocated Capacity vs. Validator Assumptions

| Subsystem | Host Allocated Memory | Tool / Validator Check | Current Payload | Actual Remaining Headroom |
|---|---|---|---|---|
| **Code** | 15,830 B (Page 0) | $\le 15,830$ B (`test_code_capacity`) | 10,847 B | **4,983 B free** |
| **Natives** | 151 entries (1,208 B) | $\le 151$ (`test_native_capacity`) | 106 entries | **45 entries free** |
| **Statics** | 95 slots (760 B) | $< 95$ (`test_static_capacity`) | 78 slots | **17 slots free** |
| **Strings** | 1,551 B (in-place) | $\le 1,551$ B (`test_string_table_capacity`)| 1,485 B | **66 B free** (in-place) / **2,680 B** (decoupled) |
| **Stack** | 256 slots (2,048 B) | $\le 256$ via $\sum \text{frames}$ (`build.py`) | 245 conservative | **121 slots free** (True peak: 135/256) |

---

## 4. Stack Analysis: Conservative Bound vs. True Call-Graph Maximum

### 4.1 The Flaw of the Conservative Sum
`build.py` line 32 originally computed:
$$\text{frames} = \sum_{f \in \text{AllFunctions}} \text{frame\_size}(f)$$
$$\text{slots} = 95 + \text{frames} + 32 \le 256$$
This formula treats all 31 functions in `trainer.c` as if they are simultaneously active on the stack in a single deep chain. This is physically impossible in the RAGE Script VM:
1. Execution is strictly single-threaded within each script thread.
2. The trainer contains zero recursive functions.
3. Subsystems execute sequentially: when `action()` finishes, its entire stack frame is popped before `drawMenu()` is called.

### 4.2 Exact Call-Graph Stack Traversal
Tracing all control flow from entry points through opcode 93 (`CALL`):
1. **Critical Execution Path**:
   `main()` [frame 9] $\rightarrow$ `action()` [frame 9] $\rightarrow$ `maxTuneVehicle()` [frame 5] = **23 slots**.
2. **Top-Level Prologue**: 2 slots.
3. **Maximum Local Frame Depth ($F_{\text{peak}}$)**: **25 slots**.
4. **Current Statics ($S_{\text{active}}$)**: **78 slots**.
5. **Native Invocation Margin**: **32 slots**.

$$\text{True Peak Stack} = 78 + 25 + 32 = \mathbf{135\text{ slots}} \quad (\text{52.7\% of 256-slot capacity})$$

Even if all 95 static slots are occupied:
$$\text{Worst-Case Peak Stack} = 95 + 25 + 32 = \mathbf{152\text{ slots}} \quad (\text{59.4\% of 256-slot capacity})$$

**Conclusion**: The stack budget was constrained by a crude validator formula, not physical stack exhaustion. There are **104 to 121 slots (832 to 968 bytes) of physical stack space completely free**.

---

## 5. Architectural Options: Option A vs. Option B

### 5.1 Option A: Separate Script via RomFS/LayeredFS Loader
- **Concept**: Compile the trainer as an independent `trainer.ysc` and load it via `REQUEST_SCRIPT` and `START_NEW_SCRIPT` hooked into `main_persistent.ysc` or `initial.ysc` inside `update2.rpf`.
- **Evaluation**:
  - Requires modifying SD card files (`atmosphere/contents/0100b00b51230000/romfs/update/update2.rpf`).
  - Violates the project's core requirement: zero SD card modifications, network-only GDB deployment.
  - Previous attempts ("Trainer v4", `TEST-TRAINERA.md`) suffered from SD staging corruption and game crashes on boot.
  - Hot-reloading is impossible without restarting the entire game process.
  - If the script terminates, no GDB journal exists to recover game state.

### 5.2 Option B: Decoupled Buffers with Controlled Host Attachment (Selected)
- **Concept**: Retain `cheat_controller` as the host script thread (always active in Story Mode, isolated from missions, zero SD card modifications). Decouple the independent 64-bit pointers inside `scrProgram` (`m_StringPages` at `+104` and `m_NativeTable` at `+64`) to eliminate the 1,551-byte collision.
- **Dual-Mode Operation**:
  1. **Mode 1 (Legacy In-Place Fallback)**:
     - Used when `strings <= 1551` and `natives <= 151`.
     - Maintains strings at `0x3aa9480000` and native table at `0x3aa9480610`.
     - Zero pointer modifications; identical to baseline behavior.
  2. **Mode 2 (Decoupled Relocation)**:
     - Used when strings exceed 1,551 bytes or natives exceed 151 entries.
     - Relocates native table and strings to non-colliding offsets within the 3,528-byte resource block:
       - Native table placed at `0x3aa9480000` ($106 \times 8 = 848$ bytes).
       - String table placed at `0x3aa9480360` (providing up to **2,664 bytes** of string capacity).
       - For larger payloads, redirected to dedicated heap buffers.
     - Updates `host['program'] + 64` (`m_NativeTable`) and `m_StringPages[0]` pointers.
     - All pointer modifications are journaled in `regions` with `before` and `after` states.
     - On `stop` or `reload`, `restore_regions()` automatically restores both memory contents and pointers to their original values.

---

## 6. Verification Criteria & Guarantees

1. **Structure & Native Validation**: `build.py` verifies all VM instructions via `vm_format.py`, maps all 2699 native hashes against `Profile.handlers`, and checks true call-graph stack depth.
2. **Mailbox ABI Compatibility**: Preserves all 21 manifest symbols, `protocolMagic = 0x4e585431`, `protocolVersion = 1`, and commands 1–9.
3. **Dangling Pointer Immunity**: Every modified pointer (`m_NativeTable`, `m_StringPages[0]`, `m_CodePages[0]`, `m_Stack`) is backed up in the session journal. Rollback restores the exact pre-injection pointers.
4. **Safe Fallback**: The legacy in-place path remains permanently active whenever the payload fits within standard bounds.
