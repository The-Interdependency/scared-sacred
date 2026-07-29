import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "the organizer agenda holds only for the player with the"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "agendas_organizer_counts_r"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "every dealt agenda is verified at match end against state"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "agendas_verify_at_end"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "beats": "no cards, no pmr, population unchanged",
        "behavior": "filibuster suspends the next full rotation of machine"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "arcana_filibuster_suspends"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "a player's second arcanum play never resolves"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "arcana_once_per_game"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "term limits removes the oldest card in play regardless of"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "arcana_term_limits_oldest"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "the wayseer logs the next two machine phases including"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "arcana_wayseer_reveals"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "no sequence (runner hooks), no field math (engine);",
        "hmmm": "FIRST-TIME VOTER's blind-draw-as-R deferred (SE shield only);",
        "purpose": "non-alignment (secret agendas) and rule-class trumps",
        "rollback": "omit arcana= param; skip deal_agendas",
        "rollout": "step 5c; completes the ruleset",
        "surfaces": "AGENDAS, deal_agendas, verify_agendas, ARCANA, ArcanaModule",
        "tests": "test_arcana_agendas.py"
      },
      "file": "engine/arcana_agendas_v1.py",
      "id": "arcana_agendas_v1"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "read-only over data modules; overwrites cards/ tree",
        "hmmm": "art status flips by file presence, not by validation record --",
        "purpose": "cards as first-class repo files; art drop-in slots",
        "rollback": "delete cards/ tree; data modules unaffected",
        "rollout": "run per data change; committed output is canon-derived",
        "surfaces": "export(root) -> index dict; __main__ CLI",
        "tests": "self-verifying counts on run (index vs files written)"
      },
      "file": "engine/cards_export.py",
      "id": "cards_export_v01"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "the civil service law converts THE COURTS from player"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_courts_flip"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "decks outside 40-59/60-79/80-99 are illegal"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_deck_tier_law"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "destroying a machine card or static causes every later"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_destruction_feeds_prereqs"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "with the coalition marker in play and m >= needs_m, the"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_hinge_reprices"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "at m <= 1 stacking effects apply twice"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_se_doubles_at_low_m"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "a secret effect resolves only when e >= a_se; a gated"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_se_gated_by_e"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "no sequence (runner), no field math (engine), no",
        "hmmm": "eats_statics (Gleichschaltung) consumes the strongest standing",
        "purpose": "card mechanics for scripted sets; deck legality",
        "rollback": "feed bare S dicts to ScriptedMachine",
        "rollout": "build step 4; ScriptedMachine retained for A/B",
        "surfaces": "WeimarMachine, field_totals, validate_deck, NOOP_EFFECTS",
        "tests": "test_cards_v1.py"
      },
      "file": "engine/cards_v1.py",
      "id": "cards_v1"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "measurement only; no tuning decisions encoded; policies",
        "hmmm": "agenda pursuit not yet modeled in selfish policy; squad is",
        "purpose": "measure win-rate spectrum across coordination levels",
        "rollback": "delete; balance claims regress to conjectural",
        "rollout": "step 5a; feeds every future balance claim",
        "surfaces": "spectrum, run_match, policies (Null/Selfish/Noisy/Squad)",
        "tests": "smoke via __main__ spectrum run"
      },
      "file": "engine/harness_v1.py",
      "id": "harness_v1"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "ambient repair lowers velocity but never un-converts a"
      },
      "file": "engine/inertial_engine.py",
      "id": "engine_conversion_is_hysteretic"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "under constant strain, conversions in the first quarter of"
      },
      "file": "engine/inertial_engine.py",
      "id": "engine_inertia_resists_early"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "state.population always equals unconverted person count"
      },
      "file": "engine/inertial_engine.py",
      "id": "engine_population_matches_field"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "identical script with nonzero R converts later or not at all"
      },
      "file": "engine/inertial_engine.py",
      "id": "engine_repair_slows_collapse"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "no card knowledge; registration only (persons never",
        "hmmm": "mass bands and seed distribution are claude-defaults pending",
        "purpose": "replace scalar population with an inertial vector field",
        "rollback": "pass LeakyEngine back to MatchRunner",
        "rollout": "build-order step 2 organ swap; LeakyEngine retained for A/B",
        "surfaces": "InertialEngine.pmr, Person, weimar_seed, engine.curve",
        "tests": "test_inertial_engine.py"
      },
      "file": "engine/inertial_engine.py",
      "id": "inertial_engine_v01"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "when the rules module computes field totals, machine-beat"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_field_totals_delegation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "in hand mode, a play resolves only from the hand holding"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_hand_law"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "strain and m deltas reported by rules.interference are"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_interference_passthrough"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "match ends in loss the moment population <= 50"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_loss_at_half"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "with null players the match always ends in loss in finite"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_null_clock_terminates"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "after a machine card reveals and before its PMR, players"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_reaction_window"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "population is reduced only on machine beats; player beats"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_registration_machine_only"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "plays failing the rules module are dropped silently; the"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_rejects_illegal_plays"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "after each full rotation the runner applies the rules"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_rotation_boundary_hooks"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "machine beats open the match and follow every player turn"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_sequence_interleaved"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "while suspend_beats > 0 a machine beat consumes the"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_suspension_primitive"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "match ends in win when the machine deck is exhausted and"
      },
      "file": "engine/politics_runner.py",
      "id": "runner_win_on_empty_deck"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "no game math, no card knowledge, no advice to players;",
        "hmmm": "player-beat PMR without registration is claude-default pending",
        "purpose": "own the interleaved turn sequence; delegate all game logic",
        "rollback": "pure stdlib, no persistence; delete file to remove",
        "rollout": "step 1 of ratified build order; stubs replaced organ by organ",
        "surfaces": "MatchRunner.run, GameState, TurnPlays, module protocols",
        "tests": "test_politics_runner.py (CHECKS reconcile CONTRACTS below)"
      },
      "file": "engine/politics_runner.py",
      "id": "politics_runner_v01"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "shared declared target across one rotation yields m+1,"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_coalition_window"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "tempo discards plus reach burn never exceed declared"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_discard_budget"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "an action is legal iff e >= a - m - burn; otherwise"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_gate_a_minus_m"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "effective r decays by one per two prior table-wide plays"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_habituation_decay"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "player-targeted plays report strain equal to their a and"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_interference_priced"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "reclamation requires e at or above the reclaiming static's"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_reclaim_priced"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "only reclaiming statics reclaim, at most one vector per"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_reclaims_gated"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "reflex legality evaluates a - m against e plus the"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_reflex_gate_uses_incoming"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "legality and pricing only; no game state mutation; no",
        "hmmm": "agenda-floor enforcement deferred to match-end module; scale",
        "purpose": "activation gating, turn grammar, targeting, interference,",
        "rollback": "pass rules=None to MatchRunner",
        "rollout": "build step 3; PermissiveRules retained for A/B",
        "surfaces": "RulesV1.legal, validate_turn, interference, coalition,",
        "tests": "test_rules_v1.py"
      },
      "file": "engine/rules_v1.py",
      "id": "rules_v1"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "agendas_verify_at_end"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_agendas_verify_at_end"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "arcana_once_per_game"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_arcana_once"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "arcana_filibuster_suspends, runner_suspension_primitive"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_filibuster"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_habituation_decay"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_habituation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "agendas_organizer_counts_r"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_organizer_counts_r"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_reclaim_priced"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_reclaim_priced"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "arcana_term_limits_oldest"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_term_limits"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "arcana_wayseer_reveals"
      },
      "file": "engine/test_arcana_agendas.py",
      "id": "check_wayseer"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_courts_flip"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_courts_flip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_deck_tier_law"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_data_integrity"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_destruction_feeds_prereqs"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_destruction_feeds_prereqs"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_se_gated_by_e, runner_field_totals_delegation"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_full_match_runs"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_hinge_reprices"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_hinge_reprices"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_se_doubles_at_low_m"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_se_doubles_at_low_m"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_se_gated_by_e"
      },
      "file": "engine/test_cards_v1.py",
      "id": "check_se_gated_by_e"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "engine_conversion_is_hysteretic"
      },
      "file": "engine/test_inertial_engine.py",
      "id": "check_conversion_is_hysteretic"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "engine_inertia_resists_early"
      },
      "file": "engine/test_inertial_engine.py",
      "id": "check_inertia_resists_early"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "engine_population_matches_field"
      },
      "file": "engine/test_inertial_engine.py",
      "id": "check_population_matches_field"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "engine_repair_slows_collapse"
      },
      "file": "engine/test_inertial_engine.py",
      "id": "check_repair_slows_collapse"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_loss_at_half"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_loss_at_half"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_null_clock_terminates"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_null_clock_terminates"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_registration_machine_only"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_registration_machine_only"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_rejects_illegal_plays"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_rejects_illegal_plays"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_sequence_interleaved"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_sequence_interleaved"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_win_on_empty_deck"
      },
      "file": "engine/test_politics_runner.py",
      "id": "check_win_on_empty_deck"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_reaction_window"
      },
      "file": "engine/test_reserve_reflex.py",
      "id": "check_counter_intercepts_se"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "runner_hand_law"
      },
      "file": "engine/test_reserve_reflex.py",
      "id": "check_hand_law"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_reflex_gate_uses_incoming"
      },
      "file": "engine/test_reserve_reflex.py",
      "id": "check_reflex_gate_uses_incoming"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "cards_destruction_feeds_prereqs"
      },
      "file": "engine/test_reserve_reflex.py",
      "id": "check_reserve_replaces_skip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_reflex_gate_uses_incoming"
      },
      "file": "engine/test_reserve_reflex.py",
      "id": "check_wels_reflex_only_m15"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_coalition_window, runner_rotation_boundary_hooks"
      },
      "file": "engine/test_rules_v1.py",
      "id": "check_coalition_window"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_discard_budget"
      },
      "file": "engine/test_rules_v1.py",
      "id": "check_discard_budget"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_gate_a_minus_m"
      },
      "file": "engine/test_rules_v1.py",
      "id": "check_gate_a_minus_m"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_interference_priced, runner_interference_passthrough"
      },
      "file": "engine/test_rules_v1.py",
      "id": "check_interference_priced"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "rules_reclaims_gated"
      },
      "file": "engine/test_rules_v1.py",
      "id": "check_reclaims_gated"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "data only, zero behavior; mechanics live in cards_v1",
        "hmmm": "ERRATA vs prose set: its \"=40\" checksum was false (true sum 37);",
        "purpose": "the set as data; single source for machine + response piles",
        "rollback": "delete; machine stub falls back to bare S values",
        "rollout": "build step 4; regenerated whenever the prose set changes",
        "surfaces": "MACHINE_SCRIPT, SETUP_STATICS, RESPONSE_DECK, WEIMAR_OPENING",
        "tests": "test_cards_v1.py (integrity block)"
      },
      "file": "engine/weimar_data.py",
      "id": "weimar_data_v01"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "/act with a card index outside the hand is refused without"
      },
      "file": "render/serve.py",
      "id": "serve_act_enforces_hand_law"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "with null input the worker thread ends the match on the"
      },
      "file": "render/serve.py",
      "id": "serve_match_thread_completes"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "behavior": "/state returns tracks, board, hand, awaiting flag, and log"
      },
      "file": "render/serve.py",
      "id": "serve_state_reports_truth"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "boundaries": "no game logic (engine/rules own truth); no advice;",
        "hmmm": "reaction-window UI is prompt-only v1; multiplayer seats wait",
        "purpose": "playable top-down table over the real engine; art live",
        "rollback": "delete render/; engine untouched",
        "rollout": "first sit-down vehicle; tutorial == this, per ruling 6",
        "surfaces": "HTTP / (board), /state, /act, /react; HumanSeat",
        "tests": "test_serve.py (state contract; no browser needed)"
      },
      "file": "render/serve.py",
      "id": "render_serve_v01"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "serve_act_enforces_hand_law"
      },
      "file": "render/test_serve.py",
      "id": "check_act_enforces_hand_law"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "serve_match_thread_completes"
      },
      "file": "render/test_serve.py",
      "id": "check_match_thread_completes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "witnesses": "serve_state_reports_truth"
      },
      "file": "render/test_serve.py",
      "id": "check_state_reports_truth"
    }
  ],
  "edges": [
    {
      "from": "arcana_agendas_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "arcana_agendas_v1",
      "to": "no field math (engine);"
    },
    {
      "from": "arcana_agendas_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "arcana_agendas_v1",
      "to": "no sequence (runner hooks)"
    },
    {
      "from": "cards_export_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "cards_export_v01",
      "to": "read-only over data modules; overwrites cards/ tree"
    },
    {
      "from": "cards_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "cards_v1",
      "to": "no"
    },
    {
      "from": "cards_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "cards_v1",
      "to": "no field math (engine)"
    },
    {
      "from": "cards_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "cards_v1",
      "to": "no sequence (runner)"
    },
    {
      "from": "harness_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "harness_v1",
      "to": "measurement only; no tuning decisions encoded; policies"
    },
    {
      "from": "inertial_engine_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "inertial_engine_v01",
      "to": "no card knowledge; registration only (persons never"
    },
    {
      "from": "politics_runner_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "politics_runner_v01",
      "to": "no advice to players;"
    },
    {
      "from": "politics_runner_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "politics_runner_v01",
      "to": "no card knowledge"
    },
    {
      "from": "politics_runner_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "politics_runner_v01",
      "to": "no game math"
    },
    {
      "from": "render_serve_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "render_serve_v01",
      "to": "no game logic (engine/rules own truth); no advice;"
    },
    {
      "from": "rules_v1",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "rules_v1",
      "to": "legality and pricing only; no game state mutation; no"
    },
    {
      "from": "weimar_data_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "weimar_data_v01",
      "to": "data only"
    },
    {
      "from": "weimar_data_v01",
      "kind": "risk",
      "source_block": "MODULE_BUILD",
      "source_id": "weimar_data_v01",
      "to": "zero behavior; mechanics live in cards_v1"
    }
  ],
  "gaps": [],
  "repo": "The-Interdependency/scared-sacred"
});
