# ratios: loc_comments=298:61 imports_exports=15:6 calls_definitions=133:17
"""serve — the table. Top-down playable board for POLITICS, stdlib only.

Layout per Erin's spec: the population at center (the inertial vector
field drawn live — every person a dot, leaning as they lean), the card
field ringed around it, machine and player avatars around that, your
hand along the bottom. Fifty-Three Days art is loaded from the base-game
set namespace.

No tips, no tricks: the interface enforces legality by refusal and
states what you MAY do, never what you should. The tutorial is the game
(hands-on from beat one, ruling 6): you sit down, history starts, and
nobody helps you.

Usage Guidance
--------------
    cd <repo-root> && python3 render/serve.py        # port 5300
    # phone browser -> http://localhost:5300
Solo seat + two noisy co-seats by default (POLITICS_SEATS=3 to change).
Match: Fifty-Three Days, hand of 5, full mechanics. Refresh-safe: state
lives server-side; the page polls. Human reflex windows and the dealt
arcanum are playable from the browser. Ctrl-C ends the republic early.

# === MODULE_BUILD ===
# id: render_serve_v01
#   purpose: playable top-down table over the real engine; art live
#   surfaces: HTTP / (board), /state, /act, /react; HumanSeat
#   boundaries: no game logic (engine/rules own truth); no advice;
#     blocking human input via queues, match on a worker thread
#   tests: test_serve.py (state and request contracts; no browser needed)
#   rollout: first sit-down vehicle; tutorial == this, per ruling 6
#   rollback: delete render/; engine untouched
#   hmmm: multiplayer seats wait on matchmaking phase; richer targeting
#     waits on a real multiplayer table rather than being guessed here
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: serve_state_reports_truth
#   behavior: /state returns tracks, board, hand, identity, reaction,
#     awaiting flag, and log tail straight from live state
# id: serve_act_enforces_hand_law
#   behavior: invalid card/burn indexes are refused; valid burns are
#     passed as actual card objects for runner hand-law enforcement
# id: serve_reaction_window
#   behavior: when a legal human reflex exists, the worker pauses until
#     the player chooses a legal reflex+burn pair or explicitly passes
# id: serve_arcana_playable
#   behavior: the human seat sees and may play only its dealt arcanum
# id: serve_match_thread_completes
#   behavior: with null human input/reactions the worker ends the match
#     on the null clock
# === END CONTRACTS ===
"""

import json
import os
import queue
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "engine"))

import politics_runner as pr                    # noqa: E402
import weimar_data as wd                        # noqa: E402
from harness_v1 import NoisyCoopPlayer          # noqa: E402
from arcana_agendas_v1 import (ArcanaModule, deal_agendas, deal_arcana)  # noqa: E402
from cards_v1 import WeimarMachine, build_response_pile    # noqa: E402
from inertial_engine import InertialEngine, weimar_seed    # noqa: E402
from rules_v1 import RulesV1                    # noqa: E402


class HumanSeat:
    """Blocks the match thread only when the human actually has a choice."""

    def __init__(self, rules):
        self.rules = rules
        self.inbox = queue.Queue()
        self.reaction_inbox = queue.Queue()
        self.awaiting = False
        self.reaction = None

    def take_turn(self, state, pid):
        self.awaiting = True
        plays = self.inbox.get()                 # blocks worker, not server
        self.awaiting = False
        return plays

    def react(self, state, pid, mcard):
        hand = state.hands[pid] if state.hands else []
        candidates = [i for i, card in enumerate(hand)
                      if card.get("reflex")
                      and self.rules.reflex_legal(state, card, mcard)]
        candidates = [i for i in candidates
                      if any(j != i for j in range(len(hand)))]
        if not candidates:
            return None
        self.reaction = {"incoming": dict(mcard), "candidates": candidates}
        choice = self.reaction_inbox.get()
        reaction = self.reaction
        self.reaction = None
        if choice is None:
            return None
        card_i, burn_i = choice
        if (card_i not in reaction["candidates"] or
                burn_i == card_i or
                not (0 <= burn_i < len(hand))):
            return None
        return hand[card_i], hand[burn_i]


class Table:
    def __init__(self, seats=3, seed=53):
        self.rules = RulesV1()
        self.human = HumanSeat(self.rules)
        st = pr.GameState(**wd.WEIMAR_OPENING)
        st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
        st.draw_pile = build_response_pile(seed)
        import random
        rng = random.Random(seed)
        deal_agendas(st, seats, rng)
        deal_arcana(st, seats, rng)
        self.state = st
        self.engine = InertialEngine(weimar_seed(100, seed))
        import random as _rnd
        bot = os.environ.get("POLITICS_BOTS", "noisy")
        if bot == "null":                        # hell mode: the empty chairs
            allies = [pr.NullPlayer() for _ in range(seats - 1)]
        else:                                    # imperfect allies; a0 seats
            allies = [NoisyCoopPlayer(_rnd.Random(seed * 7 + i))
                      for i in range(seats - 1)]  # replace later
        players = [self.human] + allies
        self.runner = pr.MatchRunner(
            self.engine, WeimarMachine(wd.MACHINE_SCRIPT,
                                       reserve=wd.RESERVE_PILE),
            players, st, rules=self.rules, hand_size=5,
            arcana=ArcanaModule())
        self.result = None
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        self.result = self.runner.run()

    def snapshot(self):
        st = self.state
        hand = st.hands[0] if st.hands else []
        arcana = (st.tallies.get("arcana") or [{}])[0]
        return {
            "tracks": {"population": st.population, "e": round(st.e, 2),
                       "m": st.m, "beat": st.machine_beats},
            "field": [{"x": round(p.x, 3), "c": p.converted}
                      for p in self.engine.persons],
            "board": [{"name": s.get("name"), "side": s.get("side"),
                       "ps": s.get("passive_s", 0),
                       "pr": s.get("passive_r", 0)}
                      for s in st.in_play_statics],
            "hand": hand,
            "reveal": next((
                {"name": ev[1], "s": ev[2],
                 "id": next((e2[1] for e2 in reversed(st.log)
                             if e2[0] == "machine_id"), None)}
                for ev in reversed(st.log) if ev[0] == "machine"), None),
            "agenda": (st.tallies.get("agendas") or [{}])[0],
            "arcana": arcana,
            "arcana_used": 0 in self.runner.arcana.used,
            "awaiting": self.human.awaiting,
            "reaction": self.human.reaction,
            "log": [list(map(str, ev)) for ev in st.log[-10:]],
            "done": None if self.result is None else {
                "outcome": self.result.outcome,
                "agendas": self.result.agenda_outcomes},
        }


def turn_from_request(table, req):
    """Translate browser indexes into owned card objects; reject bad identity."""
    hand = table.state.hands[0] if table.state.hands else []
    kind = req.get("kind")
    idx = req.get("card")
    if kind in {"static", "action"}:
        if not isinstance(idx, int) or not 0 <= idx < len(hand):
            return None
        card = hand[idx]
    else:
        card = None
    burn_indexes = req.get("burns", [])
    if not isinstance(burn_indexes, list):
        return None
    if len(set(burn_indexes)) != len(burn_indexes):
        return None
    if any(not isinstance(i, int) or not 0 <= i < len(hand)
           for i in burn_indexes):
        return None
    if idx in burn_indexes:
        return None
    burns = [hand[i] for i in burn_indexes]
    plays = pr.TurnPlays(discard_cards=burns)
    if kind == "static":
        card["side"] = "player"
        plays.static = card
    elif kind == "action":
        card["declared_target"] = "shared"
        plays.actions = [card]
    elif kind == "arcana":
        dealt = table.state.tallies.get("arcana") or []
        if not dealt:
            return None
        plays.arcana = dealt[0]
    elif kind != "pass":
        return None
    return plays


def reaction_from_request(table, req):
    """Return a validated (reflex-index, burn-index) pair or explicit pass."""
    pending = table.human.reaction
    if pending is None:
        return False, None
    if req.get("pass"):
        return True, None
    card_i, burn_i = req.get("card"), req.get("burn")
    hand = table.state.hands[0] if table.state.hands else []
    valid = (isinstance(card_i, int) and isinstance(burn_i, int)
             and card_i in pending["candidates"] and burn_i != card_i
             and 0 <= burn_i < len(hand))
    return (True, (card_i, burn_i)) if valid else (False, None)


TABLE = None
PAGE = """<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<style>body{background:#111;color:#eee;font-family:monospace;margin:0;padding:8px}
#tracks{display:flex;gap:12px;font-size:15px;padding:6px 2px;flex-wrap:wrap}
#arena{position:relative;height:46vh;background:#161616;border:1px solid #333;border-radius:6px;overflow:hidden}
canvas{width:100%;height:100%}
#reveal{position:absolute;top:6px;right:6px;width:104px;text-align:center;font-size:10px;color:#e88;background:#1c1414;border:1px solid #a33;border-radius:4px;padding:3px}
#reveal img{width:96px;display:block;margin:0 auto}
#board{font-size:11px;padding:4px;display:flex;flex-wrap:wrap;gap:4px}
.st{border:1px solid #555;padding:2px 5px;border-radius:3px}
.mach{border-color:#a33;color:#e88}.ply{border-color:#36a;color:#8be}
#hand{display:flex;gap:6px;overflow-x:auto;padding:6px 0}
.card{min-width:100px;border:1px solid #666;border-radius:4px;text-align:center;font-size:10px;background:#181818}
.card img{width:100px;display:block;border-radius:3px 3px 0 0}
.card.sel{outline:2px solid #fc3}.card.burn{outline:2px dashed #c66}
.card.rx{border-color:#fc3}
#ctl button,#reaction button{font-size:14px;margin:4px 4px 0 0;padding:7px 10px;background:#222;color:#eee;border:1px solid #666;border-radius:4px}
#identity{font-size:11px;color:#fc9;padding:2px}
#reaction{font-size:12px;color:#fc3;padding:4px 0}
#log{font-size:10px;color:#888;white-space:pre-wrap;padding-top:6px}
#done{font-size:14px;color:#fc3;padding:8px;white-space:pre-wrap}</style>
<div id=tracks></div>
<div id=arena><canvas id=cv></canvas><div id=reveal hidden></div></div>
<div id=identity></div><div id=reaction></div><div id=board></div><div id=hand></div>
<div id=ctl><button onclick="submit('static')">LAY STATIC</button>
<button onclick="submit('action')">PLAY ACTION</button>
<button onclick="mark()">MARK DISCARD</button>
<button onclick="submit('arcana')">PLAY ARCANUM</button>
<button onclick="submit('pass')">DRAW / END TURN</button>
<button onclick="reactNow(false)">REFLEX</button>
<button onclick="reactNow(true)">PASS REACTION</button></div>
<div id=done></div><div id=log></div>
<script>
let sel=null,burns=[],latest=null;
async function tick(){try{latest=await (await fetch('/state')).json();render(latest)}catch(e){}setTimeout(tick,900)}
function render(s){
 const reacting=!!s.reaction;
 tracks.innerHTML=`POP ${s.tracks.population} | E ${s.tracks.e} | M ${s.tracks.m} | BEAT ${s.tracks.beat}/40`+
 (reacting?' | <b style="color:#fc3">REACTION WINDOW</b>':(s.awaiting?' | <b style="color:#fc3">YOUR TURN</b>':' | <span style="color:#a33">HISTORY MOVES</span>'));
 const c=cv.getContext('2d');cv.width=cv.clientWidth;cv.height=cv.clientHeight;
 c.fillStyle='#161616';c.fillRect(0,0,cv.width,cv.height);
 const cx=cv.width/2,cy=cv.height/2,R=Math.min(cx,cy);
 s.field.forEach((p,i)=>{const a=(i*2.399963),r=R*0.44*Math.sqrt((i+0.5)/s.field.length);
  const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;
  c.fillStyle=p.c?'#a33':(p.x>0.5?'#c96':(p.x<-0.3?'#69c':'#999'));
  c.beginPath();c.arc(x,y,2.6,0,7);c.fill();});
 const bs=s.board;bs.forEach((b,i)=>{const a=-1.5708+i/Math.max(1,bs.length)*6.2832;
  const x=cx+Math.cos(a)*R*0.68,y=cy+Math.sin(a)*R*0.68;
  c.fillStyle=b.side=='machine'?'#a33':'#36a';c.beginPath();c.arc(x,y,5,0,7);c.fill();});
 c.fillStyle='#a33';c.fillRect(cx-14,8,28,10);
 c.fillStyle='#888';c.font='9px monospace';c.fillText('THE MACHINE',cx-32,30);
 ['YOU','ALLY','ALLY'].forEach((n,i)=>{c.fillStyle=i?'#557':'#36a';
  const x=cx+(i-1)*70;c.fillRect(x-12,cv.height-18,24,10);
  c.fillStyle='#888';c.fillText(n,x-10,cv.height-22);});
 board.innerHTML=bs.map(b=>`<span class="st ${b.side=='machine'?'mach':'ply'}">${b.name}${b.ps?' S'+b.ps:''}${b.pr?' R'+b.pr:''}</span>`).join('');
 identity.textContent='agenda: '+(s.agenda.name||'?')+' | arcanum: '+(s.arcana.name||'?')+(s.arcana_used?' [USED]':'');
 reaction.innerHTML=reacting?`Incoming ${s.reaction.incoming.id}: select a highlighted reflex, mark one other card, then REFLEX — or PASS REACTION.`:'';
 if(s.reveal&&s.reveal.id){reveal.hidden=false;reveal.innerHTML=`<img src="/art/${s.reveal.id.toLowerCase()}.png" onerror="this.hidden=true">${s.reveal.name}<br>S${s.reveal.s}`}else{reveal.hidden=true}
 const rxs=reacting?s.reaction.candidates:[];
 hand.innerHTML=s.hand.map((h,i)=>`<div class="card ${sel==i?'sel':''} ${burns.includes(i)?'burn':''} ${rxs.includes(i)?'rx':''}" data-i="${i}">
  <img src="/art/${(h.art_id||h.id||'x').toLowerCase()}.png" onerror="this.style.display='none'">
  ${h.name}<br>${h.kind||''} A${h.a||0}${h.r?' R'+h.r:''}${h.passive_r?' pR'+h.passive_r:''}</div>`).join('');
 hand.querySelectorAll('.card').forEach(el=>el.addEventListener('click',()=>{sel=Number(el.dataset.i);render(s)}));
 if(s.done){done.textContent=verdict(s.done)}
 log.textContent=s.log.map(l=>l.join(' ')).join('\n');}
function verdict(d){
 let out=(d.outcome=='win'?'THE REPUBLIC STANDS.':'THE REPUBLIC FALLS.')+'\n';
 (d.agendas||[]).forEach(a=>{const who=a.pid==0?'You':'Seat '+a.pid;
  out+=`${who} (${a.agenda}): agenda ${a.held?'HELD':'failed'}${a.held&&d.outcome=='loss'?' — won in the ashes':''}\n`});
 return out}
function mark(){if(sel!=null&&!burns.includes(sel)){burns.push(sel);sel=null;if(latest)render(latest)}}
async function submit(kind){
 if(!latest||latest.reaction)return;
 const r=await fetch('/act',{method:'POST',headers:{'content-type':'application/json'},
  body:JSON.stringify({kind:kind,card:sel,burns:burns})});
 if(r.ok){sel=null;burns=[]}}
async function reactNow(passRx){
 if(!latest||!latest.reaction)return;
 const burn=burns.length?burns[0]:null;
 const r=await fetch('/react',{method:'POST',headers:{'content-type':'application/json'},
  body:JSON.stringify(passRx?{pass:true}:{card:sel,burn:burn})});
 if(r.ok){sel=null;burns=[]}}
tick();
</script>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):                   # silence access log
        pass

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("content-type", "text/html")
            self.end_headers()
            self.wfile.write(PAGE.encode())
        elif self.path == "/state":
            self._json(TABLE.snapshot())
        elif self.path.startswith("/art/"):
            self._art(self.path[5:])
        else:
            self.send_response(404); self.end_headers()

    def _art(self, ident):
        ident = ident.replace(".png", "").lower()
        if not ident.replace("-", "").isalnum():
            self.send_response(404); self.end_headers(); return
        base = os.path.join(os.path.dirname(__file__), "..", "base-game",
                            "sets", "fifty-three-days", "cards")
        for deck in ("response", "machine", "setup", "reserve", "arcana",
                     "agendas"):
            png = os.path.join(base, deck, ident + ".png")
            if os.path.exists(png):
                self.send_response(200)
                self.send_header("content-type", "image/png")
                self.end_headers()
                with open(png, "rb") as fh:
                    self.wfile.write(fh.read())
                return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        n = int(self.headers.get("content-length", 0))
        req = json.loads(self.rfile.read(n) or "{}")
        if self.path == "/act":
            if not TABLE.human.awaiting or TABLE.human.reaction is not None:
                self._json({"ok": False}, 409)
                return
            plays = turn_from_request(TABLE, req)
            if plays is None:
                self._json({"ok": False}, 400)
                return
            TABLE.human.inbox.put(plays)
            self._json({"ok": True})
            return
        if self.path == "/react":
            ok, choice = reaction_from_request(TABLE, req)
            if not ok:
                self._json({"ok": False}, 400 if TABLE.human.reaction else 409)
                return
            TABLE.human.reaction_inbox.put(choice)
            self._json({"ok": True})
            return
        self.send_response(404); self.end_headers()


def main():
    global TABLE
    TABLE = Table(seats=int(os.environ.get("POLITICS_SEATS", "3")))
    port = int(os.environ.get("POLITICS_PORT", "5300"))
    print(f"POLITICS — Fifty-Three Days at http://localhost:{port}")
    print("hmmm: nobody in 1933 got a tooltip either.")
    ThreadingHTTPServer(("", port), H).serve_forever()


if __name__ == "__main__":
    main()
# ratios: loc_comments=298:61 imports_exports=15:6 calls_definitions=133:17
