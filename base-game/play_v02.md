# POLITICS — Base Play v0.2 (tensioned)
Layers: L1 SUBSTRATE (official record; not playable; compiles local decks) /
L2 ENGINE (automated; null clock guarantees total conversion absent play) /
L3 TABLE (humans; sole source of R).
Tracks: Population 100, E 0, M 2. Hands 7/5/3 = easy/std/hard. Play 1 draw 1.
Activation: response playable iff E >= A - M; discard 1 card = -1 barrier.
Machine cards always fire; their secret effects need E >= A_SE.
Machine phase: flip P cards (P = players). E += sum(S) - sum(R this round);
floor 0; cool -1 (-2 if M>=4). Population -= E.
Coalition: shared target this round M+1, none shared M-1. M<=1: SEs double.
Null clock: min T with (2.4P-1)T(T+1)/2 >= 100 -> P2:7 P3:6 P4:5 P5:4 P6:4.
Win: Machine deck empty and population > 50. Loss: population <= 50.
## Usage Guidance
Calibration test before first real session: deal no hands, flip only, confirm
the null clock hits within 1 turn of table. Log final E/pop/M every session;
three logs before any stat moves. All numbers [conjectural].
hmmm - the null clock is the only promise the Machine keeps.
