# ratios: loc_comments=93:31 imports_exports=2:0 calls_definitions=0:0
"""weimar_data — Fifty-Three Days, the set as executable data.

Transcription of decks/weimar_53_days_v01.md into card dicts. Prose is
canon; this file is its compilation target. Any divergence is a bug in
THIS file. All balance numbers [conjectural]; history [test-backed].

Machine card fields: id, date, name, s, static (persists; passive_s /
debuff_response / blocks / event_buff), se {a_se, kind, ...}, prereq
(skipped if that id was destroyed), destroys [response names], hinge.
Response fields: name, kind, copies, r, a, passive_r, reclaims,
blocked_by, a_extra_while, persists_marker.

Usage Guidance
--------------
    from weimar_data import MACHINE_SCRIPT, SETUP_STATICS, RESPONSE_DECK
    from cards_v1 import WeimarMachine, build_response_pile
Feed MACHINE_SCRIPT to WeimarMachine; SETUP_STATICS go into
state.in_play_statics before beat one; RESPONSE_DECK expands by copies
into the player draw pile. Integrity checks: test_cards_v1.py.

# === MODULE_BUILD ===
# id: weimar_data_v01
#   purpose: the set as data; single source for machine + response piles
#   surfaces: MACHINE_SCRIPT, SETUP_STATICS, RESPONSE_DECK, WEIMAR_OPENING
#   boundaries: data only, zero behavior; mechanics live in cards_v1
#   tests: test_cards_v1.py (integrity block)
#   rollout: build step 4; regenerated whenever the prose set changes
#   rollback: delete; machine stub falls back to bare S values
#   hmmm: ERRATA vs prose set: its "=40" checksum was false (true sum 37);
#     NEIGHBORHOOD/LEAFLET/DOCUMENT bumped +1 each to honest 40. Also:
#     M10 extra-card, M35 window, X2 once-per-rotation buff are
#     logged no-ops this version — honest incompletion, listed in
#     cards_v1 NOOP_EFFECTS
# === END MODULE_BUILD ===
"""

SETUP_STATICS = [
    {"name": "ARTICLE 48", "side": "machine", "passive_s": 1,
     "untargetable_while_e": 3},
    {"name": "THE CAMARILLA", "side": "machine", "passive_s": 0},   # buff: noop v1
    {"name": "SIX MILLION UNEMPLOYED", "side": "machine", "passive_s": 0},
]

WEIMAR_OPENING = {"population": 100, "e": 5, "m": 1}

MACHINE_SCRIPT = [
 {"id":"M01","date":"1933-01-30","name":"THE BACKROOM KINGMAKER","s":2,
  "se":{"a_se":2,"kind":"chain"}},
 {"id":"M02","date":"1933-02-01","name":"DISSOLUTION","s":1,"prereq":"X_A48"},
 {"id":"M03","date":"1933-02-04","name":"DECREE FOR THE PROTECTION OF THE GERMAN PEOPLE","s":2,
  "se":{"a_se":4,"kind":"timed_debuff","target":"THE FREE PRESS","amount":2,"beats":3}},
 {"id":"M04","date":"1933-02-17","name":"THE SHOOTING ORDER","s":2},
 {"id":"M05","date":"1933-02-22","name":"THE DEPUTIZED STREET","s":2,"prereq":"M04"},
 {"id":"M06","date":"1933-02-24","name":"THE LIEBKNECHT HOUSE RAID","s":1,
  "se":{"a_se":3,"kind":"arm_next","amount":1}},
 {"id":"M07","date":"1933-02-27","name":"THE FIRE OPPORTUNIST","s":3,
  "se":{"a_se":5,"kind":"chain","delay_if_gated":1}},
 {"id":"M08","date":"1933-02-28","name":"THE FIRE DECREE","s":2,"prereq":"M07",
  "static":{"passive_s":2,"debuff_response":1}},
 {"id":"M09","date":"1933-03-03","name":"THE THAELMANN ARREST","s":1},
 {"id":"M10","date":"1933-03-05","name":"THE 43.9% ELECTION","s":2,
  "se":{"a_se":3,"kind":"noop_extra_card"}},
 {"id":"M11","date":"1933-03-08","name":"THE STATE SEIZURES","s":2,"prereq":"M08"},
 {"id":"M12","date":"1933-03-13","name":"THE MINISTRY OF PUBLIC ENLIGHTENMENT","s":2,
  "prereq":"M10","static":{"event_buff":1}},
 {"id":"M13","date":"1933-03-20","name":"DACHAU ANNOUNCED","s":2},
 {"id":"M14","date":"1933-03-21","name":"THE DAY OF POTSDAM","s":1,
  "se":{"a_se":2,"kind":"buff_next","amount":1}},
 {"id":"M15","date":"1933-03-23","name":"THE LEGALIST COUP (ENABLING ACT)","s":3,
  "hinge":{"needs_marker":"THE COALITION VOTE","needs_m":3,"fail_s":0,
           "reprice_rest":1}},
 {"id":"M16","date":"1933-04-01","name":"THE BOYCOTT","s":2},
 {"id":"M17","date":"1933-04-07","name":"THE CIVIL SERVICE LAW","s":2,
  "se":{"a_se":4,"kind":"flip_static","target":"THE COURTS","to_passive_s":1}},
 {"id":"M18","date":"1933-04-26","name":"THE SECRET STATE POLICE","s":1,
  "static":{"passive_s":1,"name_alias":"GESTAPO"}},
 {"id":"M19","date":"1933-05-01","name":"THE STOLEN HOLIDAY","s":1,
  "se":{"a_se":2,"kind":"chain"}},
 {"id":"M20","date":"1933-05-02","name":"THE UNION SEIZURE","s":3,
  "destroys":["THE UNIONS (ADGB)"]},
 {"id":"M21","date":"1933-05-10","name":"THE BOOK FIRES","s":1,
  "se":{"a_se":3,"kind":"timed_debuff","target":"*choice*","amount":1,"beats":99}},
 {"id":"M22","date":"1933-06-22","name":"THE SPD BAN","s":2,"prereq":"M15",
  "destroys":["REICHSBANNER / IRON FRONT"]},
 {"id":"M23","date":"1933-07-05","name":"THE SELF-DISSOLUTIONS","s":2},
 {"id":"M24","date":"1933-07-14","name":"THE ONE-PARTY STATE","s":1,
  "static":{"passive_s":1,"blocks":"THE COALITION VOTE"}},
 {"id":"M25","date":"1933-07-20","name":"THE CONCORDAT","s":1,
  "se":{"a_se":2,"kind":"perm_debuff","target":"THE PULPITS","amount":1}},
 {"id":"M26","date":"1933-09-22","name":"THE CULTURE CHAMBER","s":1,"prereq":"M12"},
 {"id":"M27","date":"1933-10-14","name":"THE LEAGUE EXIT","s":1},
 {"id":"M28","date":"1933-11-12","name":"THE 92% BALLOT","s":2},
 {"id":"M29","date":"1933-11-30","name":"GESTAPO LAW","s":1},
 {"id":"M30","date":"1933-12-01","name":"PARTY AND STATE UNITY LAW","s":1},
 {"id":"M31","date":"1934-01-26","name":"THE POLISH SURPRISE","s":1},
 {"id":"M32","date":"1934-01-30","name":"THE RECONSTRUCTION ACT","s":2,"prereq":"M11"},
 {"id":"M33","date":"1934-02-24","name":"THE PEOPLE'S COURT ANNOUNCED","s":1,"prereq":"M17"},
 {"id":"M34","date":"1934-04-20","name":"HIMMLER TAKES THE GESTAPO","s":1,"prereq":"M18"},
 {"id":"M35","date":"1934-06-17","name":"THE MARBURG SPEECH","s":0,
  "se":{"a_se":5,"kind":"noop_window"}},
 {"id":"M36","date":"1934-06-30","name":"THE PURGE","s":3,"prereq":"M35"},
 {"id":"M37","date":"1934-07-03","name":"THE MURDERS LEGALIZED","s":2},
 {"id":"M38","date":"1934-07-13","name":"I BECAME THE SUPREME JUDGE","s":1},
 {"id":"M39","date":"1934-08-02","name":"THE MERGED OFFICES","s":3,"prereq":"M36",
  "destroys":["THE CAMARILLA"]},
 {"id":"M40","date":"1934-08-19","name":"THE PLEBISCITE SEAL","s":2},
]

RESPONSE_DECK = [
 {"name":"THE FREE PRESS","kind":"static","copies":2,"passive_r":2,"a":2},
 {"name":"THE UNIONS (ADGB)","kind":"static","copies":2,"passive_r":2,"a":3},
 {"name":"REICHSBANNER / IRON FRONT","kind":"static","copies":2,"passive_r":2,"a":3},
 {"name":"THE COURTS","kind":"static","copies":1,"passive_r":1,"a":2},
 {"name":"THE PULPITS","kind":"static","copies":2,"passive_r":1,"a":2},
 {"name":"THE EXILE NETWORK","kind":"static","copies":2,"passive_r":1,"a":2,
  "reclaims":True},
 {"name":"THE FOREIGN CORRESPONDENTS","kind":"static","copies":2,"passive_r":1,"a":1},
 {"name":"THE NEIGHBORHOOD","kind":"static","copies":4,"passive_r":1,"a":1},
 {"name":"THE LEAFLET RUN","kind":"action","copies":4,"r":1,"a":1},
 {"name":"STREET DEFENSE","kind":"action","copies":3,"r":2,"a":3,"self_strain":1},
 {"name":"THE STRIKE FUND","kind":"action","copies":2,"r":1,"a":2},
 {"name":"DOCUMENT & SMUGGLE","kind":"action","copies":4,"r":1,"a":1},
 {"name":"THE WHISPER NETWORK","kind":"action","copies":2,"r":1,"a":1},
 {"name":"THE GENERAL STRIKE","kind":"action","copies":2,"r":4,"a":7,
  "a_extra_while":{"SIX MILLION UNEMPLOYED":3}},
 {"name":"THE COALITION VOTE","kind":"action","copies":2,"r":3,"a":4,
  "needs_m":3,"blocked_by":"THE ONE-PARTY STATE","persists_marker":True},
 {"name":"JUDICIAL CHALLENGE","kind":"action","copies":2,"r":2,"a":2,
  "blocked_by":"THE SECRET STATE POLICE"},
 {"name":"WELS' SPEECH","kind":"action","copies":2,"r":1,"a":1,"m_bonus":2},
]

DECK_TIERS = ((40, 59), (60, 79), (80, 99))

# ratios: loc_comments=93:31 imports_exports=2:0 calls_definitions=0:0
