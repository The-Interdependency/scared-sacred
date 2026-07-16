# ratios: loc_comments=89:14 imports_exports=6:2 calls_definitions=47:8
"""Checks for reserve pile, reaction window, hand law. Run directly.

# === CHECKS ===
# id: check_reserve_replaces_skip
#   witnesses: cards_destruction_feeds_prereqs
# id: check_reflex_gate_uses_incoming
#   witnesses: rules_reflex_gate_uses_incoming
# id: check_counter_intercepts_se
#   witnesses: runner_reaction_window
# id: check_hand_law
#   witnesses: runner_hand_law
# id: check_wels_reflex_only_m15
#   witnesses: rules_reflex_gate_uses_incoming
# === END CHECKS ===
"""
import unittest

import politics_runner as pr
import weimar_data as wd
from cards_v1 import WeimarMachine, build_response_pile, field_totals
from inertial_engine import InertialEngine, weimar_seed
from rules_v1 import RulesV1


def _card(name):
    return dict([c for c in wd.RESPONSE_DECK if c["name"] == name][0])


def opening():
    st = pr.GameState(**wd.WEIMAR_OPENING)
    st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
    return st


class Checks(unittest.TestCase):

    def test_check_reserve_replaces_skip(self):
        m = WeimarMachine(wd.MACHINE_SCRIPT, reserve=wd.RESERVE_PILE)
        m.destroy("M35")
        st = opening()
        played = []
        c = m.next_card(st)
        while c:
            played.append(c["id"])
            c = m.next_card(st)
        self.assertEqual(len(played), 40)               # tempo never lost
        self.assertIn("K01", played)                    # the machine improvised
        self.assertNotIn("M36", played)                 # the planned purge died

    def test_check_reflex_gate_uses_incoming(self):
        r = RulesV1()
        st = opening(); st.e = 0; st.m = 1
        sd = _card("STREET DEFENSE")                    # a3, reflex
        calm = {"id": "M04", "s": 0}
        fire = {"id": "M07", "s": 3}
        self.assertFalse(r.reflex_legal(st, sd, calm))  # 0+0 < 3-1
        self.assertTrue(r.reflex_legal(st, sd, fire))   # 0+3 >= 2

    def test_check_counter_intercepts_se(self):
        class Interceptor:
            def __init__(self): self.used = False
            def take_turn(self, state, pid): return pr.TurnPlays()
            def react(self, state, pid, mcard):
                if mcard.get("id") == "M17" and not self.used:
                    self.used = True
                    hand = state.hands[pid]
                    jc = [c for c in hand
                          if c["name"] == "JUDICIAL CHALLENGE"]
                    burn = [c for c in hand
                            if c["name"] != "JUDICIAL CHALLENGE"]
                    if jc and burn:
                        return jc[0], burn[0]
                return None
        st = opening()
        st.in_play_statics.append({"name": "THE COURTS", "passive_r": 1,
                                   "side": "player"})
        st.draw_pile = [_card("JUDICIAL CHALLENGE"), _card("THE LEAFLET RUN"),
                        _card("THE LEAFLET RUN")] + build_response_pile(7)
        st.e = 6
        m = WeimarMachine([c for c in wd.MACHINE_SCRIPT
                           if c["id"] in ("M17", "M16")])
        runner = pr.MatchRunner(InertialEngine(weimar_seed(100, 7)), m,
                                [Interceptor()], st, rules=RulesV1(),
                                hand_size=3)
        runner.run()
        self.assertIn(("se_countered", "M17"),
                      [ev for ev in st.log if ev[0] == "se_countered"])
        courts = [s for s in st.in_play_statics
                  if s.get("name") == "THE COURTS"][0]
        self.assertNotEqual(courts.get("side"), "machine")   # bench held

    def test_check_hand_law(self):
        class Fabricator:
            def take_turn(self, state, pid):
                return pr.TurnPlays(actions=[{"kind": "action", "a": 0,
                                              "r": 99,
                                              "name": "COUNTERFEIT"}])
        st = opening()
        st.draw_pile = build_response_pile(11)
        runner = pr.MatchRunner(InertialEngine(weimar_seed(100, 11)),
                                WeimarMachine(wd.MACHINE_SCRIPT[:4]),
                                [Fabricator()], st, rules=RulesV1(),
                                hand_size=5)
        runner.run()
        played = [ev for ev in st.log
                  if ev[0] == "action" and ev[2] == "COUNTERFEIT"]
        self.assertEqual(played, [])                    # not in hand: no play

    def test_check_wels_reflex_only_m15(self):
        r = RulesV1()
        st = opening(); st.e = 5; st.m = 1
        wels = _card("WELS' SPEECH")
        self.assertTrue(r.reflex_legal(st, wels, {"id": "M15", "s": 3}))
        self.assertFalse(r.reflex_legal(st, wels, {"id": "M16", "s": 2}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=89:14 imports_exports=6:2 calls_definitions=47:8
