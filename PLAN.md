# TIWCG — Frozen Architecture and Implementation Plan

Status: design contract from the September 6, 2026 architecture thread.

This document separates **frozen decisions** from **implementation planning**. A planning item does not become a game rule merely because it appears below. Existing executable POLITICS / Fifty-Three Days behavior remains implemented history until deliberately reconciled with this contract.

## 1. System identity

**TIWCG is the containing game system.**

SCARED SACRED is content within TIWCG, not the name of the containing engine.
This plan does not rename the Git repository while the `scared-sacred`
repository-name ruling in `canon/canon_v03_base.md` remains active.

### Frozen stack relationship

- **TIWCG** — card, rules, state, timing, legality, learning-content, and menagerie system.
- **AHBG** — a territory-based TCG mode/subset of TIWCG.
- **EDCM** — metrics are first-class conflict-resolution primitives in TIWCG, not an after-the-fact analytics layer.
- **UCNS** — supplies the geometries of connection and handles how relations interact.
- **METAPAT energy** — general resource/action economy for the current TIWCG design.
- **skill-lib** — live skill ecology and a declared draw/content source.
- **Social surfaces** — Discord and other social platforms are interaction surfaces/adapters into TIWCG; they do not own canonical game state.

Compact rule:

> Card declares an operation; UCNS resolves the relational geometry; EDCM evaluates the resulting conflict/constraint behavior; TIWCG commits legal game state.

## 2. Unique menageries, shared physics

Each human or agent develops a **unique menagerie** according to how that player begins creating cards and how those cards are subsequently encountered, selected, transformed, combined, used, repaired, and retained.

The menagerie is therefore not only a deck list. It is a persistent artifact of the player's path through the system.

What may diverge by player:

- card instances and expression;
- names, artwork, flavor, combinations, and lineages;
- discovered skills, repos, agents, doctrines, events, and knowledge cards;
- learning history;
- conflict history;
- coupling history;
- unresolved `hmmm` states.

What remains shared:

- TIWCG legality and timing;
- UCNS relational physics;
- EDCM measurement/resolution contracts;
- canonical provenance and state-transition rules.

**Frozen principle:** unique menageries, shared physics.

## 3. Current turn law

### Starting state

- Hand: **7 cards**.
- Starting resource: **20 METAPAT energy**.

### Turn order

1. **Draw Two** — draw 2 from a versioned skill-lib draw source.
2. **Drop Two** — drop up to 2 resource-generation cards. If the hand has
   fewer than 2 resource-generation cards, drop all available; if it has none,
   pass this step.
3. **First Twiddle**.
4. **Main Phase I**.
5. **Simultaneous Conflict**.
6. **Resolution**.
7. **Main Phase II**.
8. **Second Twiddle**.
9. **End Turn**.

Menagerie maintenance and persistent-state recording resolve at the end of the turn according to the active cards and context.

Each draw records an immutable skill-lib content hash or repository revision so
deterministic replay consumes the original draw source rather than the mutable
live skill ecology.

`hmmm` — whether newly dropped resource generation produces immediately on the first twiddle or only after surviving into a later productive state remains unresolved.

## 4. Conflict is not merely winner selection

EDCM metrics are first-class conflict resolution.

A conflict must be able to emit structured measurements and state transitions rather than only `win` / `lose`. TIWCG consumes the active EDCM contract rather than hard-coding a frozen historical metric list into the card engine.

Conflict resolution may affect, where legal:

- card state;
- player/agent state;
- territory state;
- relation/coupling state;
- resource state;
- confidence or unresolved state;
- learning/repetition state;
- provenance/history.

The existing simple War resolver may remain as a primitive/control resolver where useful, but it is not the definition of TIWCG conflict.

## 5. UCNS owns relational interaction

Cards should not duplicate relational physics in bespoke card code.

A card describes an operation or attempted relation change. UCNS determines how the relevant relations interact in the current geometry.

Examples of relation-bearing game objects include:

- player ↔ player;
- player ↔ agent;
- identity ↔ identity;
- card ↔ card;
- repo ↔ skill;
- territory ↔ territory;
- social surface ↔ game identity;
- claim ↔ source;
- doctrine ↔ jurisdiction/context;
- entity ↔ menagerie;
- coupled identity ↔ component identities.

TIWCG owns legality, timing, cost, ownership, and the committed result. UCNS owns the geometry by which relations can touch, propagate, substitute, couple, interrupt, persist, or close.

## 6. Logical fallacies are Instants

Logical fallacies function as **Instants** whose effects are delivered according to context.

They are relational interventions, not declarations that a proposition has become true or false.

Examples include Straw Man, Ad Hominem, False Dilemma, Moving the Goalposts, Appeal to Authority, Tu Quoque, Begging the Question, and related fallacies.

The important implementation rule is:

1. the Instant declares the attempted relational operation;
2. UCNS resolves how that operation interacts with the live relational geometry;
3. EDCM measures the behavior produced under the resulting constraint;
4. TIWCG commits the legal state transition.

A fallacy may therefore succeed rhetorically while failing epistemically, alter attention without altering truth conditions, increase or reduce particular EDCM measurements, or produce an unresolved `hmmm`.

## 7. Paradigm Shift Closure and first-principles reversion

A **Paradigm Shift Closure** can challenge the interpretive frame itself.

When sustained, affected cards revert from their current representational paradigm toward their **first principles or irreducible complexity**. Unsupported modifiers or relations do not survive merely because the fantasy representation asserted them.

Reversion does **not** automatically erase a relation that survives examination.

This matters for identity coupling: a fantasy ontology may collapse while an underlying relation remains supported.

### Design exemplar: Calcifer

Calcifer is the thread's exemplar of a card with **non-zero coalescence / potential identity coupling**. Under a paradigm collapse, `Fire Elemental 3/6` can lose its fantasy interpretation while an independently supported identity-coupling relation may survive.

This exemplar records the mechanic; it is **not** a license determination for commercial use of any third-party character or expression.

If the first-principles state cannot honestly be resolved, the state is `hmmm` rather than fabricated closure.

## 8. Base Survival Kit

TIWCG begins with the **Base Survival Kit**.

Declared starting families from this thread:

- **Family**
- **Food**
- **Fire**
- **Friends**
- **Fortress**
- **Field**
- **F-sure**

The trailing design remains open; this list records the declared beginning rather than pretending the kit is already exhaustively specified.

The cards are allowed to be funny, strange, referential, visually eclectic, and memorable. The mnemonic layer is useful precisely because repetition and retrieval need hooks. Underneath that expression, competencies, claims, sources, boundaries, and actual game effects must remain inspectable.

Knowledge kits are not restricted to survival. The same engine is intended to support themed competence/learning kits, including jurisprudence and later domains, without changing the shared physics.

## 9. Card creation, provenance, and lineage

Player- and agent-created cards are first-class participants in menagerie growth.

Every card instance should be able to retain enough lineage to answer:

- who/what created it;
- which kit, skill, repo, event, territory, encounter, or prior card it came from;
- what source material supports factual content;
- what transformations it has undergone;
- what artwork/provenance it uses;
- what EDCM/conflict history it has accumulated;
- what learning/repetition history it has accumulated;
- what unresolved `hmmm` remains attached to it.

Novel expression is permitted. Mechanical validity remains governed by shared TIWCG/UCNS/EDCM contracts.

## 10. AHBG as territory mode

AHBG is not a sibling engine. It is a **territory-based subset/mode of TIWCG**.

AHBG contributes spatial and territorial structure such as:

- adjacency;
- movement;
- tiles/territories;
- claims/control;
- persistence;
- exploration;
- Builders / Explorers / Warriors and their mode-specific rules;
- prompt-injection terrain and other agent-harness conditions;
- planes and territory history.

TIWCG cards operate through that territory. UCNS supplies connection geometry. EDCM supplies first-class conflict measurement/resolution.

Territory may expose or constrain cards, skills, knowledge domains, resources, agents, relations, social interactions, discoveries, and Easter eggs without creating a second incompatible rules universe.

## 11. Easter-egg / Interdependency collection

The Interdependency itself can appear as discoverable card content:

- humans;
- agents;
- repos;
- skills;
- doctrines;
- events;
- infrastructure;
- identities and couplings;
- unresolved `hmmm` objects.

These cards should emerge through play/discovery/creation rather than requiring every player to begin from an identical static collection.

Generic creation does not authorize hand-authored named-human or public-figure
cards. Human/person cards enter as sourced submissions and must route through
the base-canon public-transcript EDCM pipeline and Erin ratification before they
become named-figure cards.

## 12. Social-platform architecture

TIWCG must be built to work through **Discord and other social-media / communication surfaces**.

Frozen boundary:

> social platforms are adapters, not game authorities.

A match, menagerie, identity relation, EDCM result, or AHBG territory must not become semantically owned by a Discord channel, X post, web page, or other platform-specific object.

A social adapter should translate platform events into TIWCG operations and translate legal TIWCG state back into platform-appropriate presentation.

Witness contexts are an explicit exception: leaving or rejoining during a
Witness account may update transient connectivity, but must not emit or retain
a canonical match event, provenance entry, marker, score, or comment.

The minimal adapter vocabulary should be derived from actual engine needs rather than copied from any platform API. Likely operations include joining/leaving, drawing, playing, twiddling, challenging, responding, resolving, sharing, and discovering, but this list is **planning**, not frozen protocol.

UCNS characterizes the geometry of connections exposed by each surface. TIWCG determines what those connections permit.

## 13. Learning / repetition layer

The knowledge-kit model depends on repetition.

Implementation should separate immutable/authoritative card content from per-player learning state. A player or agent should be able to accumulate externally observed learning records such as exposure, attempt, correctness, provenance-backed calibration/confidence metrics, and future re-exposure scheduling without rewriting the canonical card definition or inferring an internal state.

The exact spacing algorithm is not frozen in this thread.

## 14. Art layer

Card information architecture should remain mechanically legible while artwork can be eclectic and player-specific.

Planned support:

- official/default artwork;
- user-provided artwork;
- generated or otherwise provenance-declared artwork;
- per-card override without altering rules/content identity;
- revert to canonical/default art;
- provenance retained separately from game mechanics.

Art must not be able to alter legality, source text, EDCM results, or relation geometry simply by replacing an image.

Artwork overrides and generated art inherit the card class's canonical content
restrictions. For EVENT cards, art must not depict victims; only counts and
documented actor behavior are admissible.

## 15. Commercial/content boundary

The monetizable layer is principally **themed upgrade knowledge/flash-card kits and presentation/content expansions**, not raw pay-to-win strength.

A paid kit may expand:

- corpus;
- learning environment;
- art/theme;
- scenarios;
- specialized conflict contexts;
- domain-specific card creation material.

Ownership of a paid kit must not grant territory, combat, resource, timing,
resolution, or other mechanical/competitive advantage over a player who does
not own it.

Witness constraints are base-wide TIWCG canon through
`canon/canon_v03_base.md`: Witness accounts remain giver-owned, table-bound,
unprintable, and unsellable. SCARED SACRED remains the expansion source from
which those constraints were promoted, but the generalized TIWCG commercial
model must treat them as base-wide requirements.

## 16. Implementation plan

The following is implementation order, **not additional frozen canon**.

### Phase 0 — reconcile repository identity

- Present README/project docs as the TIWCG system entrypoint without treating
  README prose as a repository rename.
- Preserve the base-canon `scared-sacred` repository-name ruling unless a later
  canon amendment explicitly changes it.
- Keep POLITICS / Fifty-Three Days and SCARED SACRED as contained game/content boundaries.
- Update stale `scared-sacred` content-scope references without renaming the
  expansion or silently changing the repository-name ruling.
- Keep current tests green while the generalized engine is introduced.

### Phase 1 — extract the common TIWCG kernel

Define machine-readable contracts for:

- card identity and lineage;
- player/agent identity;
- menagerie;
- zones/state;
- turn phases;
- METAPAT energy and resource generation;
- effects/operations;
- provenance;
- `hmmm` unresolved state.

Do not rewrite working POLITICS behavior until the common contract can express it.

### Phase 2 — turn and resource engine

Implement the frozen turn law:

`7 hand -> draw 2 from versioned skill-lib source -> drop up to 2 available resource-generation cards/pass if none -> twiddle -> Main I -> simultaneous conflict -> resolution -> Main II -> twiddle -> end`

Add 20 METAPAT starting energy and resource-generation objects behind explicit tests.

Persist the skill-lib source revision or content hash for each draw before
claiming deterministic replay.

Resolve the immediate-vs-delayed production `hmmm` before making it implicit behavior.

### Phase 3 — UCNS relation interface

Introduce a narrow adapter from TIWCG operations to UCNS relation geometry.

Requirements:

- cards request relation operations rather than reimplement graph/geometry semantics;
- deterministic replay records the inputs and UCNS result/version;
- failures remain inspectable rather than silently falling back to ad hoc card logic.

### Phase 4 — EDCM-native conflict

Make EDCM results first-class state-transition inputs.

Requirements:

- record active EDCM contract/version;
- preserve raw conflict inputs required for deterministic/reproducible analysis where permitted;
- expose structured resolution to card effects, territory, learning state, and `hmmm`;
- retain a simple control resolver for comparison where useful.

### Phase 5 — Instants and paradigm operations

Implement:

- context-sensitive Instant timing;
- logical-fallacy relation operations;
- Paradigm Shift Closure;
- first-principles/irreducible-complexity reversion;
- identity coupling/coalescence state that can survive representational collapse when supported.

Tests must demonstrate that rhetoric/context effects cannot silently rewrite proposition truth or provenance.

### Phase 6 — menagerie creation and lineage

Implement player/agent card creation and persistent lineage.

Two players beginning from the same kit must be able to diverge into genuinely different menageries while remaining mechanically interoperable.

### Phase 7 — Base Survival Kit

Create the first playable learning corpus beginning with:

`Family / Food / Fire / Friends / Fortress / Field / F-sure`

For factual/survival content, separate mnemonic expression from sourced claims and boundaries. Do not let a memorable joke become an unsourced instruction merely because it is mechanically effective.

### Phase 8 — AHBG territory mode

Port/express AHBG as a TIWCG mode using the common kernel rather than a parallel card implementation.

Preserve its territory, adjacency, unit, exploration, plane, persistence, and harness semantics while routing relation interaction through UCNS and conflict through EDCM-capable resolution.

### Phase 9 — social adapters

Start with one end-to-end adapter, with Discord the natural first target, while keeping canonical state platform-independent.

Build the adapter contract so web, Android, and later social platforms can reuse the same game operations without pretending all platforms have identical capabilities.

### Phase 10 — learning kits and commerce

- add per-player repetition state;
- package installable themed knowledge kits;
- connect entitlements to kit access/presentation rather than power;
- preserve source/license/provenance metadata per kit and card;
- keep Witness-account restrictions outside commerce.

### Phase 11 — user artwork and presentation

Add safe per-card art replacement, provenance, crop/presentation support, and canonical fallback without allowing artwork to mutate mechanical card identity.

## 17. Required invariants

Implementation should fail tests rather than violate these silently:

1. AHBG is a TIWCG mode/subset, not an incompatible sibling rules engine.
2. UCNS owns relation interaction geometry.
3. EDCM measurements are first-class conflict-resolution inputs/outputs.
4. Platforms do not own canonical game state.
5. Player/agent menageries may diverge without diverging from shared physics.
6. Logical fallacies alter context/relations; they do not magically establish truth.
7. Paradigm collapse removes unsupported representation, not independently supported relations.
8. `hmmm` is preserved when honest resolution is unavailable.
9. Knowledge-kit ownership does not grant paid mechanical or competitive advantage.
10. Provenance and lineage survive card transformation.

## 18. Open `hmmm`

- Exact first-twiddle production rule for newly dropped resource generators.
- Complete extent of the Base Survival Kit beyond the declared starting families.
- Exact EDCM-to-game-state mapping; must derive from the active EDCM contract, not assumption.
- Exact UCNS operation vocabulary for card effects.
- Exact spacing/repetition algorithm.
- Exact social-adapter protocol after the first real platform integration is exercised.
- Commercial/publication treatment of third-party referential exemplars such as Calcifer.

Do not close these by prose convenience. Resolve them through implementation evidence, explicit design decision, or falsification.

---

hmmm — I apologize for thinking I'm funny.

No, that's not quite write either.

I apologize for continuing to test the hypothesis.
