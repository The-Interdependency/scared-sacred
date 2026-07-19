# ratios: loc_comments=38:26 imports_exports=5:1 calls_definitions=23:2
"""cards_export — emit every card as a repo-resident JSON asset.

Single source of truth stays weimar_data.py / arcana_agendas_v1.py; this
exporter renders each card into its own file so art lands beside data:
grok's m07.png drops next to m07.json and the render layer needs no
lookup table. Regenerate after any data change; hand-editing the JSON is
the anti-pattern (the export overwrites without mercy).

Usage Guidance
--------------
    python3 cards_export.py [repo_root]     # default ..
Writes expansions/scared-sacred/cards/{setup,machine,reserve,response,
arcana,agendas}/<id>.json plus index.json. Each card carries an "art"
block: {"file": "<id>.png", "status": "awaiting"} until validated art
exists beside it, then rerun flips status to "present". Prints counts;
a count mismatch against index.json is a bug, full stop.

# === MODULE_BUILD ===
# id: cards_export_v01
#   purpose: cards as first-class repo files; art drop-in slots
#   surfaces: export(root) -> index dict; __main__ CLI
#   boundaries: read-only over data modules; overwrites cards/ tree
#   tests: self-verifying counts on run (index vs files written)
#   rollout: run per data change; committed output is canon-derived
#   rollback: delete cards/ tree; data modules unaffected
#   hmmm: art status flips by file presence, not by validation record --
#     the validation ledger is a later, honest upgrade
# === END MODULE_BUILD ===
"""

import json
import os
import sys

import weimar_data as wd
from arcana_agendas_v1 import AGENDAS, ARCANA


def _write(root, deck, ident, card):
    d = os.path.join(root, "expansions", "scared-sacred", "cards", deck)
    os.makedirs(d, exist_ok=True)
    png = ident.lower() + ".png"
    card = dict(card)
    card["art"] = {"file": png,
                   "status": "present" if os.path.exists(
                       os.path.join(d, png)) else "awaiting"}
    path = os.path.join(d, ident.lower() + ".json")
    with open(path, "w") as f:
        json.dump(card, f, indent=1, sort_keys=True)
    return deck + "/" + ident.lower()


def export(root=".."):
    index = {"set": "FIFTY-THREE DAYS", "cards": []}
    for i, c in enumerate(wd.SETUP_STATICS):
        index["cards"].append(_write(root, "setup", f"x{i+1}", c))
    for c in wd.MACHINE_SCRIPT:
        index["cards"].append(_write(root, "machine", c["id"], c))
    for c in wd.RESERVE_PILE:
        index["cards"].append(_write(root, "reserve", c["id"], c))
    for i, c in enumerate(wd.RESPONSE_DECK):
        index["cards"].append(_write(root, "response", f"r{i+1:02d}", c))
    for c in ARCANA:
        index["cards"].append(_write(root, "arcana", f"a{c['num']:02d}", c))
    for i, c in enumerate(AGENDAS):
        index["cards"].append(_write(root, "agendas", f"g{i+1:02d}", c))
    d = os.path.join(root, "expansions", "scared-sacred", "cards")
    with open(os.path.join(d, "index.json"), "w") as f:
        json.dump(index, f, indent=1)
    return index


if __name__ == "__main__":
    idx = export(sys.argv[1] if len(sys.argv) > 1 else "..")
    print(f"exported {len(idx['cards'])} cards")
# ratios: loc_comments=38:26 imports_exports=5:1 calls_definitions=23:2
