# ratios: loc_comments=97:32 imports_exports=7:6 calls_definitions=33:14
"""harness_v1 — batch playtest instrument. Build step 5a.

Runs match batches across player policies and seeds; reports win rate,
mean collapse beat, hinge outcomes, and final tracks. This is the
possible-not-probable measuring stick: balance claims without harness
numbers stay [conjectural]; with them they graduate to [test-backed].

Policies (no policy receives advice; they are players, not tutors):
  null     plays nothing (the apathy baseline)
  selfish  cheapest legal action, never shares a target, hoards statics
  noisy    coordinates imperfectly: shares targets with probability p,
           lays statics on a whim, sometimes passes
  squad    scripted optimal coordination (upper bound, not a human)

Usage Guidance
--------------
    python3 harness_v1.py            # standard spectrum, 40 seeds each
    from harness_v1 import spectrum  # or programmatic
Interpretation discipline: squad is a ceiling; humans live between
noisy and squad. Possible-not-probable targets: null 0%, noisy low,
squad high-but-not-guaranteed. All thresholds [conjectural].

# === MODULE_BUILD ===
# id: harness_v1
#   purpose: measure win-rate spectrum across coordination levels
#   surfaces: spectrum, run_match, policies (Null/Selfish/Noisy/Squad)
#   boundaries: measurement only; no tuning decisions encoded; policies
#     receive no advice (players, not tutors)
#   tests: smoke via __main__ spectrum run
#   rollout: step 5a; feeds every future balance claim
#   rollback: delete; balance claims regress to conjectural
#   hmmm: agenda pursuit not yet modeled in selfish policy; squad is
#     scripted, not learned — a0 model seats replace it at phase 2
# === END MODULE_BUILD ===
"""

import random

import politics_runner as pr
import weimar_data as wd
from cards_v1 import WeimarMachine
from inertial_engine import InertialEngine, weimar_seed
from rules_v1 import RulesV1


def _card(name):
    return dict([c for c in wd.RESPONSE_DECK if c["name"] == name][0])


class HarnessRules(RulesV1):
    """RulesV1 plus the m_bonus wire (Wels) used across policies."""

    def interference(self, state, play):
        s, dm = super().interference(state, play)
        return s, dm + play.get("m_bonus", 0)


class SelfishPlayer:
    def __init__(self, rng):
        self.rng = rng
        self.laid = 0

    def take_turn(self, state, pid):
        static = None
        if self.laid < 1:
            static = dict(_card("THE NEIGHBORHOOD"), side="player")
            self.laid += 1
        act = dict(_card("THE LEAFLET RUN"),
                   declared_target=f"own-{pid}")        # never shared
        return pr.TurnPlays(static=static, actions=[act])


class NoisyCoopPlayer:
    def __init__(self, rng, p_share=0.5):
        self.rng, self.p = rng, p_share
        self.laid = 0

    def take_turn(self, state, pid):
        if self.rng.random() < 0.15:
            return pr.TurnPlays()                        # distracted
        static = None
        if self.laid < 2 and self.rng.random() < 0.4:
            static = dict(_card(self.rng.choice(
                ["THE NEIGHBORHOOD", "THE EXILE NETWORK",
                 "THE FOREIGN CORRESPONDENTS"])), side="player")
            self.laid += 1
        share = self.rng.random() < self.p
        target = "shared" if share else f"own-{pid}"
        name = "WELS' SPEECH" if (state.m < 3 and self.rng.random() < 0.3) \
            else "THE LEAFLET RUN"
        return pr.TurnPlays(actions=[dict(_card(name),
                                          declared_target=target)])


class SquadPlayer:
    def __init__(self, rng):
        self.t = 0

    def take_turn(self, state, pid):
        self.t += 1
        static = None
        if self.t == 1:
            static = dict(_card("THE NEIGHBORHOOD"), side="player")
        if self.t == 2:
            static = dict(_card("THE EXILE NETWORK"), side="player")
        if state.m < 3:
            act = dict(_card("WELS' SPEECH"), declared_target="shared")
        elif not any(s.get("name") == "THE COALITION VOTE"
                     for s in state.in_play_statics):
            act = dict(_card("THE COALITION VOTE"), declared_target="shared")
        else:
            act = dict(_card("THE LEAFLET RUN"), declared_target="shared")
        return pr.TurnPlays(static=static, actions=[act])


POLICIES = {
    "null":    lambda rng: pr.NullPlayer(),
    "selfish": lambda rng: SelfishPlayer(rng),
    "noisy":   lambda rng: NoisyCoopPlayer(rng),
    "squad":   lambda rng: SquadPlayer(rng),
}


def run_match(policy, seed, humans=3):
    rng = random.Random(seed)
    st = pr.GameState(**wd.WEIMAR_OPENING)
    st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
    eng = InertialEngine(weimar_seed(100, seed))
    players = [POLICIES[policy](random.Random(seed * 101 + i))
               for i in range(humans)]
    res = pr.MatchRunner(eng, WeimarMachine(wd.MACHINE_SCRIPT),
                         players, st, rules=HarnessRules()).run()
    hinge = [ev for ev in res.state.log if ev[0].startswith("hinge")]
    return {"outcome": res.outcome, "beats": res.machine_beats,
            "pop": res.state.population,
            "hinge_failed": any(ev[0] == "hinge_failed_vote" for ev in hinge)}


def spectrum(seeds=40):
    out = {}
    for policy in POLICIES:
        rows = [run_match(policy, s) for s in range(1, seeds + 1)]
        wins = sum(r["outcome"] == "win" for r in rows)
        out[policy] = {
            "win_rate": wins / len(rows),
            "mean_end_beat": sum(r["beats"] for r in rows) / len(rows),
            "mean_pop": sum(r["pop"] for r in rows) / len(rows),
            "hinge_fail_rate": sum(r["hinge_failed"] for r in rows) / len(rows),
        }
    return out


if __name__ == "__main__":
    for k, v in spectrum().items():
        print(f"{k:8s} win {v['win_rate']:.0%}  end-beat "
              f"{v['mean_end_beat']:.1f}  pop {v['mean_pop']:.0f}  "
              f"hinge-failed {v['hinge_fail_rate']:.0%}")
# ratios: loc_comments=97:32 imports_exports=7:6 calls_definitions=33:14
