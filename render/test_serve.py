# ratios: loc_comments=59:12 imports_exports=4:1 calls_definitions=34:5
"""Checks for the table server (no browser required).

# === CHECKS ===
# id: check_state_reports_truth
#   witnesses: serve_state_reports_truth, serve_arcana_playable
# id: check_act_enforces_hand_law
#   witnesses: serve_act_enforces_hand_law
# id: check_reaction_request_validation
#   witnesses: serve_reaction_window
# id: check_match_thread_completes
#   witnesses: serve_match_thread_completes
# === END CHECKS ===
"""
import time
import unittest

import serve
import politics_runner as pr


class Checks(unittest.TestCase):

    def test_check_state_reports_truth(self):
        t = serve.Table(seats=2)
        time.sleep(0.1)
        s = t.snapshot()
        self.assertEqual(len(s["field"]), 100)
        self.assertIn("population", s["tracks"])
        self.assertEqual(len(s["hand"]), 5)
        self.assertTrue(s["arcana"].get("name"))
        self.assertIn("reaction", s)
        if t.human.reaction is not None:
            t.human.reaction_inbox.put(None)
        if t.human.awaiting:
            t.human.inbox.put(pr.TurnPlays())

    def test_check_act_enforces_hand_law(self):
        fake = type("FakeTable", (), {})()
        fake.state = pr.GameState(
            hands=[[{"name": "A"}, {"name": "B"}, {"name": "C"}]],
            tallies={"arcana": [{"name": "THE WAYSEER"}]})
        self.assertIsNone(serve.turn_from_request(
            fake, {"kind": "action", "card": 99, "burns": []}))
        self.assertIsNone(serve.turn_from_request(
            fake, {"kind": "action", "card": 0, "burns": [0]}))
        turn = serve.turn_from_request(
            fake, {"kind": "action", "card": 0, "burns": [1]})
        self.assertIs(turn.actions[0], fake.state.hands[0][0])
        self.assertEqual(turn.discard_cards, [fake.state.hands[0][1]])

    def test_check_reaction_request_validation(self):
        fake = type("FakeTable", (), {})()
        fake.state = pr.GameState(hands=[[{"name": "RX"}, {"name": "BURN"}]])
        fake.human = type("FakeHuman", (), {})()
        fake.human.reaction = {"incoming": {"id": "M15"}, "candidates": [0]}
        self.assertEqual(
            serve.reaction_from_request(fake, {"card": 0, "burn": 1}),
            (True, (0, 1)))
        self.assertEqual(
            serve.reaction_from_request(fake, {"card": 0, "burn": 0}),
            (False, None))
        self.assertEqual(
            serve.reaction_from_request(fake, {"pass": True}),
            (True, None))

    def test_check_match_thread_completes(self):
        t = serve.Table(seats=2)
        for _ in range(400):
            if t.human.reaction is not None:
                t.human.reaction_inbox.put(None)
            if t.human.awaiting:
                t.human.inbox.put(pr.TurnPlays())
            if t.result is not None:
                break
            time.sleep(0.02)
        self.assertIsNotNone(t.result)
        self.assertEqual(t.result.outcome, "loss")   # passing every turn is null


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=59:12 imports_exports=4:1 calls_definitions=34:5
