m=open('make_compact.py').read()
# --- wolne, przyjemne migotanie okien ---
k=m.index("body[data-season=\"zima\"] .lit{display:inline")
e=m.index("/* napisy widoczne od początku */") if False else m.index("@keyframes candle")
e=m.index("\n",e)+1
m=m[:k]+"""body[data-season="zima"] .lit{display:inline;fill:url(#litg);opacity:0;animation:litIn 2.4s ease 4.2s both,candle 7.3s ease-in-out 6.6s infinite}
body[data-season="zima"] .lit.w2{animation:litIn 2.4s ease 4.6s both,candle 8.9s ease-in-out 7s infinite}
body[data-season="zima"] .lit.w3{animation:litIn 2.4s ease 5s both,candle 10.7s ease-in-out 7.4s infinite}
body.ready[data-season="zima"] .lit{animation-delay:0s,2.4s}
@keyframes litIn{from{opacity:0}to{opacity:.92}}
@keyframes candle{0%{opacity:.92}16%{opacity:.8}31%{opacity:.97}45%{opacity:.84}58%{opacity:1}72%{opacity:.79}86%{opacity:.95}100%{opacity:.92}}
"""+m[e:]
# --- księżyc ---
m=m.replace(".moon{fill:#fbf3d5;stroke:var(--ink);stroke-width:.9;stroke-linejoin:round}",
 ".moon{fill:#fbf3d5;stroke:var(--ink);stroke-width:.9}\n.crater{fill:#e6dbb6;opacity:.75}")
# --- panel suwaka ---
m=m.replace("/* napisy widoczne od początku */","""/* suwak czasu (podgląd) */
.scrub{display:flex;align-items:center;gap:12px;max-width:880px;margin:0 auto;padding:0 16px 36px;font-size:14px}
.scrub button{font:inherit;padding:7px 14px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:4px;cursor:pointer;min-width:118px}
.scrub input{flex:1;accent-color:var(--ink)}
.scrub output{min-width:78px;text-align:right;font-variant-numeric:tabular-nums}
.scrub small{display:block;color:#666;font-size:12px;margin-top:2px}
/* napisy widoczne od początku */""",1)
m=m.replace("open('naglowek-kompakt.html','w').write(h)","""h=h.replace('<button id="again">Rysuj ponownie</button>\\n</div>','<button id="again">Rysuj ponownie</button>\\n</div>\\n<div class="scrub"><button id="play" aria-pressed="false">⏸ Pauza</button><label style="flex:1"><input type="range" id="tl" min="0" max="1000" value="0" step="1" style="width:100%" aria-label="Czas od otwarcia strony"><small>Czas od otwarcia strony: początek suwaka to rysowanie (pierwsze sekundy), koniec to godzina.</small></label><output id="tlv">0.0 s</output></div>',1)
h=h.replace('</script>\\n</body>',SCRUB+'\\n</script>\\n</body>',1)
open('naglowek-kompakt.html','w').write(h)""",1)
m=m.replace("extra='''","""SCRUB=r'''
// ===== suwak czasu: przewijanie wszystkich animacji =====
const tl=document.getElementById('tl'),tlv=document.getElementById('tlv'),playB=document.getElementById('play');
const MAXT=3600,v2t=v=>MAXT*Math.pow(v/1000,3),t2v=t=>Math.round(1000*Math.cbrt(Math.min(1,Math.max(0,t)/MAXT)));
const fmt=t=>t<60?t.toFixed(1)+' s':Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0')+' min';
const cssAnims=()=>document.getAnimations().filter(a=>typeof CSSAnimation!=='undefined'&&a instanceof CSSAnimation);
function seek(t,full){
 paused=true;pausedT=t;scrubbed=true;
 cssAnims().forEach(a=>{if(a.__st===undefined)a.__st=a.startTime!=null?a.startTime:(document.timeline.currentTime-(a.currentTime||0));
  a.pause();a.currentTime=Math.max(0,t*1000-a.__st)});
 if(document.body.dataset.season==='jesien'&&G&&heights){
  if(t<simT-1e-3){if(!full){upd(t);return}resetLeaves()}
  if(full||t-simT<120){while(simT<t-1e-6)stepLeaves(Math.min(.05,t-simT),true);
   falling.forEach(f=>f.node.setAttribute('transform',`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`))}}
 upd(t)}
function upd(t){tlv.value=fmt(t);playB.textContent='▶ Odtwórz';playB.setAttribute('aria-pressed','true')}
function resume(){clockOff=pausedT-performance.now()/1000;paused=false;cssAnims().forEach(a=>a.play());
 playB.textContent='⏸ Pauza';playB.setAttribute('aria-pressed','false')}
let dragging=false;
tl.addEventListener('input',()=>{dragging=true;seek(v2t(+tl.value),false)});
tl.addEventListener('change',()=>{dragging=false;seek(v2t(+tl.value),true)});
playB.onclick=()=>paused?resume():seek(now(),true);
(function follow(){if(!paused&&!dragging){tl.value=t2v(now());tlv.value=fmt(now())}requestAnimationFrame(follow)})();
'''
extra='''""",1)
open('make_compact.py','w').write(m)
print('ok')
