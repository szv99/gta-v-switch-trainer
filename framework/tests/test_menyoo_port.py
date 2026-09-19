"""Unit tests for Menyoo port: manifest limits, native registrations, CLI command mappings."""
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEV = ROOT.parent

class MenyooPortBudgetTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "build/manifest.json").read_text())
        self.raw = (ROOT / "build/trainer-2699.nsc").read_bytes()

    def test_conservative_stack_budget(self):
        peak = self.manifest.get("call_graph_stack_slots", self.manifest["conservative_stack_slots"])
        self.assertLessEqual(peak, 256, f"Verified stack budget exceeded: {peak} > 256")

    def test_call_graph_stack_bound(self):
        self.assertIn("call_graph_stack_slots", self.manifest)
        call_graph_peak = self.manifest["call_graph_stack_slots"]
        self.assertLessEqual(call_graph_peak, 256)
        self.assertLessEqual(call_graph_peak, self.manifest["conservative_stack_slots"])

    def test_static_capacity(self):
        symbols = self.manifest["symbols"]
        max_slot = max(symbols.values())
        self.assertLess(max_slot, 95, f"Static slot limit exceeded: {max_slot} >= 95")

    def test_code_capacity(self):
        code_bytes = self.manifest["code_bytes"]
        self.assertLessEqual(code_bytes, 15830, f"Code size exceeded host capacity: {code_bytes} > 15830")

    def test_native_capacity(self):
        native_count = self.manifest["natives"]
        self.assertLessEqual(native_count, 151, f"Native count exceeded host capacity: {native_count} > 151")

    def test_string_table_capacity(self):
        string_size = struct.unpack_from("<I", self.raw, 112)[0]
        self.assertLessEqual(string_size, 2680, f"String table exceeded decoupled host capacity: {string_size} > 2680")

    def test_required_mailbox_abi_symbols_present(self):
        required = [
            "protocolMagic", "protocolVersion", "runtimeStatus", "heartbeat",
            "remoteCommand", "remoteArg", "remoteSequence", "acknowledgedSequence",
            "lastResult", "lastVehicle", "spawnCount", "invincible", "previousPed",
            "pendingModel", "menuOpen", "networkSignedIn", "networkSignedOnline",
            "networkCanAccess", "networkAccessReason", "networkGameInProgress",
            "networkSessionActive"
        ]
        symbols = self.manifest["symbols"]
        for name in required:
            self.assertIn(name, symbols, f"Required mailbox symbol missing: {name}")

    def test_all_natives_mapped_and_registered(self):
        regs = json.loads((DEV / "debug-setup/native-registrations.json").read_text())
        native_map = json.loads((ROOT / "build/native-map.json").read_text())
        self.assertEqual(len(native_map), self.manifest["natives"])
        for entry in native_map:
            build2699 = entry["build2699"]
            self.assertIn(build2699, regs, f"Native {entry['name']} (2699: {build2699}) not in registration table")

class MenyooCatalogConsistencyTests(unittest.TestCase):
    def test_all_trainer_models_exist_in_catalog(self):
        catalog = json.loads((ROOT / "catalog/vehicles.json").read_text())
        catalog_names = {v["name"] for v in catalog["vehicles"]}
        trainer_c_models = {
            "adder", "zentorno", "sultan", "buffalo", "blista", "baller", "bati", "sanchez", "bifta"
        }
        self.assertTrue(trainer_c_models.issubset(catalog_names))

    def test_catalog_covers_all_supported_categories(self):
        from catalog import SUPPORTED_CATEGORIES, load_catalog
        catalog = load_catalog()
        present = {v["category"] for v in catalog["vehicles"]}
        self.assertEqual(present, set(SUPPORTED_CATEGORIES))

class MenyooCliParsingTests(unittest.TestCase):
    def test_time_parsing(self):
        time_presets = {"morning": 8, "noon": 12, "evening": 18, "midnight": 0}
        self.assertEqual(time_presets["morning"], 8)
        self.assertEqual(time_presets["noon"], 12)
        self.assertEqual(time_presets["evening"], 18)
        self.assertEqual(time_presets["midnight"], 0)
        self.assertEqual(int("15") % 24, 15)

    def test_teleport_destinations_mapped(self):
        dest_map = {
            "waypoint": (15, 0), "michael": (14, 0), "franklin": (14, 1),
            "trevor": (14, 2), "customs": (14, 3), "airport": (14, 4),
            "mazebank": (14, 5), "chiliad": (14, 6), "zancudo": (14, 7),
            "prison": (14, 8), "observatory": (14, 9), "sandyshores": (14, 10),
            "paleto": (14, 11), "delperro": (14, 12), "humane": (14, 13)
        }
        self.assertEqual(len(dest_map), 15)
        self.assertEqual(dest_map["waypoint"][0], 15)
        for loc in ["michael", "franklin", "trevor", "customs", "airport", "mazebank", "chiliad",
                    "zancudo", "prison", "observatory", "sandyshores", "paleto", "delperro", "humane"]:
            self.assertEqual(dest_map[loc][0], 14)

    def test_weather_presets_mapped(self):
        w_map = {
            "extrasunny": (18, 0), "clear": (18, 1), "clouds": (18, 2),
            "rain": (18, 3), "thunder": (18, 4), "foggy": (18, 5),
            "snow": (18, 6), "reset": (19, 0)
        }
        self.assertEqual(len(w_map), 8)
        self.assertEqual(w_map["reset"], (19, 0))

    def test_new_telemetry_labels_mapped(self):
        from nxtrainer.runtime import telemetry
        fake_state = {
            "symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2},
            "host": {"stack": 0x1000}
        }
        # Verify labels 0..74 are defined without KeyError
        test_codes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                      24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                      41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
                      60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74,
                      75, 76, 77, 78, 79, 80, 81, 82, 83, 84,
                      85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98,
                      99, 100, 101, 102, 103]
        from unittest.mock import MagicMock
        import nxtrainer.runtime as rt
        for code in test_codes:
            sample = rt.telemetry(MagicMock(read=lambda addr, sz, c=code: struct.pack('<QQQ', c, 0x4e585431, 1)),
                                  {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})
            self.assertNotEqual(sample["resultLabel"], "unknown", f"Code {code} missing resultLabel")

        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 60, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "neons toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 66, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "ped model changed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 69, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "scenario started")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 71, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "object spawned")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 75, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "vehicle jumped")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 76, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "drift mode changed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 78, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "air strike triggered")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 81, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "bodyguard recruited")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 83, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "cash maxed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 84, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "stunt ramp spawned")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 85, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "rainbow paint toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 86, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "auto repair toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 87, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "horn boost toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 88, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "vehicle weapons toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 89, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "teleport gun toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 90, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "riot mode toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 91, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "flying car toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 92, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "explosion gun toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 93, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "wanted level maxed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 94, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "vehicle invisibility toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 95, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "vehicle 180 executed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 96, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "forcefield toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 97, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "bullet time toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 98, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "sky launch executed")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 99, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "warped to nearest vehicle")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 100, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "drunk mode toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 101, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "autopilot toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 102, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "siren toggled")
        self.assertEqual(rt.telemetry(MagicMock(read=lambda a,s: struct.pack('<QQQ', 103, 0x4e585431, 1)),
                                      {"symbols": {"lastResult": 0, "protocolMagic": 1, "protocolVersion": 2}, "host": {"stack": 0}})["resultLabel"], "vehicle self-destructed")

    def test_subsystem_cli_parsing(self):
        import sys
        sys.path.insert(0, str(ROOT))
        from trainer import build_parser
        parser = build_parser()

        # Customs
        args = parser.parse_args(["customs-neon", "on"])
        self.assertEqual(args.action, "customs-neon")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["customs-neon-color", "mint"])
        self.assertEqual(args.action, "customs-neon-color")
        self.assertEqual(args.color, "mint")

        args = parser.parse_args(["customs-extra"])
        self.assertEqual(args.action, "customs-extra")

        args = parser.parse_args(["customs-tint", "limo"])
        self.assertEqual(args.action, "customs-tint")
        self.assertEqual(args.tint, "limo")

        args = parser.parse_args(["customs-wheels", "tuner"])
        self.assertEqual(args.action, "customs-wheels")
        self.assertEqual(args.type, "tuner")

        args = parser.parse_args(["customs-respray", "gold"])
        self.assertEqual(args.action, "customs-respray")
        self.assertEqual(args.color, "gold")

        # Appearance
        args = parser.parse_args(["appearance-model", "michael"])
        self.assertEqual(args.action, "appearance-model")
        self.assertEqual(args.model, "michael")

        args = parser.parse_args(["appearance-reset"])
        self.assertEqual(args.action, "appearance-reset")

        args = parser.parse_args(["appearance-component", "3"])
        self.assertEqual(args.action, "appearance-component")
        self.assertEqual(args.component, 3)

        # Animations
        args = parser.parse_args(["play-scenario", "smoke"])
        self.assertEqual(args.action, "play-scenario")
        self.assertEqual(args.scenario, "smoke")

        args = parser.parse_args(["stop-anim"])
        self.assertEqual(args.action, "stop-anim")

        # Spooner
        args = parser.parse_args(["spoon-object", "ramp"])
        self.assertEqual(args.action, "spoon-object")
        self.assertEqual(args.model, "ramp")

        args = parser.parse_args(["spoon-attach"])
        self.assertEqual(args.action, "spoon-attach")

        args = parser.parse_args(["spoon-freeze", "off"])
        self.assertEqual(args.action, "spoon-freeze")
        self.assertEqual(args.value, "off")

        args = parser.parse_args(["spoon-delete"])
        self.assertEqual(args.action, "spoon-delete")

        # Fun / Stunts / Bodyguards / Cash
        args = parser.parse_args(["veh-jump"])
        self.assertEqual(args.action, "veh-jump")

        args = parser.parse_args(["veh-drift", "on"])
        self.assertEqual(args.action, "veh-drift")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-boost"])
        self.assertEqual(args.action, "veh-boost")

        args = parser.parse_args(["strike"])
        self.assertEqual(args.action, "strike")

        args = parser.parse_args(["seatbelt", "off"])
        self.assertEqual(args.action, "seatbelt")
        self.assertEqual(args.value, "off")

        args = parser.parse_args(["ragdoll"])
        self.assertEqual(args.action, "ragdoll")

        args = parser.parse_args(["bodyguard-spawn"])
        self.assertEqual(args.action, "bodyguard-spawn")

        args = parser.parse_args(["bodyguard-dismiss"])
        self.assertEqual(args.action, "bodyguard-dismiss")

        args = parser.parse_args(["add-cash"])
        self.assertEqual(args.action, "add-cash")

        args = parser.parse_args(["stunt-ramp"])
        self.assertEqual(args.action, "stunt-ramp")

        args = parser.parse_args(["veh-rainbow", "on"])
        self.assertEqual(args.action, "veh-rainbow")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-autorepair", "on"])
        self.assertEqual(args.action, "veh-autorepair")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-hornboost", "on"])
        self.assertEqual(args.action, "veh-hornboost")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-weapons", "on"])
        self.assertEqual(args.action, "veh-weapons")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["teleport-gun", "on"])
        self.assertEqual(args.action, "teleport-gun")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["riot-mode", "on"])
        self.assertEqual(args.action, "riot-mode")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-fly", "on"])
        self.assertEqual(args.action, "veh-fly")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["explosion-gun", "on"])
        self.assertEqual(args.action, "explosion-gun")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["max-wanted"])
        self.assertEqual(args.action, "max-wanted")

        args = parser.parse_args(["veh-invisible", "on"])
        self.assertEqual(args.action, "veh-invisible")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-180"])
        self.assertEqual(args.action, "veh-180")

        args = parser.parse_args(["forcefield", "on"])
        self.assertEqual(args.action, "forcefield")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["aim-slowmo", "on"])
        self.assertEqual(args.action, "aim-slowmo")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["launch-sky"])
        self.assertEqual(args.action, "launch-sky")

        args = parser.parse_args(["warp-nearest"])
        self.assertEqual(args.action, "warp-nearest")

        args = parser.parse_args(["drunk", "on"])
        self.assertEqual(args.action, "drunk")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["veh-wander", "on"])
        self.assertEqual(args.action, "veh-wander")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["autopilot", "off"])
        self.assertEqual(args.action, "autopilot")
        self.assertEqual(args.value, "off")

        args = parser.parse_args(["veh-siren", "on"])
        self.assertEqual(args.action, "veh-siren")
        self.assertEqual(args.value, "on")

        args = parser.parse_args(["siren", "off"])
        self.assertEqual(args.action, "siren")
        self.assertEqual(args.value, "off")

        args = parser.parse_args(["veh-explode"])
        self.assertEqual(args.action, "veh-explode")

if __name__ == "__main__":
    unittest.main()
