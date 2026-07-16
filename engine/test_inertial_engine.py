# ratios: loc_comments=45:12 imports_exports=3:2 calls_definitions=27:7
"""Checks for inertial_engine. Run: python3 test_inertial_engine.py

# === CHECKS ===
# id: check_inertia_resists_early
#   witnesses: engine_inertia_resists_early
# id: check_conversion_is_hysteretic
#   witnesses: engine_conversion_is_hysteretic
# id: check_population_matches_field
#   witnesses: engine_population_matches_field
# id: check_repair_slows_collapse
#   witnesses: engine_repair_slows_collapse
# === END CHECKS ===
"""
import unittest

import politics_runner as pr
from inertial_engine import InertialEngine, Person, weimar_seed

WEIMAR_S = [2,1,2,2,2,1,3,2,1,2, 2,2,2,1,3,2,2,1,1,3,
            1,2,2,1,1,1,1,2,1,1, 1,2,1,1,0,3,2,1,3,2]


def match(engine, players):
    script = [{"name": f"M{i+1:02d}", "s": s} for i, s in enumerate(WEIMAR_S)]
    st = pr.GameState(population=100, e=5, m=1)
    st.in_play_statics.append({"name": "ARTICLE 48", "passive": 1})
    return pr.MatchRunner(engine, pr.ScriptedMachine(script), players, st).run()


class Checks(unittest.TestCase):

    def test_check_inertia_resists_early(self):
        eng = InertialEngine(weimar_seed(100, 157))
        res = match(eng, [pr.NullPlayer()] * 3)
        n = len(eng.curve)
        first_q = eng.curve[0][1] - eng.curve[n // 4][1]
        last_q = eng.curve[3 * n // 4][1] - eng.curve[-1][1]
        self.assertLess(first_q, last_q)          # sigmoid, not linear

    def test_check_conversion_is_hysteretic(self):
        eng = InertialEngine([Person(x=1.2, v=0.0, m=1.0, converted=True)])
        st = pr.GameState(population=0, e=0, m=2)
        eng.pmr(st, s_total=0, r_total=50, registration=False)
        self.assertTrue(eng.persons[0].converted)  # ambient calm never un-converts

    def test_check_population_matches_field(self):
        eng = InertialEngine(weimar_seed(100, 157))
        res = match(eng, [pr.NullPlayer()] * 3)
        unconverted = sum(1 for p in eng.persons if not p.converted)
        self.assertEqual(res.state.population, unconverted)

    def test_check_repair_slows_collapse(self):
        eng_null = InertialEngine(weimar_seed(100, 157))
        beat_null = match(eng_null, [pr.NullPlayer()] * 3).machine_beats

        class OneAction:
            def take_turn(self, state, pid):
                return pr.TurnPlays(actions=[{"name": "r", "r": 1}])
        eng_r = InertialEngine(weimar_seed(100, 157))
        res_r = match(eng_r, [OneAction()] * 3)
        later = (res_r.outcome == "win") or (res_r.machine_beats > beat_null)
        self.assertTrue(later)

    def test_calibration_null_always_loses(self):
        for seed in (1, 7, 53, 157, 999):
            eng = InertialEngine(weimar_seed(100, seed))
            res = match(eng, [pr.NullPlayer()] * 3)
            self.assertEqual(res.outcome, "loss")   # ratified: no play, no republic


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=45:12 imports_exports=3:2 calls_definitions=27:7
