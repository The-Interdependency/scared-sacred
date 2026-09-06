# ratios: loc_comments=16:6 imports_exports=4:1 calls_definitions=7:2
"""Checks that generated Fifty-Three Days assets stay in the base-game set.

# === CHECKS ===
# id: check_export_namespace
#   witnesses: cards_export_v01
# === END CHECKS ===
"""
import tempfile
import unittest
from pathlib import Path

import cards_export


class Checks(unittest.TestCase):

    def test_check_export_namespace(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            idx = cards_export.export(str(root))
            base = root / "base-game" / "sets" / "fifty-three-days" / "cards"
            wrong = root / "expansions" / "scared-sacred" / "cards"
            self.assertEqual(len(idx["cards"]), 87)
            self.assertTrue((base / "index.json").is_file())
            self.assertFalse(wrong.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=16:6 imports_exports=4:1 calls_definitions=7:2
