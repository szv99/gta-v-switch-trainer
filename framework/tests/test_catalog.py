import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from catalog import CatalogError, load_catalog, validate_catalog


class CatalogTests(unittest.TestCase):
    def test_checked_in_catalog_has_nine_entries_and_two_tested(self):
        catalog = load_catalog()
        self.assertEqual(len(catalog["vehicles"]), 9)
        tested = [v["name"] for v in catalog["vehicles"] if v["runtime"]["availability"] == "tested"]
        self.assertEqual(tested, ["adder", "sultan"])

    def test_duplicate_name_is_rejected(self):
        catalog = load_catalog()
        catalog["vehicles"].append(dict(catalog["vehicles"][0], id="vehicle.adder-copy"))
        with self.assertRaisesRegex(CatalogError, "duplicate vehicle name"):
            validate_catalog(catalog)

    def test_duplicate_id_is_rejected_even_with_other_name(self):
        catalog = load_catalog()
        duplicate = dict(catalog["vehicles"][1], name="another")
        catalog["vehicles"].append(duplicate)
        with self.assertRaisesRegex(CatalogError, "duplicate vehicle id"):
            validate_catalog(catalog)

    def test_lowercase_category_and_stable_id_are_checked(self):
        catalog = load_catalog()
        catalog["vehicles"][0]["name"] = "Adder"
        with self.assertRaises(CatalogError):
            validate_catalog(catalog)
        catalog = load_catalog()
        catalog["vehicles"][0]["id"] = "adder"
        with self.assertRaisesRegex(CatalogError, "stable id"):
            validate_catalog(catalog)

    def test_cli_rejects_malformed_json(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            path.write_text(json.dumps({"schema_version": 1, "vehicles": [{"name": "adder"}]}), encoding="utf-8")
            checker = Path(__file__).resolve().parents[1] / "tools" / "check_catalog.py"
            result = subprocess.run([sys.executable, str(checker), str(path)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing id", result.stderr)


if __name__ == "__main__":
    unittest.main()
