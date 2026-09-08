"""Checks for PLAN.md architecture ambiguity closures.

# === CHECKS ===
# id: check_plan_preserves_repository_name_ruling
#   witnesses: tiwcg_plan_repository_identity
# id: check_plan_defines_drop_two_shortfall
#   witnesses: tiwcg_plan_drop_two_shortfall
# id: check_plan_keeps_witness_constraints_base_wide
#   witnesses: tiwcg_plan_witness_base_wide
# id: check_plan_records_versioned_draw_source
#   witnesses: tiwcg_plan_draw_replay_provenance
# id: check_plan_routes_named_human_cards_through_pipeline
#   witnesses: tiwcg_plan_named_human_pipeline
# id: check_plan_excludes_witness_departure_logging
#   witnesses: tiwcg_plan_witness_departure_exception
# id: check_plan_keeps_learning_confidence_observable
#   witnesses: tiwcg_plan_learning_observable_only
# id: check_plan_preserves_event_art_content_boundary
#   witnesses: tiwcg_plan_event_art_boundary
# id: check_plan_prohibits_paid_competitive_advantage
#   witnesses: tiwcg_plan_paid_power_boundary
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

    def test_check_plan_records_versioned_draw_source(self):
        self.assertIn("versioned skill-lib draw source", PLAN)
        self.assertIn("immutable skill-lib content hash or repository revision", PLAN)
        self.assertIn("Persist the skill-lib source revision or content hash", PLAN)

    def test_check_plan_routes_named_human_cards_through_pipeline(self):
        self.assertIn("Named-figure cards are generated from public transcripts", BASE_CANON)
        self.assertIn("Generic creation does not authorize hand-authored named-human", PLAN)
        self.assertIn("public-transcript EDCM pipeline", PLAN)

    def test_check_plan_excludes_witness_departure_logging(self):
        self.assertIn("departures free, unmarked, unremarked", BASE_CANON)
        self.assertIn("Witness contexts are an explicit exception", PLAN)
        self.assertIn("must not emit or retain", PLAN)

    def test_check_plan_keeps_learning_confidence_observable(self):
        self.assertIn("No internal states anywhere", BASE_CANON)
        self.assertIn("externally observed learning records", PLAN)
        self.assertIn("provenance-backed calibration/confidence metrics", PLAN)
        self.assertIn("without rewriting the canonical card definition or inferring an internal state", PLAN)

    def test_check_plan_preserves_event_art_content_boundary(self):
        self.assertIn("Victims are never depicted on event cards", BASE_CANON)
        self.assertIn("art must not depict victims", PLAN)
        self.assertIn("documented actor behavior", PLAN)

    def test_check_plan_prohibits_paid_competitive_advantage(self):
        self.assertIn("must not grant territory, combat, resource, timing", PLAN)
        self.assertIn("other mechanical/competitive advantage", PLAN)
        self.assertIn("does not grant paid mechanical or competitive advantage", PLAN)


if __name__ == "__main__":
    unittest.main(verbosity=2)
