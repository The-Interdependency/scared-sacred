# POLITICS: WEIMAR — "Fifty-Three Days" — Card Set v0.1
Claude generated. Context, prompt by Erin Patrick Spencer.

---

## MODULE_BUILD manifest

- **Purpose:** Complete first card set. Machine deck = deterministic historical replay script (Jan 30 1933 → Aug 19 1934), 40 cards in fixed order plus 3 setup statics. Response deck = 40 cards (playsets of 17 uniques), everything actually available to the opposition.
- **Boundaries:** Machine plays exactly as history; no tips, no advisor text; interface enforces legality only. Victims never depicted — counts as Isotype only. Mechanisms, never essences or internal states. Every card cites primary documents. Named figures are deceased historical actors; card text quotes documented acts and words only.
- **Prerequisite rule [claude-default]:** each scripted card lists prerequisites; if human play has destroyed a card's prerequisite, it is SKIPPED — its S never enters the world. History's plan, not history's guarantee.
- **Status tags:** all S/R/A values [conjectural — pre-playtest]. All dates, actors, documents [test-backed — standard historical record; verify citations at art pass].
- **Tuning target (ratified):** null clock reproduces history exactly; skilled coordinated play beats it rarely; nothing between gets softened.

---

## 0. Setup state (in play before turn one)

| ID | Card | Type | Effect | Source |
|---|---|---|---|---|
| X1 | **ARTICLE 48** | Machine STATIC | Passive S1 every Machine PMR. Cannot be targeted while E ≥ 3 (emergencies protect emergency powers). | Weimar Constitution, Art. 48; use normalized under Brüning 1930–32 |
| X2 | **THE CAMARILLA** | Machine STATIC | Once per rotation the Machine's next card gains +1 S (the door to the President is held open). Destroyed automatically by M40. | Papen–Hindenburg circle, Jan 1933 |
| X3 | **SIX MILLION UNEMPLOYED** | Machine STATIC | E starts at 5. THE GENERAL STRIKE (R14) costs +3 A while this is in play. Isotype: 6,000 person-icons @ 1:1,000. | Reich labor statistics, winter 1932–33 |

Opening tracks: **Population 100 · E 5 · M 1** (the SPD–KPD split is the setup screen, not a card).

---

## 1. MACHINE DECK — the script (fixed order; date; prerequisites in brackets)

**Phase I — the legal seizure (turns 1–10)**

- **M01 · Jan 30 · THE BACKROOM KINGMAKER** — TACTIC-BEARER · S2. Documented act: Papen brokers the Chancellorship; "In two months we'll have pushed [him] so far into a corner that he'll squeak." SE (A_SE 2): the next scripted card plays immediately after this one.
- **M02 · Feb 1 · DISSOLUTION** — EVENT · S1. Reichstag dissolved; new elections called under emergency conditions. [prereq: X1]
- **M03 · Feb 4 · DECREE FOR THE PROTECTION OF THE GERMAN PEOPLE** — EVENT · S2. Press and assembly restrictions by decree. SE (A_SE 4): THE FREE PRESS (R01) generates no R next rotation. [prereq: X1]
- **M04 · Feb 17 · THE SHOOTING ORDER** — EVENT · S2. Göring instructs Prussian police that failure to use firearms against "enemies of the state" will be disciplined. [source: Göring directive, 17.2.1933]
- **M05 · Feb 22 · THE DEPUTIZED STREET** — EVENT · S2. 50,000 SA/SS/Stahlhelm enrolled as auxiliary police — street violence acquires a badge. Isotype: 50 figure-icons @ 1:1,000. [prereq: M04]
- **M06 · Feb 24 · THE LIEBKNECHT HOUSE RAID** — EVENT · S1. KPD headquarters raided; "evidence of insurrection" announced, never published. SE (A_SE 3): M07's SE arms at −1 A_SE.
- **M07 · Feb 27 · THE FIRE OPPORTUNIST** — EVENT · S3. The Reichstag burns; within hours, mass arrests begin from lists prepared earlier. SE = **M08 plays immediately** (A_SE 5 — the decree only unlocks at high E; if E < 5, M08 waits one beat).
- **M08 · Feb 28 · THE FIRE DECREE** — STATIC · S2 passive. Suspends habeas corpus, press, assembly, privacy of post — for twelve years. While in play: all Response STATICS −1 R. [prereq: M07 reached the field; Reichstagsbrandverordnung text]
- **M09 · Mar 3 · THE THÄLMANN ARREST** — EVENT · S1. KPD leadership seized; ~4,000 functionaries detained within days. Isotype: 4 figure-icons @ 1:1,000, half-toned (estimates).
- **M10 · Mar 5 · THE 43.9% ELECTION** — EVENT · S2. Under fire decree and SA "supervision," NSDAP polls 43.9% — never a free majority. SE (A_SE 3): Machine draws +1 card next rotation. Isotype: vote bars, exact returns printed. [Reichstag election returns, 5.3.1933]

**Phase II — Gleichschaltung (turns 11–24)**

- **M11 · Mar 8–9 · THE STATE SEIZURES** — EVENT · S2. Reich commissars replace state governments not yet in line. [prereq: M08]
- **M12 · Mar 13 · THE MINISTRY OF PUBLIC ENLIGHTENMENT** — TACTIC-BEARER (Goebbels) · S2, STATIC after play: every Machine EVENT thereafter +1 S (narrative control is a force multiplier). [prereq: M10]
- **M13 · Mar 20 · DACHAU ANNOUNCED** — EVENT · S2. Himmler announces a camp for 5,000 at a press conference — publicity, not secrecy, was the instrument. Isotype: 5 tent-icons @ 1:1,000. Counts only; no depiction. [Münchner Neueste Nachrichten, 21.3.1933]
- **M14 · Mar 21 · THE DAY OF POTSDAM** — EVENT · S1. Staged reconciliation with the old order at the Garrison Church; respectability laundering. SE (A_SE 2): M15 gains +1 S.
- **M15 · Mar 23 · THE LEGALIST COUP (ENABLING ACT)** — EVENT · S3. Vote condition: resolves at full S unless Response field shows M ≥ 3 **and** THE COALITION VOTE (R15) in play — the combination that never happened. Passed 444–94 with KPD deputies arrested and SA lining the chamber. On resolve: X1 retires (no longer needed); Machine no longer requires prerequisites of type "decree." [Ermächtigungsgesetz, RGBl. I 141]
- **M16 · Apr 1 · THE BOYCOTT** — EVENT · S2. Organized national boycott of Jewish businesses; SA posts at doorways. Documented mechanism: economic isolation as public ritual.
- **M17 · Apr 7 · THE CIVIL SERVICE LAW** — EVENT · S2. "Restoration of the Professional Civil Service": political and racial purges of the state apparatus by statute. SE (A_SE 4): THE COURTS (R04) flips — its R becomes S1 permanently (the bench is now staffed accordingly). [Gesetz zur Wiederherstellung des Berufsbeamtentums]
- **M18 · Apr 26 · THE SECRET STATE POLICE** — STATIC · S1 passive. Gestapo established in Prussia. While in play: Response ACTIONS reveal their sleeved SEs to the Machine (surveillance).
- **M19 · May 1 · THE STOLEN HOLIDAY** — EVENT · S1. May Day nationalized; unions march under the new flags, reassured. SE (A_SE 2): M20 plays immediately.
- **M20 · May 2 · THE UNION SEIZURE** — EVENT · S3. Twenty-four hours after marching, ADGB offices occupied, funds seized, leaders arrested. Destroys THE UNIONS (R02) wherever it stands. [prereq: R02 not already removed by exile play]
- **M21 · May 10 · THE BOOK FIRES** — EVENT · S1. University-square burnings, nationally choreographed. SE (A_SE 3): one Response STATIC of the players' choice is revealed and loses 1 R (self-censorship).
- **M22 · Jun 22 · THE SPD BAN** — EVENT · S2. SPD outlawed as "hostile to state and people." Destroys REICHSBANNER (R03). [prereq: M15]
- **M23 · Jun–Jul · THE SELF-DISSOLUTIONS** — EVENT · S2. Remaining parties dissolve themselves "voluntarily" — DNVP, DVP, Center in sequence. Mechanism: anticipatory obedience as institutional suicide.
- **M24 · Jul 14 · THE ONE-PARTY STATE** — STATIC · S1 passive. Law Against the Formation of New Parties. While in play: THE COALITION VOTE (R15) is unplayable. [Gesetz gegen die Neubildung von Parteien]

**Phase III — consolidation (turns 25–40)**

- **M25 · Jul 20 · THE CONCORDAT** — EVENT · S1. Treaty neutralizes political Catholicism; the Church trades politics for sacraments. SE (A_SE 2): THE PULPITS (R05) −1 R permanently.
- **M26 · Sep 22 · THE CULTURE CHAMBER** — EVENT · S1. All artists, writers, musicians require chamber membership to work. [prereq: M12]
- **M27 · Oct 14 · THE LEAGUE EXIT** — EVENT · S1. Germany leaves the League of Nations; external constraint discarded, plebiscite scheduled to bless it.
- **M28 · Nov 12 · THE 92% BALLOT** — EVENT · S2. One-party election plus plebiscite; approval theater at gunpoint-adjacent conditions. Isotype: ballot bars with the abstention/invalid count printed — the dissent that remained visible.
- **M29 · Nov 30 · GESTAPO LAW** — EVENT · S1. Political police placed beyond judicial review in Prussia. SE (A_SE 3): JUDICIAL CHALLENGE (R16) unplayable while M18 stands.
- **M30 · Dec 1 · PARTY AND STATE UNITY LAW** — EVENT · S1. NSDAP declared "bearer of the German state-idea," legally fused to the state.
- **M31 · Jan 26 1934 · THE POLISH SURPRISE** — EVENT · S1. Non-aggression pact; foreign-policy respectability purchased abroad while the interior closes. Mechanism: external calm as internal cover.
- **M32 · Jan 30 1934 · THE RECONSTRUCTION ACT** — EVENT · S2. State parliaments abolished; federalism ends by statute on the anniversary, for the symbolism. [prereq: M11]
- **M33 · Feb 24 1934 · THE PEOPLE'S COURT ANNOUNCED** — EVENT · S1. Treason cases moved to a new court outside the ordinary judiciary (statute follows in April). [prereq: M17]
- **M34 · Apr 20 1934 · HIMMLER TAKES THE GESTAPO** — EVENT · S1. Police powers consolidate into the SS line. [prereq: M18]
- **M35 · Jun 17 1934 · THE MARBURG SPEECH** — EVENT · S0 (the Machine's only zero). Papen's public warning — conservative buyer's remorse, spoken aloud once. SE (A_SE 5): if any Response ACTION is played this rotation, it gains +2 R (the regime's one public wobble was a real opening). The script's built-in tragedy: history left the window open one beat.
- **M36 · Jun 30 1934 · THE PURGE** — EVENT · S3. Night of the Long Knives: SA leadership, Schleicher, Marburg's author's staff — rivals and inconvenient allies killed extrajudicially. Isotype: figure-lying-down icons, count printed as range (85 documented – ~200 estimated), half-toned. [prereq: M35]
- **M37 · Jul 3 1934 · THE MURDERS LEGALIZED** — EVENT · S2. Cabinet law declares the killings "lawful acts of state defense" — retroactively. Mechanism: legality as post-hoc costume. [Gesetz über Maßnahmen der Staatsnotwehr]
- **M38 · Jul 13 1934 · "I BECAME THE SUPREME JUDGE"** — EVENT · S1. Reichstag speech claiming personal judicial supremacy, applauded. Verbatim quote on card face, sourced.
- **M39 · Aug 2 1934 · THE MERGED OFFICES** — EVENT · S3. Hindenburg dies; Chancellor and President fuse; the army swears to a person, not a constitution. Destroys X2 (the door-holders are no longer needed). [prereq: M36]
- **M40 · Aug 19 1934 · THE PLEBISCITE SEAL** — EVENT · S2. 89.9% ratifies the fusion. **Set ends.** If population > 50 at this card's resolution, the players have beaten history. Isotype: the 10.1% printed as bright icons — ten in every hundred, under all of it, still said no.

---

## 2. RESPONSE DECK — 40 cards (17 uniques; copies noted)

**STATICS** *(lay one per turn; passive R every Machine PMR while standing)*

- **R01 · THE FREE PRESS** ×2 — STATIC · R2 · A2. Vorwärts, Berliner Tageblatt, the provincial dailies. Vulnerable to M03/M08 by design.
- **R02 · THE UNIONS (ADGB)** ×2 — STATIC · R2 · A3. Millions organized; leadership praying accommodation will spare them. Destroyed by M20 unless exiled first.
- **R03 · REICHSBANNER / IRON FRONT** ×2 — STATIC · R2 · A3. Three arrows; hundreds of thousands of members; never given the order. Destroyed by M22.
- **R04 · THE COURTS** ×1 — STATIC · R1 · A2. Sleeved SE (self): on M17, flips to Machine S1 permanently. An honest card about a compromised institution.
- **R05 · THE PULPITS** ×2 — STATIC · R1 · A2. Sermons reach where papers can't; −1 R after M25.
- **R06 · THE EXILE NETWORK** ×2 — STATIC · R1 · A2. Special: once per rotation, convert 2 population loss into removal-from-play — saved, not held. Prague, Paris, Amsterdam.
- **R07 · THE FOREIGN CORRESPONDENTS** ×2 — STATIC · R1 · A1. Mowrer, Shirer's forerunners; reporting out what can't be printed in. Immune to M03; not to M18.
- **R08 · THE NEIGHBORHOOD** ×3 — STATIC · R1 · A1. The Kiez: workers' quarters where the SA still needed escorts. Cheapest static in the deck; the last to fall in reality.

**ACTIONS** *(one per turn; discard 1 card to play one additional)*

- **R09 · THE LEAFLET RUN** ×3 — ACTION · R1 · A1. Mimeograph and courage. After M08: playing it reveals your hand to the Machine (M18 logic anticipated).
- **R10 · STREET DEFENSE** ×3 — ACTION · R2 · A3. Meeting the SA in kind. Sleeved SE: +1 E (defensive violence still heats the commons — the Engine's oldest lesson).
- **R11 · THE STRIKE FUND** ×2 — ACTION · R1 · A2. Money moves before bodies do; −1 A to the next R14 attempt.
- **R12 · DOCUMENT & SMUGGLE** ×3 — ACTION · R1 · A1. The archive leaves the country; every Machine card in play gets its citation preserved. Endgame value: at M40, each R12 played this game counts +1 population (what was proven later saved lives and verdicts).
- **R13 · THE WHISPER NETWORK** ×2 — ACTION · R1 · A1. Warnings travel; next Machine SE reveals early to the table.
- **R14 · THE GENERAL STRIKE** ×2 — ACTION · R4 · **A7** (−3 with X3 gone; −1 per R11). The card that beat Kapp in 1920 at low A; priced at 1933's reality. If it ever resolves: E −4, M+2, and M20 is skipped.
- **R15 · THE COALITION VOTE** ×2 — ACTION · R3 · A4 · playable only at M ≥ 3; unplayable after M24. If in play when M15 resolves: the Enabling Act fails its two-thirds — the entire script from M16 onward re-prices (every S −1). The card history never played.
- **R16 · JUDICIAL CHALLENGE** ×2 — ACTION · R2 · A2. Injunctions, appeals, the last lawful levers; dead letter after M29 while the Gestapo static stands.
- **R17 · WELS' SPEECH** ×2 — ACTION · R1 · A1 · M+2. March 23, before the vote is lost, on the record: "Freedom and life can be taken from us, but not honor." Changes no math and all meaning; the deck's dignity card. Verbatim, sourced.

**Copy count: 2+2+2+1+2+2+2+3 +3+3+2+3+2+2+2+2+2 = 40.** ✓

---

## 3. Set rules deltas

- Machine module = replay script: fixed order, prerequisite-gated skips, zero policy AI.
- Tutorial and free play use identical decks; the only difference is that free play shuffles the Response draw pile. No tips, no tricks, no advisor text; the interface enforces legality only.
- M-track start 1 is set doctrine, not a knob.
- Win check at M40 resolution: population > 50 beats history. Expected win rate target: **possible, not probable** — if playtest approaches even odds, re-price upward.

## Usage Guidance
Build order unchanged: runner → engine → these schemas as the first data. Calibration run: no Response plays; confirm total conversion lands on/near M39–M40 pacing. Then A/B: does R15+M≥3 at turn 15 actually create the counterfactual corridor, and how often do real tables find it? Log every session. All stats [conjectural]; all history [test-backed — verify each citation at art pass].

hmmm — forty scripted cards and the only one with zero strain is the warning a co-conspirator finally spoke out loud, one beat before the knives; the Machine's weakest card is the whole tragedy's hinge.
