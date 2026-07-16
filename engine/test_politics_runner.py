# ratios: loc_comments=50:17 imports_exports=2:3 calls_definitions=26:12
"""Checks for politics_runner. Run: python3 test_politics_runner.py

# === CHECKS ===
# id: check_sequence_interleaved
#   witnesses: runner_sequence_interleaved
# id: check_registration_machine_only
#   witnesses: runner_registration_machine_only
# id: check_loss_at_half
#   witnesses: runner_loss_at_half
# id: check_win_on_empty_deck
#   witnesses: runner_win_on_empty_deck
# id: check_null_clock_terminates
#   witnesses: runner_null_clock_terminates
# id: check_rejects_illegal_plays
#   witnesses: runner_rejects_illegal_plays
# === END CHECKS ===
"""
import unittest

from politics_runner import (GameState, LeakyEngine, MatchRunner, NullPlayer,
                             ScriptedMachine, TurnPlays)


def deck(n, s=2):
    return [{"name": f"M{i:02d}", "s": s} for i in range(1, n + 1)]


class RecordingPlayer:
    def __init__(self, plays=None):
        self.plays = plays or TurnPlays()
        self.turns_seen = 0

    def take_turn(self, state, pid):
        self.turns_seen += 1
        return self.plays


class Checks(unittest.TestCase):

    def _run(self, cards, players, e=0, m=2, rules=None):
        r = MatchRunner(LeakyEngine(), ScriptedMachine(cards), players,
                        GameState(e=e, m=m), rules=rules)
        return r.run()

    def test_check_sequence_interleaved(self):
        p = [RecordingPlayer(), RecordingPlayer(), RecordingPlayer()]
        res = self._run(deck(7, s=0), p)
        machine_idx = [i for i, ev in enumerate(res.state.log)
                       if ev[0] == "machine"]
        self.assertEqual(machine_idx[0], 0)          # machine opens
        self.assertEqual(len(machine_idx), 7)        # every card played

    def test_check_registration_machine_only(self):
        active = RecordingPlayer(TurnPlays(actions=[{"name": "a", "r": 1}]))
        res = self._run(deck(1, s=0), [active])
        # one machine beat at s=0, e stays 0 -> population untouched
        self.assertEqual(res.state.population, 100)

    def test_check_loss_at_half(self):
        res = self._run(deck(40, s=5), [NullPlayer()])
        self.assertEqual(res.outcome, "loss")
        self.assertLessEqual(res.state.population, 50)

    def test_check_win_on_empty_deck(self):
        res = self._run(deck(3, s=0), [NullPlayer()])
        self.assertEqual(res.outcome, "win")

    def test_check_null_clock_terminates(self):
        for players in (2, 3, 4, 5, 6):
            res = self._run(deck(400, s=3),
                            [NullPlayer() for _ in range(players)])
            self.assertEqual(res.outcome, "loss")

    def test_check_rejects_illegal_plays(self):
        class NoRules:
            def legal(self, state, play):
                return False
        active = RecordingPlayer(TurnPlays(static={"name": "x", "passive": 9},
                                           actions=[{"name": "a", "r": 9}]))
        res = self._run(deck(2, s=1), [active], rules=NoRules())
        self.assertEqual(res.state.in_play_statics, [])   # dropped silently


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=50:17 imports_exports=2:3 calls_definitions=26:12
