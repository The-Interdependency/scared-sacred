# POLITICS — Base Play v0.3 (consolidated; supersedes v0.1/v0.2/deltas)
Claude generated. Context, prompt by Erin Patrick Spencer.

## Layers
L1 SUBSTRATE: the political process per official sources. Not directly
playable. Sole input to the card generator; a jurisdiction's record
compiles into that place's Machine deck.
L2 ENGINE: the tensioned system, fully automated. Left alone it ends in
total conversion on the null clock, always.
L3 TABLE: human play. The only source of R.

## Setup
Population 100. Tension E 0. Mutuality M 2. Hands: 7 easy / 5 standard /
3 hard. Each player draws one secret AGENDA and one face-down ARCANUM.

## Activation energy
Every response card carries A. Playable iff E >= A - M (crisis creates
will; mutuality catalyzes). A player may discard cards, 1 discard = -1
effective barrier. Machine cards always fire; their secret effects
resolve only if E >= A_SE (phase transitions, not decisions).

## Round
1. HUMAN PHASE — each player: play 1, draw 1, declare target.
2. COALITION CHECK — any shared target this round: M+1. None shared: M-1.
3. MACHINE PHASE — flip P cards (P = seated players). Sum S. Resolve
   secret effects meeting their A_SE (twice each if M <= 1).
4. ENGINE — E = max(0, E + S_total - R_total); then cooling -1 (-2 if
   M >= 4). M >= 4 also grants all R +1.
5. REGISTRATION — population -= E.

## Targeting (players not assumed aligned)
Every card declares legal targets: machine-card | track | player.
INTERFERENCE COST: any player-targeted play adds its A to E as strain and
M-1. Player-targeted plays are announced and attributed openly.
Examples: Journalism@player reveals agenda or hand. Prosecution@player
forces 1 discard. Steelman@player compels a stated position; if you share
a target next round, both gain +1 R.

## Agendas
All agendas require population > 50 to win [claude-default — strike to
admit winning-in-the-ashes; darker, more real; Erin's call]; they diverge
above the floor (win with M <= 2; most attributed R; a named Machine card
still in play; ...). Revealed only on win claim or by Journalism/Audit.

## Null clock (calibration)
Mean S per Machine card 2.4, cooling -1: zero human play converts the
population at the smallest T with (2.4P - 1) * T(T+1)/2 >= 100:
P2:7 P3:6 P4:5 P5:4 P6:4 turns. Apathy loses on a printable schedule.

## Win / Loss
Win: Machine deck empties with population > 50. Loss: population <= 50.

## Usage Guidance
Calibration first: deal no hands, flip only, confirm the null clock lands
within 1 turn of table. Then A/B agendas on and off at the same table.
Log final E / population / M every session; three logs before any stat
moves. All numbers [conjectural].

hmmm — the Machine never has to coordinate and the humans have to choose
to; step 2 is the whole game wearing a rules-paragraph costume.
