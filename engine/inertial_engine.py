# ratios: loc_comments=55:62 imports_exports=5:3 calls_definitions=19:6
"""inertial_engine — population as a field of person-vectors with inertia.

Each person is a vector: position x in [-1, +1] (repair pole to converted
pole), velocity v, and inertia mass m. Tension E is a field; per machine
PMR it applies force to every unconverted person: dv = k*E/m, damped, then
x += v. A person converts when x crosses +1 (hysteresis: conversion is a
registration, not a mood — reversing a convert requires targeted repair,
not ambient calm). state.population = count of unconverted persons, so the
runner needs no change: the organ swaps under the same interface.

Opening orientations are seeded from the L1 substrate — for Weimar, the
Nov 1932 Reichstag returns place ~33% already leaning at the converted
pole before turn one. The electorate's real distribution is the board.

Usage Guidance
--------------
    from politics_runner import MatchRunner, ScriptedMachine, NullPlayer, GameState
    from inertial_engine import InertialEngine, weimar_seed
    eng = InertialEngine(persons=weimar_seed(100, rng_seed=157))
    r = MatchRunner(eng, ScriptedMachine(script), [NullPlayer()]*3,
                    GameState(population=100, e=5, m=1))
    res = r.run()          # collapse curve in eng.curve, one point per PMR

Tuning knobs: coupling k, damping d, saturation e0 (force = k*tanh(E/e0):
fields saturate; terror at E=40 is not 4x terror at E=10), mass bands.
Calibration v2 [test-backed, harness 25 seeds]: defaults k=0.006 d=0.8
e0=8 eta=0.7, cooling on machine (time) beats only. Null play loses 100%
of seeds (ratified spec: without human interference the population ends
wholly converted), mean collapse beat 34. OPEN BALANCE ITEM, measured:
steady repair policies (selfish/noisy/squad) currently win ~100% -- the
repair side over-performs once any R flows; pricing this down without
breaking the null guarantee is the standing target. Harness numbers
accompany every future claim. All other numbers [conjectural].

# === MODULE_BUILD ===
# id: inertial_engine_v01
#   purpose: replace scalar population with an inertial vector field
#   surfaces: InertialEngine.pmr, Person, weimar_seed, engine.curve
#   boundaries: no card knowledge; registration only (persons never
#     "decide" — threshold crossings per AP-5); runner untouched
#   tests: test_inertial_engine.py
#   rollout: build-order step 2 organ swap; LeakyEngine retained for A/B
#   rollback: pass LeakyEngine back to MatchRunner
#   hmmm: mass bands and seed distribution are claude-defaults pending
#     Erin; reclaim now wired via runner rotation hook (ledger item 4)
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: engine_inertia_resists_early
#   behavior: under constant strain, conversions in the first quarter of
#     beats are fewer than in the last quarter (sigmoid, not linear)
# id: engine_conversion_is_hysteretic
#   behavior: ambient repair lowers velocity but never un-converts a
#     crossed person
# id: engine_population_matches_field
#   behavior: state.population always equals unconverted person count
# id: engine_repair_slows_collapse
#   behavior: identical script with nonzero R converts later or not at all
# === END CONTRACTS ===
"""

import math
import random
from dataclasses import dataclass


@dataclass
class Person:
    x: float      # orientation: -1 repair pole .. +1 converted pole
    v: float      # angular velocity
    m: float      # inertia mass
    converted: bool = False


def weimar_seed(n=100, rng_seed=157):
    """Seed orientations from the Nov 1932 substrate: ~33% leaning at the
    converted pole, the rest distributed across the field. Mass bands:
    20% anchored (m=4), 60% movable (m=2), 20% volatile (m=1)."""
    rng = random.Random(rng_seed)
    persons = []
    for i in range(n):
        if i < n * 0.33:
            x = rng.uniform(0.4, 0.9)      # already leaning
        else:
            x = rng.uniform(-0.9, 0.3)
        band = rng.random()
        m = 4.0 if band < 0.2 else (2.0 if band < 0.8 else 1.0)
        persons.append(Person(x=x, v=0.0, m=m))
    return persons


class InertialEngine:
    """Field engine. Same pmr interface as LeakyEngine; runner unchanged."""

    def __init__(self, persons, coupling=0.006, damping=0.8, saturation=8.0,
                 eta=0.7):
        self.persons = persons
        self.k = coupling
        self.d = damping
        self.e0 = saturation   # field saturation: force = k*tanh(E/e0)
        self.eta = eta         # repair efficiency (canon: E += S - eta*R)
        self.curve = []            # (beat_index, unconverted) per PMR

    def pmr(self, state, s_total, r_total, registration):
        state.e = max(0, round(state.e + s_total - self.eta * r_total, 6))
        if registration:                     # cooling is time; time is the
            cooling = 2 if state.m >= 4 else 1   # machine beat, not the play
            state.e = max(0, state.e - cooling)
        force = self.k * math.tanh(state.e / self.e0)
        for p in self.persons:
            if p.converted:
                continue
            p.v = self.d * p.v + force / p.m
            if r_total and not registration:
                p.v -= self.k * r_total / p.m        # repair decelerates
            p.x += p.v
            if p.x >= 1.0:
                p.converted = True                   # hysteresis: crossed
        state.population = sum(1 for p in self.persons if not p.converted)
        self.curve.append((len(self.curve), state.population))
        return state

    def reclaim(self, state, n):
        """Targeted repair: un-convert up to n crossed vectors, nearest
        the threshold first. Costed upstream by rules; the engine only
        performs the registration. Reclaimed vectors keep their mass and
        return just inside the line with zero velocity."""
        crossed = sorted((p for p in self.persons if p.converted),
                         key=lambda p: p.x)
        for p in crossed[:n]:
            p.converted = False
            p.x, p.v = 0.95, 0.0
        state.population = sum(1 for p in self.persons if not p.converted)

# ratios: loc_comments=55:62 imports_exports=5:3 calls_definitions=19:6
