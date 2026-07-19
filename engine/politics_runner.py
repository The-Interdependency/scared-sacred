# ratios: loc_comments=193:103 imports_exports=3:8 calls_definitions=95:20
"""politics_runner — turn-sequence runner for POLITICS (base game).

The runner owns the ORDER of play and nothing else. All game truth lives
in the modules it calls: the engine owns the math, the machine owns card
selection, players own their plays, rules own legality. The runner never
computes strain, never advises, never softens. No tips, no tricks.

Sequence (Erin's spec, ratified):
    match start -> machine beat -> p1 turn -> machine beat -> p2 turn ->
    machine beat -> ... -> machine beat -> p1 turn -> ...
A machine beat = one Machine card + population math run (PMR with
registration). A player turn = lay one static, play one action, optional
discard-to-play-extra-actions, draw ends turn; then a PMR WITHOUT
registration (E/M update only) [claude-default, reversible].

Usage Guidance
--------------
Run the null-clock calibration (no player ever plays):

    from politics_runner import (MatchRunner, LeakyEngine,
                                 ScriptedMachine, NullPlayer, GameState)
    machine = ScriptedMachine([{"name": f"M{i:02d}", "s": 2, "passive": 0}
                               for i in range(1, 41)])
    r = MatchRunner(engine=LeakyEngine(),
                    machine=machine,
                    players=[NullPlayer(), NullPlayer(), NullPlayer()],
                    state=GameState(population=100, e=0, m=2))
    result = r.run()
    print(result.outcome, result.machine_beats, result.state.population)

Swap NullPlayer for any object with take_turn(state, pid) -> TurnPlays to
seat a human UI, an a0 agent, or an older-model playtester. Swap
ScriptedMachine for a policy machine in later sets; Weimar ships scripted.
Integration: this module is build-order step 1; the engine here is the
step-2 stub already carrying the real leaky-integrator math so the null
clock demo runs end to end. All balance numbers [conjectural].

# === MODULE_BUILD ===
# id: politics_runner_v01
#   purpose: own the interleaved turn sequence; delegate all game logic
#   surfaces: MatchRunner.run, GameState, TurnPlays, module protocols
#   boundaries: no game math, no card knowledge, no advice to players;
#     legality enforced by rejection only (no tips doctrine)
#   tests: test_politics_runner.py (CHECKS reconcile CONTRACTS below)
#   rollout: step 1 of ratified build order; stubs replaced organ by organ
#   rollback: pure stdlib, no persistence; delete file to remove
#   hmmm: player-beat PMR without registration is claude-default pending
#     Erin; null clock recalibration under interleaving is open
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: runner_sequence_interleaved
#   behavior: machine beats open the match and follow every player turn
# id: runner_registration_machine_only
#   behavior: population is reduced only on machine beats; player beats
#     update e and m only
# id: runner_loss_at_half
#   behavior: match ends in loss the moment population <= 50
# id: runner_win_on_empty_deck
#   behavior: match ends in win when the machine deck is exhausted and
#     population > 50
# id: runner_null_clock_terminates
#   behavior: with null players the match always ends in loss in finite
#     beats (the machine needs no will)
# id: runner_rejects_illegal_plays
#   behavior: plays failing the rules module are dropped silently; the
#     runner never explains or advises
# id: runner_rotation_boundary_hooks
#   behavior: after each full rotation the runner applies the rules
#     coalition delta and any permitted reclamation, then clears the
#     declared-target window
# id: runner_interference_passthrough
#   behavior: strain and m deltas reported by rules.interference are
#     applied on the player beat that caused them
# id: runner_field_totals_delegation
#   behavior: when the rules module computes field totals, machine-beat
#     passives (both sides) come from it; standing institutions repair
#     every machine beat they survive
# id: runner_hand_law
#   behavior: in hand mode, a play resolves only from the hand holding
#     it; played and burned cards move to the discard pile; the turn ends
#     with one draw while the pile lasts
# id: runner_suspension_primitive
#   behavior: while suspend_beats > 0 a machine beat consumes the
#     suspension instead of a card: no card, no pmr, population unchanged
#     (shared plumbing: filibuster now, the witness rule later)
# id: runner_reaction_window
#   behavior: after a machine card reveals and before its PMR, players
#     may discard one card to reflex a reflex-flagged card into the beat;
#     a counters_se reflex prevents the incoming secret effect from ever
#     arming
# === END CONTRACTS ===
"""

from dataclasses import dataclass, field


# ---------------------------------------------------------------- state

@dataclass
class GameState:
    """Track container. The population registers; it never chooses."""
    population: int = 100
    e: int = 0
    m: int = 2
    machine_beats: int = 0
    in_play_statics: list = field(default_factory=list)
    log: list = field(default_factory=list)
    draw_pile: list = field(default_factory=list)
    hands: list = field(default_factory=list)
    discard_pile: list = field(default_factory=list)
    tallies: dict = field(default_factory=dict)
    suspend_beats: int = 0


@dataclass
class TurnPlays:
    """What one player submits for one turn."""
    static: dict | None = None
    actions: list = field(default_factory=list)
    discards: int = 0
    arcana: dict | None = None


@dataclass
class MatchResult:
    outcome: str          # "loss" | "win"
    machine_beats: int
    state: GameState
    agenda_outcomes: list = field(default_factory=list)


# -------------------------------------------------------- stub modules

class LeakyEngine:
    """PMR: the leaky integrator. E = max(0, E + S - R); cooling; then
    registration (population -= E) on machine beats only."""

    def pmr(self, state, s_total, r_total, registration):
        state.e = max(0, state.e + s_total - r_total)
        cooling = 2 if state.m >= 4 else 1
        state.e = max(0, state.e - cooling)
        if registration:
            state.population -= state.e
        return state


class ScriptedMachine:
    """Replay machine: fixed card order, prerequisite-gated skips.
    History's plan, not history's guarantee."""

    def __init__(self, script, destroyed=None):
        self.script = list(script)
        self.destroyed = set(destroyed or [])
        self.cursor = 0

    def next_card(self, state):
        while self.cursor < len(self.script):
            card = self.script[self.cursor]
            self.cursor += 1
            prereq = card.get("prereq")
            if prereq and prereq in self.destroyed:
                state.log.append(("machine_skip", card["name"]))
                continue
            return card
        return None


class NullPlayer:
    """Plays nothing. Apathy, as a module."""

    def take_turn(self, state, player_id):
        return TurnPlays()


class PermissiveRules:
    """Stub legality: accepts anything shaped like a play. Real rules
    module (activation energy, targets) replaces this at build step 3."""

    def legal(self, state, play):
        return isinstance(play, dict)


# --------------------------------------------------------------- runner

class MatchRunner:
    """Owns the sequence. Machine first; one machine beat per player turn."""

    def __init__(self, engine, machine, players, state, rules=None,
                 hand_size=None, arcana=None):
        self.arcana = arcana
        self.engine = engine
        self.machine = machine
        self.players = players
        self.state = state
        self.rules = rules or PermissiveRules()
        self._targets = []
        self.hand_mode = hand_size is not None
        if self.hand_mode:
            for _ in players:
                self.state.hands.append(
                    [self.state.draw_pile.pop(0)
                     for _ in range(min(hand_size,
                                        len(self.state.draw_pile)))])

    def _take_from_hand(self, pid, card):
        """Hand law: a card resolves only out of the hand that holds it."""
        hand = self.state.hands[pid]
        for i, c in enumerate(hand):
            if c is card or c == card:
                self.state.discard_pile.append(hand.pop(i))
                return True
        return False

    def _reaction_window(self, mcard):
        """Machine card revealed; before its PMR, any player may discard
        one card to reflex one reflex-flagged card into the beat.
        Returns (extra_r, se_countered)."""
        extra_r, countered = 0, False
        for pid, player in enumerate(self.players):
            if not hasattr(player, "react"):
                continue
            rx = player.react(self.state, pid, mcard)
            if not rx:
                continue
            reflex_card, burn = rx
            legal = (not hasattr(self.rules, "reflex_legal")
                     or self.rules.reflex_legal(self.state, reflex_card,
                                                mcard))
            if not legal:
                continue
            if self.hand_mode:
                if not self._take_from_hand(pid, burn):
                    continue
                if not self._take_from_hand(pid, reflex_card):
                    continue
            extra_r += reflex_card.get("r", 0)
            self._targets.append(mcard.get("id"))
            self.state.log.append(("reflex", pid, reflex_card.get("name"),
                                   mcard.get("id")))
            if reflex_card.get("counters_se") and mcard.get("has_se"):
                countered = True
        return extra_r, countered

    def _machine_beat(self):
        if self.state.suspend_beats > 0:          # the world holds still
            self.state.suspend_beats -= 1
            self.state.log.append(("suspended_beat",))
            return None
        card = self.machine.next_card(self.state)
        if card is None:
            return "deck_empty"
        self.state.machine_beats += 1
        if hasattr(self.rules, "field_totals"):
            passive_s, passive_r = self.rules.field_totals(self.state)
        else:
            passive_s = sum(s.get("passive", 0)
                            for s in self.state.in_play_statics)
            passive_r = 0
        self.state.log.append(("machine", card["name"], card["s"]))
        reflex_r, countered = self._reaction_window(card)
        if hasattr(self.machine, "resolve_se"):
            self.machine.resolve_se(card, self.state, countered=countered)
        self.engine.pmr(self.state, card["s"] + passive_s,
                        passive_r + reflex_r, registration=True)
        if self.state.population <= 50:
            return "loss"
        return None

    def _player_beat(self, pid):
        plays = self.players[pid].take_turn(self.state, pid)
        if hasattr(self.rules, "validate_turn"):
            plays = self.rules.validate_turn(self.state, plays)
        if self.arcana and getattr(plays, "arcana", None):
            self.arcana.apply(plays.arcana, self.state, self.machine,
                              self.engine, pid, len(self.players))
        if self.hand_mode:
            if plays.static and not self._take_from_hand(pid, plays.static):
                plays.static = None
            plays.actions = [a for a in plays.actions
                             if self._take_from_hand(pid, a)]
        r_total, s_extra = 0, 0
        if plays.static and self.rules.legal(self.state, plays.static):
            self.state.in_play_statics.append(plays.static)
            self.state.log.append(("static", pid, plays.static.get("name")))
        for action in plays.actions:
            if self.rules.legal(self.state, action):
                if hasattr(self.rules, "effective_r"):
                    r_total += self.rules.effective_r(self.state, action)
                else:
                    r_total += action.get("r", 0)
                n = self.state.tallies.get("played:" + action.get("name", ""), 0)
                self.state.tallies["played:" + action.get("name", "")] = n + 1
                self._targets.append(action.get("declared_target"))
                self.state.log.append(("action", pid, action.get("name"),
                                       action.get("target")))
                if hasattr(self.rules, "interference"):
                    ds, dm = self.rules.interference(self.state, action)
                    s_extra += ds
                    self.state.m = max(0, min(5, self.state.m + dm))
        self.engine.pmr(self.state, s_extra, r_total, registration=False)
        if self.hand_mode and self.state.draw_pile:
            self.state.hands[pid].append(self.state.draw_pile.pop(0))
        return None

    def _rotation_boundary(self):
        if hasattr(self.rules, "coalition"):
            dm = self.rules.coalition(self._targets)
            self.state.m = max(0, min(5, self.state.m + dm))
        self._targets = []
        if hasattr(self.rules, "rotation_effects") and \
                hasattr(self.engine, "reclaim"):
            fx = self.rules.rotation_effects(self.state)
            if fx.get("reclaim"):
                self.engine.reclaim(self.state, fx["reclaim"])
        return None

    def run(self, max_beats=500):
        halt = self._machine_beat()
        while halt is None and self.state.machine_beats < max_beats:
            for pid in range(len(self.players)):
                self._player_beat(pid)
                halt = self._machine_beat()
                if halt is not None:
                    break
            if halt is None:
                self._rotation_boundary()
        outcome = "win" if (halt == "deck_empty"
                            and self.state.population > 50) else "loss"
        verdicts = []
        if self.state.tallies.get("agendas"):
            from arcana_agendas_v1 import verify_agendas
            verdicts = verify_agendas(self.state, outcome)
        return MatchResult(outcome, self.state.machine_beats, self.state,
                           verdicts)

# ratios: loc_comments=193:103 imports_exports=3:8 calls_definitions=95:20
