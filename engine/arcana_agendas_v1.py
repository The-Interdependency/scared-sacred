# ratios: loc_comments=119:51 imports_exports=2:3 calls_definitions=45:5
"""arcana_agendas_v1 — secret agendas and the nine trumps. Build step 5c.

AGENDAS: dealt one per player at setup, secret, verified at match end.
Fifty-Three Days runs ashes-mode (ledger ruling 5, claude-default
ratified by silence): agendas verify on EITHER outcome -- the set admits
players who win in the ashes, because its historical agenda-holders did.

ARCANA: rule-class trumps outside the S/R economy. One per player, once
per game, public and attributed. The Wayseer reveals; it never controls.

Usage Guidance
--------------
    from arcana_agendas_v1 import (deal_agendas, verify_agendas,
                                   ARCANA, ArcanaModule)
    deal_agendas(state, players=3, rng)
    runner = MatchRunner(..., arcana=ArcanaModule())
    plays = TurnPlays(arcana={"name": "THE WAYSEER"})   # from your deal
    result.agenda_outcomes  # per-player verdicts at match end
Filibuster and the Witness Rule share the suspension primitive
(GameState.suspend_beats): the world stopping is sequence-level plumbing,
built once. All numbers [conjectural].

# === MODULE_BUILD ===
# id: arcana_agendas_v1
#   purpose: non-alignment (secret agendas) and rule-class trumps
#   surfaces: AGENDAS, deal_agendas, verify_agendas, ARCANA, ArcanaModule
#   boundaries: no sequence (runner hooks), no field math (engine);
#     arcana effects mutate state through declared primitives only
#   tests: test_arcana_agendas.py
#   rollout: step 5c; completes the ruleset
#   rollback: omit arcana= param; skip deal_agendas
#   hmmm: FIRST-TIME VOTER's blind-draw-as-R deferred (SE shield only);
#     AUDIT compatibility is a coarse bool pending richer agenda algebra
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: agendas_verify_at_end
#   behavior: every dealt agenda is verified at match end against state
#     and log; ashes-mode verifies on loss as well as win
# id: agendas_organizer_counts_r
#   behavior: the organizer agenda holds only for the player with the
#     strictly greatest attributed r tally
# id: arcana_once_per_game
#   behavior: a player's second arcanum play never resolves
# id: arcana_wayseer_reveals
#   behavior: the wayseer logs the next two machine phases including
#     secret-effect presence, raises m by one, and alters nothing
# id: arcana_filibuster_suspends
#   behavior: filibuster suspends the next full rotation of machine
#     beats: no cards, no pmr, population unchanged
# id: arcana_term_limits_oldest
#   behavior: term limits removes the oldest card in play regardless of
#     side
# === END CONTRACTS ===
"""


AGENDAS = [
    {"name": "THE SURVIVOR", "kind": "population_floor", "floor": 50,
     "compatible": True},
    {"name": "THE ORGANIZER", "kind": "most_r", "compatible": True},
    {"name": "THE MACHINE POLITICIAN", "kind": "m_max", "m_max": 2,
     "compatible": False},
    {"name": "THE ARCHIVIST", "kind": "named_plays",
     "card": "DOCUMENT & SMUGGLE", "count": 3, "compatible": True},
    {"name": "THE QUIET BENEFICIARY", "kind": "static_stands",
     "static": "ARTICLE 48", "compatible": False},
    {"name": "THE EXILE", "kind": "laid_static",
     "static": "THE EXILE NETWORK", "compatible": True},
]


def deal_agendas(state, players, rng):
    pool = list(AGENDAS)
    rng.shuffle(pool)
    state.tallies["agendas"] = [pool[i % len(pool)] for i in range(players)]


def verify_agendas(state, outcome):
    verdicts = []
    r_by_pid = {}
    plays_by_pid = {}
    laid_by_pid = {}
    for ev in state.log:
        if ev[0] == "action":
            r_by_pid[ev[1]] = r_by_pid.get(ev[1], 0) + 1
            plays_by_pid.setdefault(ev[1], []).append(ev[2])
        if ev[0] == "static":
            laid_by_pid.setdefault(ev[1], []).append(ev[2])
    for pid, agenda in enumerate(state.tallies.get("agendas", [])):
        k = agenda["kind"]
        if k == "population_floor":
            held = state.population > agenda["floor"]
        elif k == "most_r":
            mine = r_by_pid.get(pid, 0)
            held = mine > 0 and all(v < mine for p, v in r_by_pid.items()
                                    if p != pid)
        elif k == "m_max":
            held = state.m <= agenda["m_max"]
        elif k == "named_plays":
            held = plays_by_pid.get(pid, []).count(agenda["card"]) \
                >= agenda["count"]
        elif k == "static_stands":
            held = any(s.get("name") == agenda["static"]
                       for s in state.in_play_statics)
        elif k == "laid_static":
            held = agenda["static"] in laid_by_pid.get(pid, [])
        else:
            held = False
        verdicts.append({"pid": pid, "agenda": agenda["name"],
                         "held": held, "outcome": outcome})
    return verdicts


ARCANA = [
    {"name": "THE FIRST-TIME VOTER", "num": 0},
    {"name": "THE WHISTLEBLOWER", "num": 2},
    {"name": "THE INJUNCTION", "num": 8},
    {"name": "THE WAYSEER", "num": 9},
    {"name": "THE ELECTION", "num": 10},
    {"name": "THE FILIBUSTER", "num": 12},
    {"name": "TERM LIMITS", "num": 13},
    {"name": "THE SCANDAL", "num": 16},
    {"name": "THE AUDIT", "num": 20},
]


class ArcanaModule:
    """Applies trumps. Public, attributed, once per player per game."""

    def __init__(self):
        self.used = set()

    def apply(self, arcanum, state, machine, engine, pid, players):
        name = arcanum.get("name")
        if pid in self.used:
            state.log.append(("arcana_refused", pid, name))
            return
        self.used.add(pid)
        state.log.append(("arcana", pid, name))
        if name == "THE WAYSEER":
            peek = machine.peek(2 * players) if hasattr(machine, "peek") \
                else []
            state.log.append(("wayseer_reveal",
                              [(c["id"], c["name"], bool(c.get("se")))
                               for c in peek]))
            state.m = min(5, state.m + 1)
        elif name == "THE WHISTLEBLOWER":
            pending = [s.get("name") for s in state.in_play_statics
                       if s.get("side") == "machine"]
            state.log.append(("whistleblower_reveal", pending))
        elif name == "THE INJUNCTION":
            targets = [s for s in state.in_play_statics
                       if s.get("side") == "machine"
                       and s.get("passive_s", 0) > 0]
            if targets:
                targets[0]["passive_s"] = 0
                targets[0]["frozen"] = True
                state.log.append(("injunction", targets[0]["name"]))
        elif name == "THE ELECTION":
            import random as _r
            ag = state.tallies.get("agendas", [])
            _r.Random(state.machine_beats).shuffle(ag)
            state.log.append(("election_reshuffle", len(ag)))
        elif name == "THE FILIBUSTER":
            state.suspend_beats += players
        elif name == "TERM LIMITS":
            if state.in_play_statics:
                gone = state.in_play_statics.pop(0)
                state.log.append(("term_limits", gone.get("name")))
        elif name == "THE SCANDAL":
            targets = [s for s in state.in_play_statics
                       if s.get("side") == "machine"]
            if targets:
                state.in_play_statics.remove(targets[-1])
                state.e += 4
                state.log.append(("scandal", targets[-1].get("name")))
        elif name == "THE FIRST-TIME VOTER":
            state.tallies["se_shield"] = state.tallies.get("se_shield", 0) \
                + players
            state.log.append(("se_shield", players))
        elif name == "THE AUDIT":
            ag = state.tallies.get("agendas", [])
            incompat = sum(1 for a in ag if not a.get("compatible"))
            state.m = max(0, min(5, state.m + (2 if incompat == 0
                                               else -incompat)))
            state.log.append(("audit", [a["name"] for a in ag]))

# ratios: loc_comments=119:51 imports_exports=2:3 calls_definitions=45:5
