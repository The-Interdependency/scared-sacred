# ratios: loc_comments=160:65 imports_exports=4:4 calls_definitions=80:13
"""cards_v1 — secret effects, interaction links, the M15 hinge, deck law.

WeimarMachine plays the scripted set with its mechanics live: SE gating
by A_SE against E (double resolution at M<=1), chains, timed and
permanent debuffs, static flips (the Courts), destruction links (the
Unions, Reichsbanner, the Camarilla), prerequisite skips fed by real
destruction events, and the Enabling Act hinge — the counterfactual
corridor as executable code.

Usage Guidance
--------------
    from weimar_data import MACHINE_SCRIPT, SETUP_STATICS, WEIMAR_OPENING
    from cards_v1 import WeimarMachine, validate_deck, field_totals
    m = WeimarMachine(MACHINE_SCRIPT)
    st = GameState(**WEIMAR_OPENING)
    st.in_play_statics += [dict(s) for s in SETUP_STATICS]
    MatchRunner(engine, m, players, st, rules=RulesV1()).run()
field_totals(state) returns (passive_s, passive_r) honoring fire-decree
debuffs; RulesV1 delegates to it when present. validate_deck enforces
tier law 40-59 / 60-79 / 80-99. NOOP_EFFECTS lists the honestly
unimplemented SEs. All numbers [conjectural].

# === MODULE_BUILD ===
# id: cards_v1
#   purpose: card mechanics for scripted sets; deck legality
#   surfaces: WeimarMachine, field_totals, validate_deck, NOOP_EFFECTS
#   boundaries: no sequence (runner), no field math (engine), no
#     legality of player plays (rules); machine-side mechanics only
#   tests: test_cards_v1.py
#   rollout: build step 4; ScriptedMachine retained for A/B
#   rollback: feed bare S dicts to ScriptedMachine
#   hmmm: eats_statics (Gleichschaltung) consumes the strongest standing
#     player institution per machine beat once M23/K09 land — the late
#     game eats the repair base, as it did. NOOP_EFFECTS =
#     noop_extra_card (M10), noop_window (M35),
#     camarilla rotation buff, book-fires *choice* target (resolves
#     against highest passive_r for now) — logged, not hidden
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: cards_se_gated_by_e
#   behavior: a secret effect resolves only when e >= a_se; a gated
#     chain with delay_if_gated fires on the following beat instead
# id: cards_se_doubles_at_low_m
#   behavior: at m <= 1 stacking effects apply twice
# id: cards_destruction_feeds_prereqs
#   behavior: destroying a machine card or static causes every later
#     card with that prereq to be skipped
# id: cards_courts_flip
#   behavior: the civil service law converts THE COURTS from player
#     passive_r to machine passive_s
# id: cards_hinge_reprices
#   behavior: with the coalition marker in play and m >= needs_m, the
#     enabling act resolves at fail_s and all later s reduce by
#     reprice_rest, floored at zero
# id: cards_deck_tier_law
#   behavior: decks outside 40-59/60-79/80-99 are illegal
# === END CONTRACTS ===
"""

NOOP_EFFECTS = {"noop_extra_card", "noop_window"}


def build_response_pile(seed=53):
    """Expand RESPONSE_DECK by copies into a shuffled 40-card pile."""
    import random
    from weimar_data import RESPONSE_DECK
    pile = []
    for i, c in enumerate(RESPONSE_DECK):
        pile += [dict(c, art_id=f"r{i+1:02d}")
                 for _ in range(c.get("copies", 1))]
    random.Random(seed).shuffle(pile)
    return pile


def field_totals(state):
    """(passive_s, passive_r) across in-play statics; machine-side
    debuff_response reduces each player static's contribution."""
    debuff = sum(s.get("debuff_response", 0) for s in state.in_play_statics
                 if s.get("side") == "machine")
    ps, pr = 0, 0
    for s in state.in_play_statics:
        if s.get("side") == "machine":
            ps += s.get("passive_s", 0)
        else:
            pr += max(0, s.get("passive_r", 0) - debuff
                      - s.get("perm_debuff", 0) - s.get("timed_debuff", 0))
    return ps, pr


def validate_deck(cards):
    n = sum(c.get("copies", 1) for c in cards)
    for lo, hi in ((40, 59), (60, 79), (80, 99)):
        if lo <= n <= hi:
            return True, n
    return False, n


class WeimarMachine:
    """The script with its mechanics live. History's plan, not history's
    guarantee: destruction feeds prerequisite skips."""

    def __init__(self, script, reserve=None):
        self.script = [dict(c) for c in script]
        self.reserve = [dict(c) for c in (reserve or [])]
        self._by_id = {c["id"]: c for c in self.script + self.reserve}
        self.cursor = 0
        self.destroyed = set()
        self.chain_queue = []
        self.delayed = []
        self.buff_next = 0
        self.event_buff = 0
        self.reprice = 0

    def destroy(self, ident):
        self.destroyed.add(ident)

    def peek(self, n):
        """Non-consuming look ahead (the Wayseer's whole power)."""
        return [dict(c) for c in self.script[self.cursor:self.cursor + n]]

    # ------------------------------------------------------- helpers

    def _tick_timed(self, state):
        for s in state.in_play_statics:
            if s.get("timed_beats"):
                s["timed_beats"] -= 1
                if s["timed_beats"] <= 0:
                    s["timed_debuff"] = 0

    def _apply_effect(self, se, state, card):
        kind = se.get("kind")
        if kind in NOOP_EFFECTS:
            state.log.append(("se_noop", card["id"], kind))
            return
        if kind == "chain":
            self.chain_queue.append("next")
        elif kind == "arm_next":
            self.buff_next += 0            # arming lowers next gate: v1 logs only
            state.log.append(("se_armed", card["id"]))
        elif kind == "buff_next":
            self.buff_next += se.get("amount", 1)
        elif kind == "timed_debuff":
            target = se.get("target")
            pool = [s for s in state.in_play_statics
                    if s.get("side") != "machine"]
            if target == "*choice*":
                pool.sort(key=lambda s: -s.get("passive_r", 0))
                chosen = pool[:1]
            else:
                chosen = [s for s in pool if s.get("name") == target]
            for s in chosen:
                s["timed_debuff"] = se.get("amount", 1)
                s["timed_beats"] = se.get("beats", 1)
        elif kind == "perm_debuff":
            for s in state.in_play_statics:
                if s.get("name") == se.get("target"):
                    s["perm_debuff"] = s.get("perm_debuff", 0) + se.get("amount", 1)
        elif kind == "flip_static":
            for s in state.in_play_statics:
                if s.get("name") == se.get("target"):
                    s["side"] = "machine"
                    s["passive_s"] = se.get("to_passive_s", 1)
                    s["passive_r"] = 0
                    state.log.append(("se_flip", se["target"]))

    def _resolve_se(self, card, state):
        se = card.get("se")
        if not se:
            return
        gate = se.get("a_se", 0)
        if state.e >= gate:
            times = 2 if (state.m <= 1 and se.get("kind") not in
                          {"chain"} | NOOP_EFFECTS) else 1
            for _ in range(times):
                self._apply_effect(se, state, card)
            state.log.append(("se", card["id"], se.get("kind"), times))
        elif se.get("delay_if_gated"):
            self.delayed.append(dict(se, delay_if_gated=None, card_id=card["id"]))

    def _resolve_hinge(self, card, state):
        h = card["hinge"]
        marker = any(s.get("name") == h["needs_marker"]
                     for s in state.in_play_statics)
        if marker and state.m >= h["needs_m"]:
            self.reprice = h["reprice_rest"]
            state.log.append(("hinge_failed_vote", card["id"]))
            return h["fail_s"]
        state.log.append(("hinge_passed", card["id"]))
        return card["s"]

    # --------------------------------------------------------- main

    def next_card(self, state):
        self._tick_timed(state)
        eaters = sum(s.get("eats_statics", 0) for s in state.in_play_statics
                     if s.get("side") == "machine")
        if eaters:
            prey = sorted((s for s in state.in_play_statics
                           if s.get("side") != "machine"),
                          key=lambda s: -s.get("passive_r", 0))
            for s in prey[:eaters]:
                state.in_play_statics.remove(s)
                state.log.append(("gleichgeschaltet", s.get("name")))
        for se in self.delayed:
            if state.e >= se.get("a_se", 0):
                self._apply_effect(se, state, {"id": se["card_id"]})
                self.delayed.remove(se)
        while self.cursor < len(self.script):
            card = self.script[self.cursor]
            self.cursor += 1
            prereq = card.get("prereq")
            if prereq and prereq in self.destroyed:
                state.log.append(("machine_skip", card["id"]))
                if self.reserve:                 # the plan dies; the machine
                    card = self.reserve.pop(0)   # improvises the beat anyway
                    state.log.append(("reserve_played", card["id"]))
                else:
                    continue
            s = card["s"]
            if card.get("hinge"):
                s = self._resolve_hinge(card, state)
            s = max(0, s + self.buff_next + self.event_buff - self.reprice)
            self.buff_next = 0
            for name in card.get("destroys", []):
                self.destroy(name)
                state.in_play_statics[:] = [x for x in state.in_play_statics
                                            if x.get("name") != name]
                state.log.append(("destroyed", name))
            if card.get("static"):
                st = dict(card["static"], name=card["name"], side="machine")
                state.in_play_statics.append(st)
                if "event_buff" in card["static"]:
                    self.event_buff += card["static"]["event_buff"]
            state.log.append(("machine_id", card["id"]))
            return {"name": card["name"], "id": card["id"], "s": s,
                    "has_se": bool(card.get("se"))}
        return None

    def resolve_se(self, played, state, countered=False):
        """Runner calls this after the reaction window. A countered SE
        never arms; the interception is logged, not explained."""
        card = self._by_id.get(played["id"])
        if not card or not card.get("se"):
            return
        if countered:
            state.log.append(("se_countered", card["id"]))
            return
        self._resolve_se(card, state)

# ratios: loc_comments=160:65 imports_exports=4:4 calls_definitions=80:13
