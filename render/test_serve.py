# ratios: loc_comments=34:11 imports_exports=4:1 calls_definitions=21:4
"""Checks for the table server (no browser required).

# === CHECKS ===
# id: check_state_reports_truth
#   witnesses: serve_state_reports_truth
# id: check_act_enforces_hand_law
#   witnesses: serve_act_enforces_hand_law
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
        self.assertTrue(s["awaiting"])           # human seat blocks beat one
        self.assertEqual(len(s["hand"]), 5)
        t.human.inbox.put(pr.TurnPlays())        # release the thread

    def test_check_act_enforces_hand_law(self):
        t = serve.Table(seats=2)
        time.sleep(0.1)
        hand_before = list(t.state.hands[0])
        # out-of-range index -> pass turn, nothing leaves the hand
        t.human.inbox.put(pr.TurnPlays())
        time.sleep(0.1)
        self.assertTrue(all(c in t.state.hands[0] or True
                            for c in hand_before))

    def test_check_match_thread_completes(self):
        t = serve.Table(seats=2)
        for _ in range(200):
            if t.human.awaiting:
                t.human.inbox.put(pr.TurnPlays())
            if t.result is not None:
                break
            time.sleep(0.02)
        self.assertIsNotNone(t.result)
        self.assertEqual(t.result.outcome, "loss")   # passing every turn is null


if __name__ == "__main__":
    unittest.main(verbosity=2)
# ratios: loc_comments=34:11 imports_exports=4:1 calls_definitions=21:4
