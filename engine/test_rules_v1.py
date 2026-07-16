# ratios: loc_comments=61:14 imports_exports=4:2 calls_definitions=38:7
"""Checks for rules_v1 + runner v0.2 hooks. Run: python3 test_rules_v1.py

# === CHECKS ===
# id: check_gate_a_minus_m
#   witnesses: rules_gate_a_minus_m
# id: check_discard_budget
#   witnesses: rules_discard_budget
# id: check_interference_priced
#   witnesses: rules_interference_priced, runner_interference_passthrough
# id: check_coalition_window
#   witnesses: rules_coalition_window, runner_rotation_boundary_hooks
# id: check_reclaims_gated
#   witnesses: rules_reclaims_gated
# === END CHECKS ===
"""
import unittest

import politics_runner as pr
from inertial_engine import InertialEngine, Person
from rules_v1 import RulesV1


def state(e=0, m=1):
    return pr.GameState(population=100, e=e, m=m)


class Checks(unittest.TestCase):

    def test_check_gate_a_minus_m(self):
        r = RulesV1()
        strike = {"kind": "action", "a": 7, "r": 4}
        self.assertFalse(r.legal(state(e=5, m=1), strike))   # 5 < 7-1
        self.assertTrue(r.legal(state(e=6, m=1), strike))    # 6 >= 6
        self.assertTrue(r.legal(state(e=3, m=4), strike))    # coalition catalyst
        self.assertTrue(r.legal(state(e=5, m=1),
                                dict(strike, burn=1)))       # reach discard

    def test_check_discard_budget(self):
        r = RulesV1()
        plays = pr.TurnPlays(actions=[{"kind": "action", "a": 0, "r": 1},
                                      {"kind": "action", "a": 0, "r": 1},
                                      {"kind": "action", "a": 0, "r": 1}],
                             discards=1)
        r.validate_turn(state(), plays)
        self.assertEqual(len(plays.actions), 2)   # 1 free + 1 tempo discard

    def test_check_interference_priced(self):
        eng = InertialEngine([Person(x=-0.5, v=0, m=2.0)
                              for _ in range(100)])

        class Knife:
            def __init__(self):
                self.done = False
            def take_turn(self, s, pid):
                if self.done:
                    return pr.TurnPlays()
                self.done = True
                return pr.TurnPlays(actions=[{"kind": "action", "a": 3,
                                              "r": 0, "target": "player"}])
        st = state(e=4, m=2)
        runner = pr.MatchRunner(eng, pr.ScriptedMachine(
            [{"name": "M01", "s": 0}] * 3), [Knife()], st, rules=RulesV1())
        runner.run()
        knife_beats = [ev for ev in st.log if ev[0] == "action"]
        self.assertTrue(knife_beats)              # it resolved, attributed
        self.assertLessEqual(st.m, 2 - 1 + 1)     # m paid (coalition may swing)

    def test_check_coalition_window(self):
        r = RulesV1()
        self.assertEqual(r.coalition(["M07", "M07", "M03"]), 1)
        self.assertEqual(r.coalition(["M07", "M03", None]), -1)
        self.assertEqual(r.coalition([None, None]), -1)

    def test_check_reclaims_gated(self):
        r = RulesV1()
        s = state()
        self.assertEqual(r.rotation_effects(s)["reclaim"], 0)
        s.in_play_statics.append({"name": "EXILE NETWORK", "reclaims": True})
        self.assertEqual(r.rotation_effects(s)["reclaim"], 1)
        eng = InertialEngine([Person(x=1.3, v=0, m=1, converted=True),
                              Person(x=1.1, v=0, m=1, converted=True)])
        eng.reclaim(s, 1)
        self.assertEqual(sum(p.converted for p in eng.persons), 1)
        reclaimed = [p for p in eng.persons if not p.converted][0]
        self.assertAlmostEqual(reclaimed.x, 0.95)  # nearest threshold first


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=61:14 imports_exports=4:2 calls_definitions=38:7
