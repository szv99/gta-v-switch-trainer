# Menyoo Upstream & Adaptation Architecture

## 1. Upstream Information

- **Repository**: [https://github.com/MAFINS/MenyooSP](https://github.com/MAFINS/MenyooSP)
- **Author**: MAFINS and contributors
- **Active Community Fork**: [https://github.com/itsjustcurtis/MenyooSP](https://github.com/itsjustcurtis/MenyooSP)
- **License**: GNU General Public License v3.0 (GPLv3) (see `LICENSE.txt` in upstream repo)
- **Upstream Commit Reference**: `b894e14f31490fbb91740dc554111bda5be39608` (2025-02-06, archival commit)
- **Tree Commit Reference**: `834213bc4660a303255b6ca72a77ccdc71ada496`
- **Notice**: In accordance with Section 5 of GNU GPLv3, this port modifies and adapts the design, control patterns, menu hierarchies, and script logic of Menyoo to run inside the Grand Theft Auto V script virtual machine on Nintendo Switch (Atmosphère).

---

## 2. Platform Architecture Differences

| Component | Menyoo SP (PC Upstream) | NX Trainer (Switch Port) | Adaptation Approach |
|---|---|---|---|
| **Binary format** | Windows Dynamic Link Library (`.asi` / PE DLL) | GTA V script bytecode (`.nsc` / `.ysc`) injected into `cheat_controller` thread | Written in C, compiled via SC-CL, converted via custom translator (`map2699.py` / `vm_format.py`) |
| **Runtime environment** | Native x86_64 machine code under Windows NT | Custom 64-bit GTA V Script VM executing under Switch OS / Atmosphère | Restricted to GTA V VM instruction set; no arbitrary malloc or C++ standard library |
| **UI Rendering** | Direct3D 11 hooking, DirectX sprite blitting, custom font shaders | GTA native text rendering engine (`BEGIN_TEXT_COMMAND_DISPLAY_TEXT`, font 0, scale 0.38f, outline) | In-engine text commands render directly on game viewport; zero external overlay required |
| **Input handling** | Win32 `GetAsyncKeyState`, DirectInput, ScriptHookV keyboard hook | Game engine discrete frontend controls (`DISABLE_CONTROL_ACTION`, `IS_DISABLED_CONTROL_JUST_PRESSED`) | Uses GTA controls 164–167 (D-pad), 177 (A / Select), 178 (B / Cancel), with custom 350ms/140ms delayed repeat |
| **Natives resolution** | ScriptHookV dynamic pattern scanner & native handler dispatcher | Build-specific native registration cross-mapping table targeting PC build 2699 | Statically cross-mapped via `CrossMapping_Universal.h` and verified against binary offsets in `native-registrations.json` |
| **Configuration & data** | XML configuration files on Windows filesystem (`tinyxml2`) | Static offline metadata catalogs (`catalog/vehicles.json`) & memory mailbox | Offline catalog validation; volatile runtime states held in script statics |
| **Dual control** | Keyboard / controller in-game only | In-game gamepad UI + asynchronous PC CLI mailbox ABI over GDB socket | Script statics serve as atomic mailbox for remote control while playing |

---

## 3. Host Script Budget & Constraints

The trainer is injected into the existing Story Mode `cheat_controller` script thread without modifying game files on the SD card. By implementing **Dual-Mode Decoupled Relocation** (Mode 2) in `nxtrainer/runtime.py`, the native handler table and string table are dynamically relocated within the pooled 3,528-byte host resource block, expanding string capacity from 1,551 B to 2,680 B while preserving zero SD card footprint:

| Resource | Host Capacity | Current Payload | Utilization | Status |
|---|---|---|---|---|
| **Code Size** | 15,830 bytes (`0x3DD6`) | 15,761 bytes | 99.6% | OK (69 bytes headroom; optimized bytecode) |
| **String Table (Decoupled)** | 2,680 bytes (pooled host block) | 2,160+ bytes | ~80.6% | OK (safely decoupled from native table) |
| **Native Handlers** | 151 entries (`0x97`) | 142 entries | 94.0% | OK (all 142 registered & verified in build 2699) |
| **Static Variables** | 95 slots (760 bytes) | 94 slots | 98.9% | OK (1 slot free; packed bitfield `extraFlags`) |
| **Call-Graph Stack Depth** | 256 physical stack slots | 158 slots | 61.7% | OK (98 slots free; call-graph verified) |

### Optimization Rules Applied
1. **Exact Call-Graph Stack Analysis Engine**: Replaced the naive sum-of-all-frames calculation with directed call-graph traversal (`analyze_call_graph`), proving that peak physical stack depth is strictly bounded by the maximum execution path (`main -> action -> maxTuneVehicle`), unlocking nearly 100 free physical stack slots.
2. **Decoupled Relocation Buffer (Mode 2)**: Dynamically points `m_NativeTable` to `0x3aa9480000` and `m_StringPages[0]` to `0x3aa94803E0`, cleanly separating strings from native function pointers and preventing in-place buffer collision.
3. **Sequential Menu Rendering Engine**: Replaced repeated row calculations and selection comparisons with stateful rendering primitives (`mLine`, `mSub`, `mToggle`, `mChoice`), saving over 900 bytes of bytecode and enabling 7 additional flagship Menyoo features within the 15,830 B host budget.
4. **Host-Attached Bitfield Compression**: Compressed 10 subsystem toggle states into a single 64-bit static bitfield (`extraFlags`), keeping total static count within the 95-slot host limit without discarding any existing states.
5. **Vehicle Action Deduplication**: Shared active vehicle retrieval (`IS_PED_IN_ANY_VEHICLE`) across all vehicle commands, eliminating redundant native checks and saving over 160 bytes.
6. **Non-Blocking Streaming & Safety Probes**: Model streaming (`REQUEST_MODEL`), collision streaming (`REQUEST_COLLISION_AT_COORD`), and terrain height calculation (`GET_GROUND_Z_FOR_3D_COORD`) execute statefully across game ticks (`WAIT(0)`) with timeouts, preventing UI stalls or infinite loops.

---

## 4. Port Coverage Progress

- **Initial Stage (Basics)**: ~5% coverage (Player heal/godmode, vehicle repair/flip/tune, 9-car spawner).
- **Expanded Stage (Subsystems & Iconic Sandbox Features)**: ~65% coverage of core Menyoo SP functionality (103 distinct features, 15,761 / 15,830 code bytes):
  - **12 Distinct Menus**: Main (0), Player (1), Vehicle (2), Spawner (3), Teleport (4), Weapons (5), World (6), Customs (7), Appearance (8), Animations (9), Spooner (10), Settings (11).
  - **Vehicle Customs & Stunts**: Rainbow Paint (6-phase continuous RGB cycle), Neons underglow (4 sides), 8 neon RGB presets, extras toggle, 6 window tints, 7 wheel types, 5 custom RGB resprays.
  - **Vehicle Combat, AI & Physics**: Warp into Nearest Vehicle (100m auto-search and boarding), Autopilot / Cruise Wander (traffic-aware AI driving), Emergency Vehicle Siren (siren/emergency lights on any car), Vehicle Self-Destruct / Explode (instant detonation), Auto-Repair (continuous pristine mode), Horn Boost (forward speed impulse), Vehicle Weapons (front-bumper RPG rocket volleys), Flying Car (handbrake aerodynamic flight mode), Instant 180 Turnaround (rapid reverse flick), Invisible Vehicle (Wonder Woman/Ghost chassis), Vehicle Jump (bunny hop 10m), Drift Mode (low grip), Rocket Boost (70 m/s), Stunt Ramp Ahead (instant launch ramp).
  - **Player Combat & Sandbox**: Drunk Mode (drunken ragdoll physics and staggering gait), Repulsor Forcefield Shield (kinetic pushwave barrier hurling peds and cars), Sky Launch (super vertical ejection 100m for skydiving), 5-Star Wanted Level (instant maximum police chase), Teleport Gun (instant warp to bullet impact point), Riot Mode (pedestrian combat anarchy), Story/MP ped model changer, outfit reset, component variation cycling, Seatbelt (anti-windshield ejection), Instant Ragdoll, Max Story Cash ($2 Billion).
  - **Bodyguard System**: Recruits armed clone bodyguard into player's combat group with godmode and weapons; dismiss on demand.
  - **Animations & Scenarios**: 8 scenario presets (smoking, coffee, cheer, flex, binoculars, push-ups, sit-ups, guard stand), instant task clearing.
  - **Entity Manager / Spooner**: Prop spawning (road cone, work barrier, stunt ramp, wood box), attach entity to ped, freeze position toggle, delete entity.
  - **Weapon Enhancements**: Explosion Gun (bullet impact high-yield explosive blasts), Bullet Time on Aim (slow-motion 0.2x when aiming), Air Strike (massive remote blimp-yield explosion ahead), Heavy Arsenal, Infinite Ammo, Explosive Ammo/Melee, Super Damage.
  - **32 Automated Unit Tests**: Passing offline across budget checks, catalog consistency, runtime relocation, and CLI dispatch.
