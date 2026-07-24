# ratios: loc_comments=69:92 imports_exports=2:1 calls_definitions=32:9
"""rules_v1 — legality and pricing for POLITICS. Build step 3.

The rules module answers exactly two questions and volunteers nothing:
may this play happen (legality), and what does it cost the commons
(pricing). No advice, no hints, no softening — rejection is silent.

Enforced doctrine (play v0.3 + ledger rulings 1-5, 2026-07-15):
  A-M GATE     response with activation A is legal iff E >= A - M - burn,
               where burn = discards this player allocated to reach.
  DISCARD      both semantics, declared at discard time: tempo (one extra
               action per discard) or reach (-1 effective barrier per
               discard). Never both from the same discarded card.
  TURN GRAMMAR at most one static; actions beyond the first each require
               one tempo discard; draw ends turn (runner owns the draw).
  TARGETING    every card declares target: machine-card | track | player.
  INTERFERENCE any player-targeted play injects its A into E as strain
               and costs M-1. Public and attributed (runner logs it).
  COALITION    over one full rotation: any shared declared target M+1,
               none shared M-1.
  RECLAMATION  only statics of the sponsorship/exile family reclaim
               crossed vectors: one per rotation, full A, undiscounted.

Usage Guidance
--------------
    from rules_v1 import RulesV1
    rules = RulesV1()
    runner = MatchRunner(engine, machine, players, state, rules=rules)
    # play dicts: {"kind": "action"|"static", "name": str, "a": int,
    #              "r": int, "target": "machine"|"track"|"player",
    #              "burn": int, "reclaims": bool}
    # TurnPlays.discards is the total burned; rules verifies tempo+reach
    # spending never exceeds it.
Integration: pairs with politics_runner v0.2 hooks (validate_turn,
interference, coalition, rotation_effects). Replace PermissiveRules to
turn pricing on; A/B against it to measure what pricing changes.
All numbers [conjectural].

# === MODULE_BUILD ===
# id: rules_v1
#   purpose: activation gating, turn grammar, targeting, interference,
#     coalition, reclamation permission
#   surfaces: RulesV1.legal, validate_turn, interference, coalition,
#     rotation_effects
#   boundaries: legality and pricing only; no game state mutation; no
#     advice (silent rejection per no-tips doctrine)
#   tests: test_rules_v1.py
#   rollout: build step 3; PermissiveRules retained for A/B
#   rollback: pass rules=None to MatchRunner
#   hmmm: agenda-floor enforcement deferred to match-end module; scale
#     multiplayer pricing untouched until matchmaking exists
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: rules_gate_a_minus_m
#   behavior: an action is legal iff e >= a - m - burn; otherwise
#     silently rejected
# id: rules_discard_budget
#   behavior: tempo discards plus reach burn never exceed declared
#     discards; over-budget turns are trimmed, never explained
# id: rules_interference_priced
#   behavior: player-targeted plays report strain equal to their a and
#     an m penalty of one
# id: rules_coalition_window
#   behavior: shared declared target across one rotation yields m+1,
#     no shared target yields m-1
# id: rules_reclaims_gated
#   behavior: only reclaiming statics reclaim, at most one vector per
#     rotation
# id: rules_habituation_decay
#   behavior: effective r decays by one per two prior table-wide plays
#     of the same card name, floored at zero
# id: rules_reclaim_priced
#   behavior: reclamation requires e at or above the reclaiming static's
#     full a, undiscounted by m
# id: rules_reflex_gate_uses_incoming
#   behavior: reflex legality evaluates a - m against e plus the
#     triggering card's s; reflex_only_to, requires_static and
#     blocked_by all bind
# === END CONTRACTS ===
"""


class RulesV1:
    """Legality and pricing. Mutates nothing; reports everything."""

    # ------------------------------------------------------- per-play

    def legal(self, state, play):
        if not isinstance(play, dict):
            return False
        blocked = play.get("blocked_by")
        if blocked and any(s.get("name") == blocked
                           for s in state.in_play_statics):
            return False
        if play.get("needs_m") and state.m < play["needs_m"]:
            return False
        kind = play.get("kind", "action")
        if kind == "static":
            return True                      # laying an institution is free
        a = play.get("a", 0)
        for name, extra in (play.get("a_extra_while") or {}).items():
            if any(s.get("name") == name for s in state.in_play_statics):
                a += extra
        burn = play.get("burn", 0)
        return state.e >= a - state.m - burn

    def field_totals(self, state):
        from cards_v1 import field_totals
        return field_totals(state)

    def reflex_legal(self, state, play, incoming):
        """Reflex gate: the provocation supplies its own activation
        energy — evaluate A - M against E plus the incoming card's S."""
        if not play.get("reflex"):
            return False
        only = play.get("reflex_only_to")
        if only and incoming.get("id") != only:
            return False
        req = play.get("requires_static")
        if req and not any(s.get("name") == req and s.get("side") != "machine"
                           for s in state.in_play_statics):
            return False
        blocked = play.get("blocked_by")
        if blocked and any(s.get("name") == blocked
                           for s in state.in_play_statics):
            return False
        a = play.get("a", 0)
        return state.e + incoming.get("s", 0) >= a - state.m

    # ------------------------------------------------------ per-turn

    def validate_turn(self, state, plays):
        """Trim a TurnPlays to grammar and discard budget. Silent."""
        budget = plays.discards
        reach_spend = sum(p.get("burn", 0) for p in plays.actions)
        kept, tempo_spend = [], 0
        for i, action in enumerate(plays.actions):
            cost = 0 if i == 0 else 1        # extras cost one tempo discard
            if reach_spend + tempo_spend + cost <= budget or (i == 0 and reach_spend <= budget):
                kept.append(action)
                tempo_spend += cost
        plays.actions = kept
        return plays

    # -------------------------------------------------------- pricing

    def interference(self, state, play):
        """Returns (strain, m_delta) a resolved play injects into the
        commons. Player-targeted plays heat the pot; m_bonus cards
        (Wels) build it; nothing else moves it."""
        s, dm = 0, play.get("m_bonus", 0)
        if play.get("target") == "player":
            s, dm = play.get("a", 0), dm - 1
        return s, dm

    def coalition(self, declared_targets):
        """One rotation of declared targets -> m delta."""
        named = [t for t in declared_targets if t]
        if len(named) != len(set(named)):
            return 1                          # any shared target
        if named:
            return -1                         # all pulling apart
        return -1                             # nobody declared anything

    def rotation_effects(self, state):
        """Reclamation permission: one vector per rotation, only if a
        reclaiming static stands, priced at the static's full A,
        undiscounted by M (reclaiming a person costs more than keeping
        them was — ledger ruling 4)."""
        reclaimers = [s for s in state.in_play_statics if s.get("reclaims")]
        if reclaimers and state.e >= reclaimers[0].get("a", 0):
            return {"reclaim": 1}
        return {"reclaim": 0}

    def effective_r(self, state, play):
        """Habituation: the third leaflet shocks no one. Each prior play
        of the same card name across the table decays its R."""
        prior = state.tallies.get("played:" + play.get("name", ""), 0)
        return max(0, play.get("r", 0) - prior // 2)

# ratios: loc_comments=69:92 imports_exports=2:1 calls_definitions=32:9
