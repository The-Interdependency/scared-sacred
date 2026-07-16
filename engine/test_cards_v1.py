# ratios: loc_comments=83:18 imports_exports=6:2 calls_definitions=54:9
"""Checks for cards_v1 + weimar_data. Run: python3 test_cards_v1.py

# === CHECKS ===
# id: check_data_integrity
#   witnesses: cards_deck_tier_law
# id: check_se_gated_by_e
#   witnesses: cards_se_gated_by_e
# id: check_se_doubles_at_low_m
#   witnesses: cards_se_doubles_at_low_m
# id: check_destruction_feeds_prereqs
#   witnesses: cards_destruction_feeds_prereqs
# id: check_courts_flip
#   witnesses: cards_courts_flip
# id: check_hinge_reprices
#   witnesses: cards_hinge_reprices
# id: check_full_match_runs
#   witnesses: cards_se_gated_by_e, runner_field_totals_delegation
# === END CHECKS ===
"""
import unittest

import politics_runner as pr
import weimar_data as wd
from cards_v1 import WeimarMachine, field_totals, validate_deck
from inertial_engine import InertialEngine, weimar_seed
from rules_v1 import RulesV1


def opening():
    st = pr.GameState(**wd.WEIMAR_OPENING)
    st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
    return st


class Checks(unittest.TestCase):

    def test_check_data_integrity(self):
        self.assertEqual(len(wd.MACHINE_SCRIPT), 40)
        ok, n = validate_deck(wd.RESPONSE_DECK)
        self.assertTrue(ok)
        self.assertEqual(n, 40)
        dates = [c["date"] for c in wd.MACHINE_SCRIPT]
        self.assertEqual(dates, sorted(dates))          # history is ordered
        self.assertFalse(validate_deck([{"copies": 39}])[0])
        self.assertFalse(validate_deck([{"copies": 100}])[0])

    def test_check_se_gated_by_e(self):
        m = WeimarMachine([wd.MACHINE_SCRIPT[6], wd.MACHINE_SCRIPT[7]])  # M07,M08
        st = opening(); st.e = 2                         # below A_SE 5
        c = m.next_card(st)
        m.resolve_se(c, st)                              # window closed, uncountered
        self.assertNotIn("next", m.chain_queue)          # gated: no chain
        self.assertTrue(m.delayed)                       # ...but delayed, armed
        st.e = 6
        m.next_card(st)                                  # next beat: fires
        self.assertFalse(m.delayed)

    def test_check_se_doubles_at_low_m(self):
        card = {"id": "T", "name": "T", "s": 0,
                "se": {"a_se": 0, "kind": "perm_debuff",
                       "target": "THE PULPITS", "amount": 1}}
        for m_val, expect in ((1, 2), (3, 1)):
            m = WeimarMachine([card])
            st = opening(); st.m = m_val
            st.in_play_statics.append({"name": "THE PULPITS", "passive_r": 1})
            m.resolve_se(m.next_card(st), st)
            pulpits = [s for s in st.in_play_statics
                       if s.get("name") == "THE PULPITS"][0]
            self.assertEqual(pulpits["perm_debuff"], expect)

    def test_check_destruction_feeds_prereqs(self):
        m = WeimarMachine(wd.MACHINE_SCRIPT)
        m.destroy("M35")                                 # Marburg never spoken
        st = opening(); st.e = 0
        skipped = []
        card = m.next_card(st)
        while card:
            card = m.next_card(st)
        skipped = [ev[1] for ev in st.log if ev[0] == "machine_skip"]
        self.assertIn("M36", skipped)                    # no speech, no purge card

    def test_check_courts_flip(self):
        m17 = [c for c in wd.MACHINE_SCRIPT if c["id"] == "M17"]
        m = WeimarMachine(m17)
        st = opening(); st.e = 6; st.m = 3               # gate open, no doubling
        st.in_play_statics.append({"name": "THE COURTS", "passive_r": 1})
        ps_before, pr_before = field_totals(st)
        m.resolve_se(m.next_card(st), st)
        ps_after, pr_after = field_totals(st)
        self.assertEqual(pr_after, max(0, pr_before - 1))
        self.assertEqual(ps_after, ps_before + 1)        # the bench changed sides

    def test_check_hinge_reprices(self):
        script = [c for c in wd.MACHINE_SCRIPT if c["id"] in ("M15", "M16")]
        m = WeimarMachine(script)
        st = opening(); st.m = 3
        st.in_play_statics.append({"name": "THE COALITION VOTE"})
        c15 = m.next_card(st)
        self.assertEqual(c15["s"], 0)                    # the vote fails
        c16 = m.next_card(st)
        self.assertEqual(c16["s"], 1)                    # boycott repriced 2->1
        m2 = WeimarMachine(script)
        st2 = opening()                                  # m=1, no marker: history
        self.assertEqual(m2.next_card(st2)["s"], 3)

    def test_check_full_match_runs(self):
        eng = InertialEngine(weimar_seed(100, 157))
        r = pr.MatchRunner(eng, WeimarMachine(wd.MACHINE_SCRIPT),
                           [pr.NullPlayer()] * 3, opening(), rules=RulesV1())
        res = r.run()
        self.assertEqual(res.outcome, "loss")            # null play still loses
        self.assertGreater(res.machine_beats, 10)        # but not instantly


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=83:18 imports_exports=6:2 calls_definitions=54:9
