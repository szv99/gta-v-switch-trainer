# GTA V Nintendo Switch (Build 2699) In-Memory GDB Trainer

> [!WARNING]
> **Work In Progress (WIP) — Developer & Reverse Engineering Preview**  
> This project is in active development. It is primarily intended for developers, reverse engineers, and CFW modding researchers. The GDB remote injection, native cross-mapping, and CLI controls are stable, while the in-game UI input focus is currently being refined.

A zero-reboot, in-memory script trainer and research framework targeting **Grand Theft Auto V** on the **Nintendo Switch** (Title ID `01004CD00DB34000`, Build 2699 / v1.0.3).

Instead of repackaging multi-gigabyte RPF archives, this framework uses Atmosphere's GDB stub (`sys-gdbsp` / DMNT2) to inject compiled GTA native script bytecode directly into running game threads and controls them in real time over a shared-memory Mailbox IPC protocol.

---

## Architecture Overview

```
+-------------------------------------------------------+
|                    Host PC (Python)                   |
|                                                       |
|   +--------------------+     +--------------------+   |
|   |   trainer.py CLI   | <-> |  nxtrainer Runtime |   |
|   +--------------------+     +--------------------+   |
|                                        | GDB (RSP)    |
+----------------------------------------|--------------+
                                         | TCP :22225
+----------------------------------------|--------------+
|            Nintendo Switch (Atmosphere CFW)           |
|                                        v              |
|                                  sys-gdbsp            |
|                                        |              |
|   GTA V Process (01004CD00DB34000)     v              |
|   +------------------------------------------------+  |
|   | Script Thread (e.g. am_pi_menu)                |  |
|   |   +------------------------------------------+ |  |
|   |   | Injected Payload: trainer-2699.nsc       | |  |
|   |   | - 142 cross-mapped Switch natives        | |  |
|   |   | - Shared-memory Mailbox ABI (Statics)    | |  |
|   |   | - OSD & Vehicle/Player/World subsystems  | |  |
|   |   +------------------------------------------+ |  |
|   +------------------------------------------------+  |
+-------------------------------------------------------+
```

1. **SC-CL & Bytecode Toolchain**: The trainer script is written in C (`framework/script/trainer.c`) and compiled via SC-CL into YSC/YSA2 assembly.
2. **Native Cross-Mapping Engine (`map2699.py`)**: GTA V PC native hashes are cross-referenced against the Switch binary's native registration tables to produce a validated `trainer-2699.nsc` bytecode payload mapped to Switch native handlers.
3. **In-Memory Thread Hijacking**: Using Atmosphere's GDB stub over TCP port `22225`, the runtime suspends the target script thread, saves its original code and stack to a recovery journal, and writes the trainer payload in place.
4. **Mailbox IPC ABI**: Bidirectional communication between the PC CLI and the running Switch script is handled via static memory offsets (command ID, arguments, sequence numbers, heartbeat, and status flags).

---

## Current Status

| Subsystem | Status | Description |
|---|---|---|
| **SC-CL Build Pipeline** | ✅ Working | Compiles `trainer.c` to `trainer-2699.nsc` in <1s with full static call-graph checks. |
| **Native Cross-Mapping** | ✅ Working | 142/142 natives mapped and validated against Switch build 2699. |
| **GDB Transport & Injection** | ✅ Working | Clean memory injection, verification hashing, and atomic rollback journal. |
| **Mailbox IPC & CLI Controls** | ✅ Working | Real-time vehicle spawning, teleportation, godmode, repair, weather, and time via CLI. |
| **Unit Test Suite** | ✅ Working | 32/32 tests pass covering memory safety, catalog consistency, and protocol frames. |
| **In-Game OSD Menu** | ⚠️ WIP | Visual menu renders on-screen; input restoration when toggling back to gameplay is under active investigation (CLI control remains fully functional). |

---

## Repository Structure

```
├── README.md               # You are here
├── trainer.py              # Root wrapper for framework/trainer.py
├── trainer-cli.py          # Interactive/command-line entry point
├── map2699.py              # Switch Build 2699 native hash cross-mapping engine
├── vm_format.py            # YSC/YSA2 bytecode parser and validator
├── ysc-ida.py              # IDA Pro / Ghidra analysis helper for Switch scripts
├── framework/
│   ├── build.py            # Compiles C source, translates natives, analyzes stack
│   ├── trainer.py          # Main CLI tool (install, status, monitor, exec)
│   ├── script/
│   │   └── trainer.c       # In-game trainer source code (C)
│   ├── nxtrainer/
│   │   ├── runtime.py      # GDB injection lifecycle, journals & mailbox protocol
│   │   └── transport.py    # Robust GDB Remote Serial Protocol (RSP) client
│   ├── catalog/
│   │   └── vehicles.json   # Verified Switch vehicle hashes and categories
│   ├── docs/               # Technical architectural documentation
│   ├── research/           # Reverse engineering notes on Switch threads & network
│   └── tests/              # Comprehensive test suite (32 unit tests)
├── debug-setup/
│   ├── native-registrations.json # Dumped native handler registration offsets
│   ├── script-native-handlers.json
│   └── system_settings.debug.ini # Atmosphere debugger configuration
└── SC-CL-SampleProject-master/   # Embedded SC-CL compiler & GTA headers
```

---

## Requirements

- **Nintendo Switch**:
  - Atmosphere CFW installed and running.
  - Atmosphere GDB stub enabled (`sys-gdbsp` on port `22225` or `dmnt:cht` debug configuration).
  - Grand Theft Auto V (Title ID `01004CD00DB34000`, Build 2699).
- **Host PC**:
  - Windows (required for SC-CL compiler binary) or Wine on Linux.
  - Python 3.9+ with standard libraries (`socket`, `struct`, `unittest`).

---

## Getting Started

### 1. Build the Payload
Compile the C script and generate the Switch-compatible bytecode payload:
```bash
python framework/build.py
```
This produces `framework/build/trainer-2699.nsc` and updates `framework/build/manifest.json`.

### 2. Run the Verification Tests
```bash
python -m unittest discover -s framework/tests -v
```

### 3. Connect to Switch & Check Status
Make sure GTA V is running in story mode on your Switch, then query the process:
```bash
python trainer.py --ip 192.168.0.XX status
```

### 4. Install the Trainer (In-Memory)
```bash
python trainer.py --ip 192.168.0.XX install
```
This safely attaches via GDB, creates a rollback checkpoint of the target script thread, writes the payload, and establishes heartbeat communication.

### 5. Control via CLI
```bash
# Spawn vehicles
python trainer.py --ip 192.168.0.XX spawn adder
python trainer.py --ip 192.168.0.XX spawn oppressor2

# Player cheats
python trainer.py --ip 192.168.0.XX godmode on
python trainer.py --ip 192.168.0.XX wanted 0
python trainer.py --ip 192.168.0.XX repair
python trainer.py --ip 192.168.0.XX give-weapons

# Teleportation
python trainer.py --ip 192.168.0.XX teleport airport
python trainer.py --ip 192.168.0.XX teleport maze-bank

# World controls
python trainer.py --ip 192.168.0.XX weather thunderstorm
python trainer.py --ip 192.168.0.XX time 23 00
```

### 6. Monitor Live Telemetry
```bash
python trainer.py --ip 192.168.0.XX monitor
```

### 7. Clean Uninstall / Restore Memory
```bash
python trainer.py --ip 192.168.0.XX uninstall
```
Restores the original game thread memory from the session journal without needing to restart the game.

---

## Controller Bindings (In-Game Menu)

When enabled, the trainer can also be controlled directly with the Joy-Cons / Pro Controller:

- **Open / Close Menu**: `L + D-Pad Left` (or `RB + D-Pad Right`)
- **Navigate Up / Down**: `D-Pad Up` / `D-Pad Down`
- **Adjust Option / Value**: `D-Pad Left` / `D-Pad Right`
- **Select / Activate**: `A` button
- **Back / Exit Submenu**: `B` button

*(Note: In-game input restoration is currently under active refinement. Use CLI commands if input feels unresponsive after closing the menu).*

---

## Documentation & Deep Dives

- [`framework/docs/PAYLOAD-ARCHITECTURE.md`](framework/docs/PAYLOAD-ARCHITECTURE.md) — Detailed explanation of thread hijacking and memory layout.
- [`framework/docs/MENYOO-PORT-STATUS.md`](framework/docs/MENYOO-PORT-STATUS.md) — Menyoo feature parity analysis and stack budget calculations.
- [`framework/docs/INPUT-FIX-2026-09-13.md`](framework/docs/INPUT-FIX-2026-09-13.md) — Investigation notes on Switch controller input handling.
- [`framework/research/`](framework/research/) — Network state research and thread tables.

---

## License & Disclaimers

This project is strictly for educational, reverse engineering, and single-player modding research.  
Grand Theft Auto V is a registered trademark of Rockstar Games / Take-Two Interactive. This project is not affiliated with or endorsed by Rockstar Games or Nintendo.
