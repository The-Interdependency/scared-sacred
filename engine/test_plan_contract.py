"""Checks for PLAN.md architecture ambiguity closures.

# === CHECKS ===
# id: check_plan_preserves_repository_name_ruling
#   witnesses: tiwcg_plan_repository_identity
# id: check_plan_defines_drop_two_shortfall
#   witnesses: tiwcg_plan_drop_two_shortfall
# id: check_plan_keeps_witness_constraints_base_wide
#   witnesses: tiwcg_plan_witness_base_wide
# === END CHECKS ===
"""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLAN = (ROOT / "PLAN.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
BASE_CANON = (ROOT / "canon" / "canon_v03_base.md").read_text(encoding="utf-8")


class PlanContractChecks(unittest.TestCase):

    def test_check_plan_preserves_repository_name_ruling(self):
        self.assertIn("Repo retains the name scared-sacred", BASE_CANON)
        self.assertIn("does not rename the Git repository", PLAN)
        self.assertIn("repository-name ruling", PLAN)
        self.assertIn("does not supersede", README)

    def test_check_plan_defines_drop_two_shortfall(self):
        self.assertIn("drop up to 2 resource-generation cards", PLAN)
        self.assertIn("drop all available", PLAN)
        self.assertIn("pass this step", PLAN)

    def test_check_plan_keeps_witness_constraints_base_wide(self):
        self.assertIn("The Witness Rule and the Litany are", BASE_CANON)
        self.assertIn("base-wide TIWCG canon", PLAN)
        self.assertIn("giver-owned, table-bound", PLAN)
        self.assertIn("unprintable, and unsellable", PLAN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
