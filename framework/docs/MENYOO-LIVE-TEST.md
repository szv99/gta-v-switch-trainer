# Menyoo Live Test Procedure — Nintendo Switch (Atmosphère)

## 1. Safety & Environment Rules

> [!IMPORTANT]
> - **IP Console**: `192.168.0.122` (GDB port `22225`).
> - **Single Controller Lock**: Always use `with locked():` via `trainer.py`. Never kill another agent's process or delete `state/controller.lock`.
> - **LSO Isolation**: This task is strictly independent of Los Santos Online. Do NOT modify network patches or globals.
> - **Short GDB Attachment**: The debugger connects, performs operations, and detaches immediately in `finally` blocks to keep the game thread running smoothly.

---

## 2. Compilation & Verification Before Live Test

Run the build pipeline and test suite from PowerShell:

```powershell
# 1. Compile C script to GTA VM bytecode, translate instructions, and emit manifest
C:\Python314\python.exe build.py

# 2. Run all 26 automated unit tests (budgets, limits, catalog, CLI, protocol)
C:\Python314\python.exe -m unittest discover -s tests -v
```

Ensure both commands succeed with 0 errors before connecting to the console.

---

## 3. Live Deployment & Testing Sequence

Ensure Grand Theft Auto V is running in **Story Mode** on the Switch.

### Step 1: Discovery & PID Identification
```powershell
C:\Python314\python.exe trainer.py discover
```
*Expected*: Returns JSON with running GTA `pid`, module `base` address, and `cheat_controller` thread ID.

### Step 2: Install or Reload Payload
```powershell
# First-time installation:
C:\Python314\python.exe trainer.py install

# Or if an earlier session is already active:
C:\Python314\python.exe trainer.py reload
```
*Expected*: `Trainer running: {"heartbeat": ..., "runtimeStatus": 1}`.

### Step 3: Verify In-Game Menu Navigation (Gamepad)

1. **Open Menu**: Hold **R (Cover / 44)** and press **D-pad Right (Context / 38)** or **D-pad Left (166)**.
   *Check*: Overlay appears with title `Menyoo | Main`.
2. **D-pad Movement & Repeat**:
   - Press **D-pad Down (164)** and **Up (165)** to move between rows.
   - Hold D-pad Down: cursor should start scrolling after 350ms and smoothly repeat every 140ms.
3. **Submenu Entry & Back**:
   - Press **A (177)** on `Player >`: opens `Menyoo | Player`.
   - Press **A (177)** on `< Back` or press **B (178)**: returns to `Menyoo | Main`.
4. **Pause Menu Yielding**:
   - Open in-game pause map (`+` button).
   - *Check*: Trainer menu does NOT draw and does NOT consume map navigation controls.
   - Close pause menu: trainer controls resume properly.

### Step 4: Category Function Tests

#### Player Options
- Select `Heal + Armour`: Character health restored to maximum, body armor bar filled.
- Select `Clear Wanted Level`: Cops called off immediately.
- Select `Invincible: [ON]`: Godmode enabled. Fall from height or shoot feet — no health lost.
- Toggle `Invincible: [OFF]`: Returns to taking damage normally.
- Select `Never Wanted: [ON]`: Star rating remains permanently 0.

#### Vehicle Options
- Spawn vehicle or enter any car.
- Damage car, break windows, dirty car.
- Select `Repair Vehicle`: Health, engine, and deformations repaired.
- Select `Clean Vehicle`: Dirt and mud removed.
- Overturn car on its roof. Select `Flip Upright`: Car rotated to level pitch/roll and placed properly on wheels.
- Select `Max Tuning`: Engine, brakes, transmission, suspension, and turbo installed.
- Select `Delete Last Spawned`: Trainer-spawned vehicle deleted.

#### Vehicle Spawner
- Navigate to `Category`: Press **D-pad Left/Right** to cycle `Super`, `Sports`, `Muscle`, `Compact`, `SUV`, `Motorcycle`, `Off-Road`.
- Navigate to `Model`: Press **D-pad Left/Right** to cycle models in chosen category (e.g. `Adder`, `Zentorno`).
- Toggle `Spawn Inside: [ON]`: Player automatically placed behind the steering wheel upon spawn.
- Press **A** on `Spawn Vehicle`: Vehicle appears on road ahead with ground placement.

#### Teleport Options
- Place custom waypoint on map pause screen. Return to game.
- Select `Waypoint`: Ground elevation probed, vehicle/player teleported onto terrain safely without falling through the void.
- Select `Michael's House`: Teleported to Rockford Hills driveway.
- Select `Mount Chiliad`: Teleported to the summit platform.

#### World Options
- Select `Pause Clock: [ON]`: In-game shadows and daytime clock stop advancing.
- Select `Time: < Morning (08:00) >` -> `Apply Time`: Sun shifts to morning position.
- Select `Weather: < Rain >` -> `Apply Weather`: Rainstorm starts.
- Select `Reset Weather`: Weather cycle returns to dynamic Story Mode weather.

### Step 5: Remote CLI Command Verification

You can also test each feature directly from PC PowerShell without using the gamepad:

```powershell
C:\Python314\python.exe trainer.py status
C:\Python314\python.exe trainer.py heal
C:\Python314\python.exe trainer.py wanted-clear
C:\Python314\python.exe trainer.py invincible on
C:\Python314\python.exe trainer.py spawn adder
C:\Python314\python.exe trainer.py repair
C:\Python314\python.exe trainer.py clean
C:\Python314\python.exe trainer.py flip
C:\Python314\python.exe trainer.py tune
C:\Python314\python.exe trainer.py teleport michael
C:\Python314\python.exe trainer.py teleport waypoint
C:\Python314\python.exe trainer.py time noon
C:\Python314\python.exe trainer.py weather rain
C:\Python314\python.exe trainer.py weather reset
C:\Python314\python.exe trainer.py delete-vehicle
```

### Step 6: Graceful Stop & Restoration
```powershell
C:\Python314\python.exe trainer.py stop
```
*Expected*:
1. Godmode disabled, clock unpaused, weather persistence cleared.
2. In-game script sets `runtimeStatus = 2` (cleanup acknowledged).
3. Host `cheat_controller` original RAM bytes restored and verified against baseline.
4. Console reports: `Stopped, effects cleaned up, original RAM restored and verified.`

---

## 4. Troubleshooting & Recovery

- If GDB reports `Another trainer command is running`: Wait a few seconds for the file lock to release.
- If a write was interrupted:
  ```powershell
  C:\Python314\python.exe trainer.py recover
  ```
- If the game crashes or is closed: Relaunch GTA into Story Mode. `install` automatically detects the new PID and module base.
