# Menyoo Port Status — GTA V on Nintendo Switch (Atmosphère)

> **Build target**: GTA V PC port / Build 2699 running under Atmosphère.  
> **Payload Manifest**: Version 0.1.0, Protocol 1, Code: 15,761 B (69 B headroom), Strings: 2,160+ B (Decoupled capacity: 2,680 B), Natives: 142/151, Statics: 94/95, Stack: 158/256 (Call-graph bound).  
> **Status Taxonomy**:
> - `działa live`: Confirmed on physical Nintendo Switch console.
> - `przetestowana offline`: Compiled to bytecode, VM instruction translated, symbol & stack verified, covered by 32 automated unit tests.
> - `zaimplementowana bez testu`: Implemented in C bytecode, awaiting live hardware verification run.
> - `wymaga adaptera`: Missing native or host bridge; requires custom memory/script adapter.
> - `aktualnie niedostępna`: Complex subsystem deferred to later stages (XML parser, complex spooner raycasting, etc.).

---

## 1. Feature Status Matrix

### Category: Player Options
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Heal Player** | `PlayerOptions::Heal` | **działa live** | `NX_HEAL(ped, GET_ENTITY_MAX_HEALTH(ped), 0, 0)` |
| **Max Armour** | `PlayerOptions::AddArmour` | **działa live** | `SET_PED_ARMOUR(ped, 100)` |
| **Clear Wanted Level** | `PlayerOptions::NeverWanted(0)` | **działa live** | `SET_PLAYER_WANTED_LEVEL(PLAYER_ID(), 0, false)` + `SET_PLAYER_WANTED_LEVEL_NOW` |
| **Invincibility (Godmode)** | `PlayerOptions::Invincibility` | **działa live** | `SET_ENTITY_INVINCIBLE(ped, true)`. Reverts cleanly on disable, death, or script cleanup. |
| **Never Wanted Toggle** | `PlayerOptions::NeverWanted` | **przetestowana offline** | State flag locked in script loop; forces wanted level to 0 every tick. |
| **Super Jump Toggle** | `PlayerOptions::SuperJump` | **przetestowana offline** | `NX_SET_SUPER_JUMP_THIS_FRAME(PLAYER_ID())` applied per frame. |
| **Fast Sprint Toggle** | `PlayerOptions::FastSprint` | **przetestowana offline** | `NX_SET_RUN_SPRINT_MULTIPLIER(PLAYER_ID(), 1.49f)`. |
| **Fast Swim Toggle** | `PlayerOptions::FastSwim` | **przetestowana offline** | `NX_SET_SWIM_MULTIPLIER_FOR_PLAYER(PLAYER_ID(), 1.49f)`. |
| **Never Tired (Infinite Stamina)** | `PlayerOptions::UnlimitedStamina` | **przetestowana offline** | `NX_RESTORE_PLAYER_STAMINA(PLAYER_ID(), 1.0f)` restored continuously. |
| **Police Ignore Player** | `PlayerOptions::IgnoredByPolice` | **przetestowana offline** | `NX_SET_POLICE_IGNORE_PLAYER(PLAYER_ID(), toggle)`. |
| **Thermal Vision Toggle** | `PlayerOptions::ThermalVision` | **przetestowana offline** | `NX_SET_SEETHROUGH(toggle)`. |
| **Night Vision Toggle** | `PlayerOptions::NightVision` | **przetestowana offline** | `NX_SET_NIGHTVISION(toggle)`. |
| **Clean Clothes & Wounds** | `PlayerOptions::CleanClothes` | **przetestowana offline** | `NX_CLEAR_PED_BLOOD_DAMAGE` + `NX_RESET_PED_VISIBLE_DAMAGE`. |
| **Invisibility Toggle** | `PlayerOptions::Invisibility` | **przetestowana offline** | `NX_SET_ENTITY_VISIBLE(ped, !toggle, 0)`. |
| **No Ragdoll Toggle** | `PlayerOptions::NoRagdoll` | **przetestowana offline** | `NX_SET_PED_CAN_RAGDOLL(ped, !toggle)`. |
| **Suicide** | `PlayerOptions::Suicide` | **przetestowana offline** | `NX_HEAL(ped, 0, 0, 0)`. |
| **Drunk Mode / Stagger** | `PlayerOptions::Drunk` | **działa live** | `NX_SET_PED_IS_DRUNK(ped, toggle)` activates drunken physics, staggered locomotion, and facial expressions. |
| **Seatbelt Toggle** | `PlayerOptions::Seatbelt` | **przetestowana offline** | `NX_SET_PED_CONFIG_FLAG(ped, 32, false)` locks ped inside vehicle, preventing windshield ejection. |
| **Ragdoll On Demand** | `PlayerOptions::Ragdoll` | **przetestowana offline** | `NX_SET_PED_TO_RAGDOLL(ped, 4000, 4000, 0, false, false, false)` triggers instant ragdoll physics. |
| **Max Story Mode Cash ($2B)** | `PlayerOptions::AddCash` | **przetestowana offline** | `NX_STAT_SET_INT` awards $2,000,000,000 to Michael (`SP0`), Franklin (`SP1`), and Trevor (`SP2`). |
| **Spawn Clone Bodyguard** | `PlayerOptions::Bodyguards` | **przetestowana offline** | `NX_CLONE_PED(ped)` + `NX_SET_PED_AS_GROUP_MEMBER` spawns invincible companion armed with carbine. |
| **Dismiss Bodyguard** | `PlayerOptions::DismissGuard` | **przetestowana offline** | `NX_DELETE_PED(&lastBodyguard)` cleanly cleans up companion entity. |
| **5-Star Wanted Level** | `PlayerOptions::WantedLevel` | **przetestowana offline** | `SET_PLAYER_WANTED_LEVEL(5, false)` + `SET_PLAYER_WANTED_LEVEL_NOW` triggers instant maximum SWAT/heli pursuit. |
| **Repulsor Forcefield Shield** | `PlayerOptions::Forcefield` | **przetestowana offline** | Explosion type 70 (0.0f damage, inaudible, invisible) continuously deflects and launches peds & vehicles away from player. |
| **Sky Launch (Super Ejection)** | `PlayerOptions::BasicStats` | **przetestowana offline** | `NX_APPLY_FORCE_TO_ENTITY` launches player/vehicle 100 meters vertically into the sky for skydive/stunts. |
| **Respawn Detection** | `Routine::OnTick` (ped watch) | **przetestowana offline** | Checks `ped != previousPed`; cleans up dead ped handle and re-applies godmode to revived ped. |
| **Character Switch Handling**| `Routine::OnTick` (ped watch) | **przetestowana offline** | Detects change between Michael/Franklin/Trevor; resets pending models and transfers effects. |

### Category: Vehicle Options
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Repair Vehicle** | `VehicleOptions::Repair` | **działa live** | `SET_VEHICLE_FIXED` + `NX_SET_VEHICLE_DEFORMATION_FIXED` + `NX_SET_VEHICLE_DIRT_LEVEL(0.0f)`. |
| **Clean Vehicle** | `VehicleOptions::Wash` | **przetestowana offline** | `NX_SET_VEHICLE_DIRT_LEVEL(veh, 0.0f)`. |
| **Fix Tyres** | `VehicleOptions::FixTyres` | **przetestowana offline** | Loops `NX_SET_VEHICLE_TYRE_FIXED(v, 0..7)`. |
| **Flip Upright** | `VehicleOptions::Flip` | **przetestowana offline** | `NX_SET_ENTITY_ROTATION` keeping heading + `SET_VEHICLE_ON_GROUND_PROPERLY(veh, 5.0f)`. |
| **Max Performance Tuning** | `VehicleModShop::MaxPerformance` | **przetestowana offline** | `NX_SET_VEHICLE_MOD_KIT(veh, 0)` + max Engine(11), Brakes(12), Transmission(13), Suspension(15), Armor(16) + Turbo(18). |
| **Keep Engine Running** | `VehicleOptions::EngineAlwaysOn` | **przetestowana offline** | `NX_SET_VEHICLE_ENGINE_ON(v, true, true, false)` asserted continuously. |
| **Vehicle Godmode** | `VehicleOptions::Godmode` | **przetestowana offline** | `SET_ENTITY_INVINCIBLE` + `NX_SET_VEHICLE_CAN_BE_VISIBLY_DAMAGED(false)` + `NX_SET_VEHICLE_TYRES_CAN_BURST(false)`. |
| **Bulletproof Tyres** | `VehicleOptions::BulletproofTyres`| **przetestowana offline** | `NX_SET_VEHICLE_TYRES_CAN_BURST(v, false)`. |
| **Instant Stop / Handbrake**| `VehicleOptions::InstantStop` | **przetestowana offline** | `NX_SET_VEHICLE_FORWARD_SPEED(v, 0.0f)`. |
| **Speed Boost (35 m/s)** | `VehicleOptions::SpeedBoost` | **przetestowana offline** | `NX_SET_VEHICLE_FORWARD_SPEED(v, 35.0f)`. |
| **Rocket Boost (70 m/s)** | `VehicleOptions::SpeedBoost` | **przetestowana offline** | `NX_SET_VEHICLE_FORWARD_SPEED(v, 70.0f)` gives supersonic forward impulse. |
| **Vehicle Jump (Bunny Hop)** | `VehicleOptions::VehicleJump` | **przetestowana offline** | `NX_APPLY_FORCE_TO_ENTITY(v, 1, 0, 0, 11.0f, ...)` launches vehicle 10m into the air. |
| **Drift Mode / Low Grip** | `VehicleOptions::DriftMode` | **przetestowana offline** | `NX_SET_VEHICLE_REDUCE_GRIP(v, toggle)` enables effortless power sliding. |
| **Stunt Ramp Ahead** | `VehicleOptions::SpawnRampAhead` | **przetestowana offline** | Streams & freezes `prop_mp_ramp_01` 14m in front of vehicle aligned with heading. |
| **Auto-Repair (Pristine)** | `VehicleOptions::AutoRepair` | **przetestowana offline** | Continuously fixes vehicle deformation, mechanical damage, and dirt level every tick. |
| **Horn Boost** | `VehicleOptions::HornBoost` | **przetestowana offline** | `NX_SET_VEHICLE_FORWARD_SPEED(v, 50.0f)` triggered whenever horn control (86) is pressed. |
| **Vehicle Weapons (Rockets)** | `VehicleWeapons::Rockets` | **przetestowana offline** | Computes 80m forward vector and fires RPG rocket via `NX_SHOOT_SINGLE_BULLET`. |
| **Flying Car (Flight Mode)** | `VehicleOptions::Fly` | **przetestowana offline** | Applying handbrake (76) imparts 15m forward impulse and 8m vertical aerodynamic lift. |
| **Instant 180 Turnaround** | `VehicleOptions::Quick180` | **przetestowana offline** | Whips vehicle heading 180 degrees instantaneously via `NX_SET_ENTITY_ROTATION` keeping forward velocity. |
| **Invisible Vehicle** | `VehicleOptions::Invisibility` | **przetestowana offline** | `NX_SET_ENTITY_VISIBLE(v, false, 0)` makes chassis completely invisible while driver/wheels/exhaust remain active. |
| **Toggle Vehicle Doors** | `VehicleOptions::ToggleDoors` | **przetestowana offline** | Toggles `NX_SET_VEHICLE_DOOR_OPEN` / `NX_SET_VEHICLE_DOORS_SHUT`. |
| **Primary/Secondary Respray**| `VehicleModShop::Respray` | **przetestowana offline** | Choice selector between 8 factory paint finishes (`NX_SET_VEHICLE_COLOURS`). |
| **License Plate Style** | `VehicleModShop::PlateStyle` | **przetestowana offline** | Choice selector across 4 plate formats (`NX_SET_VEHICLE_NUMBER_PLATE_TEXT_INDEX`). |
| **Warp into Nearest Vehicle** | `VehicleOptions::WarpIntoNearest` | **działa live** | `NX_GET_CLOSEST_VEHICLE(x, y, z, 100.0f, 0, 70)` searches radius 100m and warps ped into driver seat (`NX_SET_PED_INTO_VEHICLE`). |
| **Vehicle Autopilot / Wander**| `VehicleOptions::AutoPilot` | **działa live** | `NX_TASK_VEHICLE_DRIVE_WANDER(ped, v, 30.0f, 786603)` commands AI to cruise through traffic obeying road rules. |
| **Emergency Vehicle Siren** | `VehicleOptions::Siren` | **działa live** | `NX_SET_VEHICLE_SIREN(v, toggle)` activates sirens and flashing emergency lights on any vehicle. |
| **Vehicle Self-Destruct** | `VehicleOptions::SelfDestruct` | **działa live** | `NX_ADD_EXPLOSION(pos, 0, 10.0f, true, false, 2.0f)` violently destroys the active or last vehicle. |
| **Delete Last Spawned** | `VehicleOptions::Delete` | **przetestowana offline** | `NX_DELETE_VEHICLE(&lastVehicle)` deletes *only* trainer-spawned entity, never arbitrary traffic. |
| **Vehicle Safety Check** | `VehicleOptions::IsInVehicle` | **przetestowana offline** | If `!IS_PED_IN_ANY_VEHICLE(ped, false)`, sets `lastResult = -5` ("Enter a vehicle first") without NULL dereference. |

### Category: Vehicle Spawner
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Spawner Categories** | `VehicleSpawner::Categories` | **przetestowana offline** | 7 categories: Super, Sports, Muscle, Compact, SUV, Motorcycle, Off-Road. |
| **Model Catalog** | `VehicleSpawner::ModelList` | **przetestowana offline** | Verified against `catalog/vehicles.json` schema and installed game assets. |
| **Adder & Sultan Spawning** | `VehicleSpawner::Spawn` | **działa live** | Confirmed by user and non-zero handle telemetry. |
| **Asynchronous Streaming** | `Model::Load` with timeout | **działa live** | `REQUEST_MODEL` + `HAS_MODEL_LOADED` with non-blocking 5.0s timeout and `-3` error status. |
| **Spawn in Front of Player**| `VehicleSpawner::SpawnPos` | **działa live** | `GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS(ped, {0, 7, 0.5})` + `SET_VEHICLE_ON_GROUND_PROPERLY`. |
| **Spawn Inside Driver Seat**| `VehicleSpawner::SpawnInSeat` | **przetestowana offline** | `NX_SET_PED_INTO_VEHICLE(ped, veh, -1)` when `spawnInVehicle` option is active. |
| **Spawn Tuned Option** | `VehicleSpawner::SpawnTuned` | **przetestowana offline** | Automatically calls `maxTuneVehicle` on creation. |
| **Spawn Godmode Option** | `VehicleSpawner::SpawnInvincible`| **przetestowana offline** | Automatically arms vehicle invincibility and bulletproof tyres. |
| **Installed Asset Validation** | `IS_MODEL_IN_CDIMAGE` | **działa live** | Rejects uninstalled DLC models before requesting streaming (`lastResult = -2`). |
| **Resource Release** | `SET_MODEL_AS_NO_LONGER_NEEDED`| **działa live** | Immediately frees model memory after successful creation or on abort. |
| **Entity Population Limit** | `SpawnVehicle::TrackedList` | **przetestowana offline** | Tracks `lastVehicle` handle; enables one-touch cleanup and replacement. |

### Category: Teleport Options
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Waypoint Teleport** | `TeleMethods::ToWaypoint` | **przetestowana offline** | Reads waypoint blip (sprite 8); streams scene with `NX_LOAD_SCENE` & `NX_REQUEST_COLLISION_AT_COORD`. |
| **Forward 5m Teleport** | `TeleMethods::ForwardTeleport`| **przetestowana offline** | Warps entity 5m along heading vector through doors/fences (`GET_OFFSET_FROM_ENTITY_IN_WORLD_COORDS`). |
| **Ground Z Height Discovery** | `TeleMethods::GroundZCheck` | **przetestowana offline** | Probes ground collision at 6 heights (100, 200, 50, 300, 500, 800m) with `NX_GET_GROUND_Z`. |
| **Anti-Void Fall Abort** | `TeleMethods::SafeCoords` | **przetestowana offline** | Aborts if ground elevation is not resolved within 3.5 seconds (`lastResult = -13`); never drops into void. |
| **Predefined: Michael's House**| `Locations::MichaelsHouse` | **przetestowana offline** | `(-813.88, 178.68, 72.15, heading 110.0)` |
| **Predefined: Franklin's House**| `Locations::FranklinsHouse` | **przetestowana offline** | `(7.90, 529.80, 170.60, heading 290.0)` |
| **Predefined: Trevor's Trailer**| `Locations::TrevorsTrailer` | **przetestowana offline** | `(1975.20, 3817.30, 33.40, heading 30.0)` |
| **Predefined: LS Customs (Burton)**| `Locations::LSCustoms` | **przetestowana offline** | `(-365.40, -131.80, 38.70, heading 70.0)` |
| **Predefined: LSIA Airport** | `Locations::LSIAirport` | **przetestowana offline** | `(-1034.60, -2733.60, 13.80, heading 330.0)` |
| **Predefined: Maze Bank Tower**| `Locations::MazeBankRoof` | **przetestowana offline** | `(-75.00, -818.50, 326.00, heading 330.0)` |
| **Predefined: Mount Chiliad** | `Locations::MountChiliad` | **przetestowana offline** | `(501.50, 5604.50, 797.90, heading 355.0)` |
| **Predefined: Fort Zancudo** | `Locations::FortZancudo` | **przetestowana offline** | `(-2047.40, 3132.10, 32.80, heading 150.0)` |
| **Predefined: Bolingbroke Prison**| `Locations::Prison` | **przetestowana offline** | `(1846.40, 2585.90, 45.70, heading 90.0)` |
| **Predefined: Galileo Observatory**| `Locations::Observatory` | **przetestowana offline** | `(-438.40, 1072.80, 327.70, heading 340.0)` |
| **Predefined: Sandy Shores Airfield**| `Locations::SandyShores` | **przetestowana offline** | `(1747.00, 3273.00, 41.10, heading 190.0)` |
| **Predefined: Paleto Bay** | `Locations::PaletoBay` | **przetestowana offline** | `(-106.00, 6467.00, 31.60, heading 45.0)` |
| **Predefined: Del Perro Pier** | `Locations::DelPerroPier` | **przetestowana offline** | `(-1686.00, -1072.00, 13.10, heading 50.0)` |
| **Predefined: Humane Labs** | `Locations::HumaneLabs` | **przetestowana offline** | `(3616.00, 3737.00, 28.70, heading 270.0)` |
| **Vehicle Teleportation** | `TeleMethods::TeleportVehicle` | **przetestowana offline** | Teleports vehicle together with ped if seated, resetting velocity and properly seating wheels. |

### Category: Weapon Options
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Give All Standard Weapons** | `WeaponOptions::GiveAllWeapons` | **przetestowana offline** | Delivers 21 standard firearms, melee weapons, and parachute with 9999 ammo. |
| **Refill / Max Ammo** | `WeaponOptions::MaxAmmo` | **przetestowana offline** | Loops over all arsenal weapons with 9999 ammo count. |
| **Infinite Ammo Toggle** | `WeaponOptions::InfiniteAmmo` | **przetestowana offline** | `NX_SET_PED_INFINITE_AMMO(ped, true, 0)`. |
| **Never Reload Toggle** | `WeaponOptions::NeverReload` | **przetestowana offline** | `NX_SET_PED_INFINITE_AMMO_CLIP(ped, true)`. |
| **Explosive Ammo Toggle** | `WeaponOptions::ExplosiveAmmo` | **przetestowana offline** | `NX_SET_EXPLOSIVE_AMMO_THIS_FRAME(PLAYER_ID())`. |
| **Fire Ammo Toggle** | `WeaponOptions::FireAmmo` | **przetestowana offline** | `NX_SET_FIRE_AMMO_THIS_FRAME(PLAYER_ID())`. |
| **Explosive Melee Toggle** | `WeaponOptions::ExplosiveMelee` | **przetestowana offline** | `NX_SET_EXPLOSIVE_MELEE_THIS_FRAME(PLAYER_ID())`. |
| **Super Damage / One-Hit Kill** | `WeaponOptions::DamageMultiplier` | **przetestowana offline** | `NX_SET_PLAYER_WEAPON_DAMAGE_MODIFIER(PLAYER_ID(), 999.0f)`. |
| **Give Heavy Arsenal** | `WeaponOptions::HeavyWeapons` | **przetestowana offline** | Delivers RPG, Minigun, Grenade Launcher, Homing Launcher, Heavy Sniper, Sticky Bombs. |
| **Give Parachute** | `WeaponOptions::GiveParachute` | **przetestowana offline** | `NX_GIVE_WEAPON_TO_PED(ped, 0xFBAB5776, 1, false, true)`. |
| **Remove All Weapons** | `WeaponOptions::RemoveAllWeapons` | **przetestowana offline** | `NX_REMOVE_ALL_PED_WEAPONS(ped, true)`. |
| **Air Strike / Remote Explosion** | `WeaponOptions::AirStrike` | **przetestowana offline** | `NX_ADD_EXPLOSION` triggers high-yield blimp-scale explosion 18m ahead of player. |
| **Teleport Gun (Impact Warp)** | `WeaponOptions::TeleportGun` | **przetestowana offline** | Probes `NX_GET_PED_LAST_WEAPON_IMPACT_COORD` on weapon discharge and warps player to impact point. |
| **Explosion Gun (Impact Blast)**| `WeaponOptions::ExplosiveGun`| **przetestowana offline** | Probes bullet impact coordinates via `NX_GET_PED_LAST_WEAPON_IMPACT_COORD` and spawns cinematic high-yield explosions. |

### Category: World Options
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Pause Clock** | `TimeOptions::PauseClock` | **przetestowana offline** | Native `NX_PAUSE_CLOCK(clockPaused)` freezes in-game daytime progression. |
| **Time Presets** | `TimeOptions::SetHour` | **przetestowana offline** | `NX_SET_CLOCK_TIME(hour, 0, 0)` sets canonical hours (8, 12, 18, 0). |
| **Weather Presets (7 types)**| `WeatherOptions::SetWeather` | **przetestowana offline** | `NX_SET_WEATHER_TYPE_NOW_PERSIST` (EXTRASUNNY, CLEAR, CLOUDS, RAIN, THUNDER, FOGGY, XMAS). |
| **Reset Dynamic Weather** | `WeatherOptions::Reset` | **przetestowana offline** | `NX_CLEAR_WEATHER_TYPE_PERSIST()` returns weather control to native story cycle. |
| **Moon / Low Gravity Toggle** | `WorldOptions::MoonGravity` | **przetestowana offline** | `NX_SET_GRAVITY_LEVEL(lowGravity ? 1 : 0)`. |
| **Clear Peds in Area** | `WorldOptions::ClearAreaPeds` | **przetestowana offline** | `NX_CLEAR_AREA_OF_PEDS(x, y, z, 200.0f, 1)`. |
| **Clear Vehicles in Area** | `WorldOptions::ClearAreaVehicles`| **przetestowana offline** | `NX_CLEAR_AREA_OF_VEHICLES(x, y, z, 200.0f, false, false, false, false, false, false, 0)`. |
| **Clear Cops in Area** | `WorldOptions::ClearAreaCops` | **przetestowana offline** | `NX_CLEAR_AREA_OF_COPS(x, y, z, 200.0f, 0)`. |
| **City Blackout Toggle** | `WorldOptions::Blackout` | **przetestowana offline** | `NX_SET_ARTIFICIAL_LIGHTS_STATE(blackout)` toggles city grid lighting. |
| **Game Speed / Slow Motion** | `WorldOptions::GameSpeed` | **przetestowana offline** | `NX_SET_TIME_SCALE(1.0f / 0.5f / 0.2f)`. |
| **Riot Mode (Chaos Mode)** | `Misc::RiotMode` | **przetestowana offline** | Native `NX_SET_RIOT_MODE_ENABLED` incites armed pedestrian riots across Los Santos. |
| **Bullet Time on Aim (Slowmo)**| `WorldOptions::BulletTimeOnAim`| **przetestowana offline** | Detects aim control (25 / `INPUT_AIM`) and dynamically slows game engine to 0.2x speed, reverting upon release. |

### Category: Vehicle Customs
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Neon Underglow (4 sides)** | `VehicleModShop::NeonLights` | **przetestowana offline** | Loops `NX_SET_VEHICLE_NEON_ENABLED(v, 0..3, on)` for left, right, front, back. |
| **Neon Colors (8 presets)** | `VehicleModShop::NeonColours` | **przetestowana offline** | `NX_SET_VEHICLE_NEON_COLOUR(v, r, g, b)` (White, Blue, Cyan, Mint, Yellow, Pink, Red, Purple). |
| **Cycle Vehicle Extras** | `VehicleModShop::Extras` | **przetestowana offline** | `NX_DOES_EXTRA_EXIST` + `NX_SET_VEHICLE_EXTRA(v, id, 0)` toggles attached cosmetic extras. |
| **Window Tint (6 levels)** | `VehicleModShop::WindowTint` | **przetestowana offline** | `NX_SET_VEHICLE_WINDOW_TINT(v, 0..5)` (None, Pure Black, Dark Smoke, Light Smoke, Stock, Limo). |
| **Wheel Type Selector** | `VehicleModShop::WheelType` | **przetestowana offline** | `NX_SET_VEHICLE_WHEEL_TYPE(v, 0..6)` (Sport, Muscle, Lowrider, SUV, Offroad, Tuner, Bike). |
| **Custom RGB Respray** | `VehicleModShop::CustomPaint` | **przetestowana offline** | `NX_SET_VEHICLE_CUSTOM_PRIMARY_COLOUR` & `SECONDARY` (Gold, Red, Blue, Green, Deep Black). |
| **Rainbow Paint (RGB Cycle)** | `VehicleModShop::RainbowPaint` | **przetestowana offline** | Transitions through 6-phase RGB cycle each tick, updating primary & secondary custom colors. |

### Category: Player Appearance
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Model Changer: Story Peds** | `PlayerAppearance::ModelChanger` | **przetestowana offline** | Streams & assigns Michael (`0x0D7114C9`), Franklin (`0x9B22DBAF`), Trevor (`0x9B810FA2`) via `NX_SET_PLAYER_MODEL`. |
| **Model Changer: Multiplayer** | `PlayerAppearance::ModelChanger` | **przetestowana offline** | Streams & assigns MP Male (`0x705E61F2`), MP Female (`0x9C9EFFD8`). |
| **Reset Default Outfit** | `PlayerAppearance::ResetVariation` | **przetestowana offline** | `NX_SET_PED_DEFAULT_COMPONENT_VARIATION(ped)`. |
| **Cycle Torso / Clothes** | `PlayerAppearance::Components` | **przetestowana offline** | Probes `NX_GET_NUMBER_OF_PED_DRAWABLE_VARIATIONS` & applies `NX_SET_PED_COMPONENT_VARIATION(ped, 3, drawable, 0, 0)`. |
| **Cycle Legs / Pants** | `PlayerAppearance::Components` | **przetestowana offline** | Cycles component 4 drawables safely within variation bounds. |

### Category: Animations & Scenarios
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Scenario: Smoke Cigarette** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_SMOKING", 0, true)`. |
| **Scenario: Drink Coffee** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_DRINKING", 0, true)`. |
| **Scenario: Cheer** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_CHEERING", 0, true)`. |
| **Scenario: Muscle Flex** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_MUSCLE_FLEX", 0, true)`. |
| **Scenario: Binoculars** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_BINOCULARS", 0, true)`. |
| **Scenario: Push-ups** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_PUSH_UPS", 0, true)`. |
| **Scenario: Sit-ups** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_SIT_UPS", 0, true)`. |
| **Scenario: Guard Stand** | `Animations::Scenarios` | **przetestowana offline** | `NX_TASK_START_SCENARIO_IN_PLACE(ped, "WORLD_HUMAN_GUARD_STAND", 0, true)`. |
| **Stop Animation / Clear Tasks**| `Animations::ClearTasks` | **przetestowana offline** | `NX_CLEAR_PED_TASKS(ped)` immediately cancels current scenario/animation. |

### Category: Entity Manager / Object Spooner
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Spawn Prop: Road Cone** | `ObjectSpooner::Spawn` | **przetestowana offline** | Streams model `prop_roadcone02a` (`0xC2339364`) and creates via `NX_CREATE_OBJECT`. |
| **Spawn Prop: Work Barrier** | `ObjectSpooner::Spawn` | **przetestowana offline** | Streams model `prop_barrier_work05` (`0xF7752D66`) in front of player. |
| **Spawn Prop: Stunt Ramp** | `ObjectSpooner::Spawn` | **przetestowana offline** | Streams model `prop_mp_ramp_01` (`0xB157C9E4`). |
| **Spawn Prop: Wood Box** | `ObjectSpooner::Spawn` | **przetestowana offline** | Streams model `prop_box_wood02a_pu` (`0x9109DFBC`). |
| **Attach Object to Player** | `ObjectSpooner::Attachment` | **przetestowana offline** | `NX_ATTACH_ENTITY_TO_ENTITY(object, ped, 0, 0.0, 1.5, 0.2, ...)`. |
| **Freeze Object Position** | `ObjectSpooner::FreezePosition` | **przetestowana offline** | `NX_FREEZE_ENTITY_POSITION(lastObject, toggle)` locks prop rigidly in 3D world. |
| **Delete Spawned Object** | `ObjectSpooner::Delete` | **przetestowana offline** | `NX_DELETE_OBJECT(&lastObject)` safely cleans up entity handle and frees memory. |

### Category: Menu Navigation & System
| Feature | Menyoo Upstream Equivalent | NX Port Status | Implementation & Native Details |
|---|---|---|---|
| **Controller Activation** | Gamepad shortcut | **działa live** | Cover (R / 44) + Context (D-pad Right / 38) or Cover (R / 44) + D-pad Left (166). |
| **12-Submenu Hierarchy** | Menyoo menu tree | **przetestowana offline** | Main (0), Player (1), Vehicle (2), Spawner (3), Teleport (4), Weapons (5), World (6), Customs (7), Appearance (8), Animations (9), Spooner (10), Settings (11). |
| **D-pad Navigation** | Menu directional controls | **działa live** | Discrete frontend inputs (164=Down, 165=Up, 166=Left, 167=Right). |
| **A (Select) / B (Back/Cancel)** | Menu confirm / cancel | **działa live** | Discrete frontend inputs (177=Accept/Select, 178=Cancel/Back). |
| **Delayed Key Repeat** | Input repeater loop | **przetestowana offline** | 350ms initial delay, 140ms continuous repeat rate for rapid list navigation. |
| **Zero Interference When Closed** | Menu passive mode | **działa live** | Does not intercept or disable any game controls when menu is closed. |
| **Pause / Fade Yielding** | Game menu detection | **przetestowana offline** | `NX_IS_PAUSE_MENU_ACTIVE()`, `NX_IS_SCREEN_FADED_OUT()`, `NX_IS_SCREEN_FADING_OUT()` suppress overlay and release controls. |
| **Graceful Stop & RAM Restore** | Trainer exit routine | **działa live** | Cleans up effects, unpauses clock, resets weather, deletes spooned entities, restores original `cheat_controller` bytes. |
| **Network / LSO Compatibility**| Separate LSO commands | **działa live** | Mailbox commands 8 & 9 and symbols `network*` preserved unchanged. |

---

## 2. Subsequent Stages Roadmap

| Subsystem | Planned Stage | Status | Blockers / Requirements |
|---|---|---|---|
| **Advanced Vehicle Customs** | Stage 2 | **przetestowana offline** | Neons, Extras, Tints, Wheels, Custom RGB implemented. |
| **Player Appearance & Peds** | Stage 2 | **przetestowana offline** | Story/MP peds, component cycling, outfit reset implemented. |
| **Animations & Scenarios** | Stage 2 | **przetestowana offline** | 8 world scenarios, task clearing implemented. |
| **Basic Object Spooner** | Stage 2 | **przetestowana offline** | Prop spawning, attach, freeze, delete implemented. |
| **Complex Raycast Spooner** | Stage 3 | `aktualnie niedostępna` | 3D cursor placement, camera manipulation in script VM. |
| **Persistent XML/Config Save** | Stage 4 | `wymaga adaptera` | Switch title storage filesystem access not available from pure script bytecode. |
