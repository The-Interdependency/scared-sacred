# ratios: loc_comments=94:21 imports_exports=8:2 calls_definitions=54:10
"""Checks for arcana + agendas + habituation + reclaim pricing.

# === CHECKS ===
# id: check_agendas_verify_at_end
#   witnesses: agendas_verify_at_end
# id: check_organizer_counts_r
#   witnesses: agendas_organizer_counts_r
# id: check_arcana_once
#   witnesses: arcana_once_per_game
# id: check_wayseer
#   witnesses: arcana_wayseer_reveals
# id: check_filibuster
#   witnesses: arcana_filibuster_suspends, runner_suspension_primitive
# id: check_term_limits
#   witnesses: arcana_term_limits_oldest
# id: check_habituation
#   witnesses: rules_habituation_decay
# id: check_reclaim_priced
#   witnesses: rules_reclaim_priced
# === END CHECKS ===
"""
import random
import unittest

import politics_runner as pr
import weimar_data as wd
from arcana_agendas_v1 import ArcanaModule, deal_agendas, verify_agendas
from cards_v1 import WeimarMachine
from inertial_engine import InertialEngine, weimar_seed
from rules_v1 import RulesV1


def opening():
    st = pr.GameState(**wd.WEIMAR_OPENING)
    st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
    return st


class Checks(unittest.TestCase):

    def test_check_agendas_verify_at_end(self):
        st = opening()
        deal_agendas(st, 3, random.Random(9))
        eng = InertialEngine(weimar_seed(100, 9))
        res = pr.MatchRunner(eng, WeimarMachine(wd.MACHINE_SCRIPT),
                             [pr.NullPlayer()] * 3, st,
                             rules=RulesV1()).run()
        self.assertEqual(len(res.agenda_outcomes), 3)
        self.assertEqual(res.agenda_outcomes[0]["outcome"], "loss")
        # ashes-mode: THE MACHINE POLITICIAN can hold on a lost table
        for v in res.agenda_outcomes:
            if v["agenda"] == "THE MACHINE POLITICIAN":
                self.assertTrue(v["held"])       # m stayed at 1

    def test_check_organizer_counts_r(self):
        st = opening()
        st.tallies["agendas"] = [a for a in
                                 __import__("arcana_agendas_v1").AGENDAS
                                 if a["name"] == "THE ORGANIZER"] * 2
        st.log += [("action", 0, "X"), ("action", 0, "X"),
                   ("action", 1, "X")]
        v = verify_agendas(st, "win")
        self.assertTrue(v[0]["held"])            # pid 0 strictly greatest
        self.assertFalse(v[1]["held"])

    def test_check_arcana_once(self):
        st = opening()
        arc = ArcanaModule()
        m = WeimarMachine(wd.MACHINE_SCRIPT)
        arc.apply({"name": "THE WAYSEER"}, st, m, None, 0, 3)
        arc.apply({"name": "THE SCANDAL"}, st, m, None, 0, 3)
        kinds = [ev[0] for ev in st.log]
        self.assertIn("arcana_refused", kinds)

    def test_check_wayseer(self):
        st = opening()
        m0 = st.m
        arc = ArcanaModule()
        m = WeimarMachine(wd.MACHINE_SCRIPT)
        arc.apply({"name": "THE WAYSEER"}, st, m, None, 1, 3)
        reveal = [ev for ev in st.log if ev[0] == "wayseer_reveal"][0]
        self.assertEqual(len(reveal[1]), 6)      # 2 x P cards shown
        self.assertEqual(st.m, m0 + 1)
        self.assertEqual(m.cursor, 0)            # nothing consumed, nothing bent

    def test_check_filibuster(self):
        class Trump:
            def __init__(self): self.done = False
            def take_turn(self, state, pid):
                if not self.done:
                    self.done = True
                    return pr.TurnPlays(arcana={"name": "THE FILIBUSTER"})
                return pr.TurnPlays()
        st = opening()
        eng = InertialEngine(weimar_seed(100, 3))
        res = pr.MatchRunner(eng, WeimarMachine(wd.MACHINE_SCRIPT),
                             [Trump(), pr.NullPlayer()], st,
                             rules=RulesV1(),
                             arcana=ArcanaModule()).run()
        self.assertEqual(sum(1 for ev in st.log
                             if ev[0] == "suspended_beat"), 2)

    def test_check_term_limits(self):
        st = opening()
        oldest = st.in_play_statics[0]["name"]
        ArcanaModule().apply({"name": "TERM LIMITS"}, st,
                             WeimarMachine([]), None, 0, 3)
        self.assertNotIn(oldest, [s["name"] for s in st.in_play_statics])

    def test_check_habituation(self):
        r = RulesV1()
        st = opening()
        leaflet = {"name": "THE LEAFLET RUN", "r": 1, "a": 1}
        self.assertEqual(r.effective_r(st, leaflet), 1)
        st.tallies["played:THE LEAFLET RUN"] = 2
        self.assertEqual(r.effective_r(st, leaflet), 0)   # the third shocks no one

    def test_check_reclaim_priced(self):
        r = RulesV1()
        st = opening()
        st.in_play_statics.append({"name": "THE EXILE NETWORK",
                                   "reclaims": True, "a": 2,
                                   "side": "player"})
        st.e = 1
        self.assertEqual(r.rotation_effects(st)["reclaim"], 0)  # can't afford
        st.e = 2
        self.assertEqual(r.rotation_effects(st)["reclaim"], 1)  # full A, no M


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=94:21 imports_exports=8:2 calls_definitions=54:10
