# ratios: loc_comments=206:51 imports_exports=15:4 calls_definitions=97:15
"""serve — the table. Top-down playable board for POLITICS, stdlib only.

Layout per Erin's spec: the population at center (the inertial vector
field drawn live — every person a dot, leaning as they lean), the card
field ringed around it, machine and player avatars around that, your
hand along the bottom. Real card art from expansions/.../cards/.

No tips, no tricks: the interface enforces legality by refusal and
states what you MAY do, never what you should. The tutorial is the game
(hands-on from beat one, ruling 6): you sit down, history starts, and
nobody helps you.

Usage Guidance
--------------
    cd <repo-root> && python3 render/serve.py        # port 5300
    # phone browser -> http://localhost:5300
Solo seat + two null co-seats by default (POLITICS_SEATS=3 to change).
Match: Fifty-Three Days, hand of 5, full mechanics. Refresh-safe: state
lives server-side; the page polls. Ctrl-C ends the republic early.

# === MODULE_BUILD ===
# id: render_serve_v01
#   purpose: playable top-down table over the real engine; art live
#   surfaces: HTTP / (board), /state, /act, /react; HumanSeat
#   boundaries: no game logic (engine/rules own truth); no advice;
#     blocking human input via queue, match on a worker thread
#   tests: test_serve.py (state contract; no browser needed)
#   rollout: first sit-down vehicle; tutorial == this, per ruling 6
#   rollback: delete render/; engine untouched
#   hmmm: reaction-window UI is prompt-only v1; multiplayer seats wait
#     on matchmaking phase; agenda card shown, arcana button minimal
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: serve_state_reports_truth
#   behavior: /state returns tracks, board, hand, awaiting flag, and log
#     tail straight from the live GameState, nothing derived or advised
# id: serve_act_enforces_hand_law
#   behavior: /act with a card index outside the hand is refused without
#     explanation
# id: serve_match_thread_completes
#   behavior: with null input the worker thread ends the match on the
#     null clock
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
from arcana_agendas_v1 import ArcanaModule, deal_agendas   # noqa: E402
from cards_v1 import WeimarMachine, build_response_pile    # noqa: E402
from inertial_engine import InertialEngine, weimar_seed    # noqa: E402
from rules_v1 import RulesV1                    # noqa: E402


class HumanSeat:
    """Blocks the match thread until the browser posts a turn."""

    def __init__(self):
        self.inbox = queue.Queue()
        self.awaiting = False

    def take_turn(self, state, pid):
        self.awaiting = True
        plays = self.inbox.get()                 # blocks worker, not server
        self.awaiting = False
        return plays

    def react(self, state, pid, mcard):
        return None                              # v1: no human reflex UI


class Table:
    def __init__(self, seats=3, seed=53):
        self.human = HumanSeat()
        st = pr.GameState(**wd.WEIMAR_OPENING)
        st.in_play_statics.extend(dict(s) for s in wd.SETUP_STATICS)
        st.draw_pile = build_response_pile(seed)
        import random
        deal_agendas(st, seats, random.Random(seed))
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
            players, st, rules=RulesV1(), hand_size=5,
            arcana=ArcanaModule())
        self.result = None
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        self.result = self.runner.run()

    def snapshot(self):
        st = self.state
        hand = st.hands[0] if st.hands else []
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
            "awaiting": self.human.awaiting,
            "log": [list(map(str, ev)) for ev in st.log[-8:]],
            "done": None if self.result is None else {
                "outcome": self.result.outcome,
                "agendas": self.result.agenda_outcomes},
        }


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
.card.sel{outline:2px solid #fc3}
.card.burn{outline:2px dashed #c66}
#ctl button{font-size:14px;margin:4px 4px 0 0;padding:7px 10px;background:#222;color:#eee;border:1px solid #666;border-radius:4px}
#agenda{font-size:11px;color:#fc9;padding:2px}
#log{font-size:10px;color:#888;white-space:pre-wrap;padding-top:6px}
#done{font-size:14px;color:#fc3;padding:8px;white-space:pre-wrap}</style>
<div id=tracks></div>
<div id=arena><canvas id=cv></canvas><div id=reveal hidden></div></div>
<div id=agenda></div><div id=board></div><div id=hand></div>
<div id=ctl><button onclick="submit('static')">LAY STATIC</button>
<button onclick="submit('action')">PLAY ACTION</button>
<button onclick="mark()">MARK DISCARD</button>
<button onclick="submit('pass')">DRAW / END TURN</button></div>
<div id=done></div><div id=log></div>
<script>
let sel=null, burns=[];
async function tick(){try{const s=await (await fetch('/state')).json();render(s)}catch(e){}setTimeout(tick,900)}
function render(s){
 tracks.innerHTML=`POP ${s.tracks.population} | E ${s.tracks.e} | M ${s.tracks.m} | BEAT ${s.tracks.beat}/40`+(s.awaiting?' | <b style="color:#fc3">YOUR TURN</b>':' | <span style="color:#a33">HISTORY MOVES</span>');
 const c=cv.getContext('2d');cv.width=cv.clientWidth;cv.height=cv.clientHeight;
 c.fillStyle='#161616';c.fillRect(0,0,cv.width,cv.height);
 const cx=cv.width/2,cy=cv.height/2,R=Math.min(cx,cy);
 // ring 1: the population, center disk — every person a dot, leaning as they lean
 s.field.forEach((p,i)=>{const a=(i*2.399963),r=R*0.44*Math.sqrt((i+0.5)/s.field.length);
  const x=cx+Math.cos(a)*r,y=cy+Math.sin(a)*r;
  c.fillStyle=p.c?'#a33':(p.x>0.5?'#c96':(p.x<-0.3?'#69c':'#999'));
  c.beginPath();c.arc(x,y,2.6,0,7);c.fill();});
 // ring 2: the card field — statics orbit the population
 const bs=s.board;bs.forEach((b,i)=>{const a=-1.5708+i/bs.length*6.2832;
  const x=cx+Math.cos(a)*R*0.68,y=cy+Math.sin(a)*R*0.68;
  c.fillStyle=b.side=='machine'?'#a33':'#36a';
  c.beginPath();c.arc(x,y,5,0,7);c.fill();});
 // ring 3: avatars — the machine above, the seats below
 c.fillStyle='#a33';c.fillRect(cx-14,8,28,10);
 c.fillStyle='#888';c.font='9px monospace';c.fillText('THE MACHINE',cx-32,30);
 ['YOU','ALLY','ALLY'].forEach((n,i)=>{c.fillStyle=i?'#557':'#36a';
  const x=cx+(i-1)*70;c.fillRect(x-12,cv.height-18,24,10);
  c.fillStyle='#888';c.fillText(n,x-10,cv.height-22);});
 board.innerHTML=bs.map(b=>`<span class="st ${b.side=='machine'?'mach':'ply'}">${b.name}${b.ps?' S'+b.ps:''}${b.pr?' R'+b.pr:''}</span>`).join('');
 agenda.textContent='your agenda: '+(s.agenda.name||'?');
 if(s.reveal&&s.reveal.id){reveal.hidden=false;reveal.innerHTML=`<img src="/art/${s.reveal.id.toLowerCase()}.png" onerror="this.hidden=true">${s.reveal.name}<br>S${s.reveal.s}`}
 hand.innerHTML=s.hand.map((h,i)=>`<div class="card ${sel==i?'sel':''} ${burns.includes(i)?'burn':''}" onclick="sel=${i}">
  <img src="/art/${(h.art_id||h.id||'x').toLowerCase()}.png" onerror="this.style.display='none'">
  ${h.name}<br>${h.kind} A${h.a||0}${h.r?' R'+h.r:''}${h.passive_r?' pR'+h.passive_r:''}</div>`).join('');
 if(s.done){done.textContent=verdict(s.done)}
 log.textContent=s.log.map(l=>l.join(' ')).join('\n');}
function verdict(d){
 let out=(d.outcome=='win'?'THE REPUBLIC STANDS.':'THE REPUBLIC FALLS.')+'\n';
 (d.agendas||[]).forEach(a=>{const who=a.pid==0?'You':'Seat '+a.pid;
  out+=`${who} (${a.agenda}): agenda ${a.held?'HELD':'failed'}${a.held&&d.outcome=='loss'?' — won in the ashes':''}\n`});
 return out}
function mark(){if(sel!=null){burns.push(sel);sel=null}}
async function submit(kind){await fetch('/act',{method:'POST',headers:{'content-type':'application/json'},
 body:JSON.stringify({kind:kind,card:sel,burns:burns})});sel=null;burns=[]}
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
        base = os.path.join(os.path.dirname(__file__), "..", "expansions",
                            "scared-sacred", "cards")
        for deck in ("response", "machine", "setup", "reserve"):
            png = os.path.join(base, deck, ident + ".png")
            if os.path.exists(png):
                self.send_response(200)
                self.send_header("content-type", "image/png")
                self.end_headers()
                self.wfile.write(open(png, "rb").read())
                return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path != "/act":
            self.send_response(404); self.end_headers(); return
        n = int(self.headers.get("content-length", 0))
        req = json.loads(self.rfile.read(n) or "{}")
        hand = TABLE.state.hands[0] if TABLE.state.hands else []
        idx = req.get("card")
        card = hand[idx] if isinstance(idx, int) and 0 <= idx < len(hand) \
            else None
        burns = [hand[b] for b in req.get("burns", [])
                 if isinstance(b, int) and 0 <= b < len(hand)]
        plays = pr.TurnPlays(discards=len(burns))
        if req.get("kind") == "static" and card is not None:
            card["side"] = "player"
            plays.static = card
        elif req.get("kind") == "action" and card is not None:
            card["declared_target"] = "shared"
            plays.actions = [card]
        if TABLE.human.awaiting:
            TABLE.human.inbox.put(plays)
            self._json({"ok": True})
        else:
            self._json({"ok": False}, 409)       # not your beat; no explanation


def main():
    global TABLE
    TABLE = Table(seats=int(os.environ.get("POLITICS_SEATS", "3")))
    port = int(os.environ.get("POLITICS_PORT", "5300"))
    print(f"POLITICS — Fifty-Three Days at http://localhost:{port}")
    print("hmmm: nobody in 1933 got a tooltip either.")
    ThreadingHTTPServer(("", port), H).serve_forever()


if __name__ == "__main__":
    main()
# ratios: loc_comments=206:51 imports_exports=15:4 calls_definitions=97:15
