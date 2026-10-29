import re
h=open('naglowek.html').read()
js=open('header2_js.txt').read()
h=re.sub(r'<script>.*</script>',lambda m:js,h,flags=re.S)
R=[("#hero{position:relative;height:clamp(520px,78vh,800px);overflow:hidden}","#hero{position:relative;height:clamp(240px,34vh,380px);overflow:hidden}"),
("@media (max-width:900px){#hero{height:calc(min(100vw,560px)*1.02 + 90px)}}","@media (max-width:900px){#hero{height:calc(min(100vw,560px)*.47 + 80px)}}"),
("<title>Parafia Ewangelicko-Augsburska Brenna-Górki</title>","<title>Brenna-Górki – nagłówek kompaktowy</title>"),
("Prototyp nagłówka. Poniżej","Wersja kompaktowa (1/3 ekranu). Poniżej")]
for a,b in R:
    assert a in h,a; h=h.replace(a,b)
CSSW='''
/* ===== zimowy wieczór ===== */
body[data-season="zima"]{--ridge:#e6e9ee;--ridge2:#d3dae4}
body[data-season="zima"] #sky{background:linear-gradient(to bottom,#24395a 0%,#4f6a8f 28%,#b9b7c4 52%,#f0d2b4 66%,transparent 80%)}
body[data-season="zima"] .cloud path{fill:color-mix(in srgb,#c9d3e2 70%,transparent);stroke-opacity:.2}
.stars circle{fill:#fff6dc;animation:twinkle ease-in-out infinite alternate}
@keyframes twinkle{from{opacity:.25}to{opacity:1}}
body[data-season="zima"] .hide-zima{display:none}
/* ciepłe światło w oknach kościoła w Brennej – zapala się po narysowaniu kościoła, migocze jak świeca */
.lit{display:none}
body[data-season="zima"] .lit{display:inline;fill:url(#litg);opacity:0;animation:litIn 2.4s ease 4.2s both,candle 4.6s ease-in-out 6.6s infinite}
body[data-season="zima"] .lit.w2{animation:litIn 2.4s ease 4.6s both,candle 5.3s ease-in-out 7s infinite}
body[data-season="zima"] .lit.w3{animation:litIn 2.4s ease 5s both,candle 6.1s ease-in-out 7.4s infinite}
body.ready[data-season="zima"] .lit{animation-delay:0s,2.4s}
@keyframes litIn{from{opacity:0}to{opacity:.92}}
@keyframes candle{0%{opacity:.95}12%{opacity:.62}18%{opacity:.86}30%{opacity:1}42%{opacity:.52}50%{opacity:.78}58%{opacity:.6}70%{opacity:.98}80%{opacity:.68}88%{opacity:.9}100%{opacity:.95}}
.liftg{opacity:0;animation:fade 1.2s ease 2.4s forwards} body.ready .liftg{animation-delay:0s}
.lf{stroke:#6b3a14;stroke-width:.4}
.ray{stroke-width:1.3;stroke-linecap:round}
.moon{fill:#fbf3d5;stroke:var(--ink);stroke-width:.9}
.crater{fill:#e6dbb6;opacity:.75}
#sky{transition:none}
/* suwak czasu (podgląd) */
.scrub{display:flex;align-items:center;gap:12px;max-width:880px;margin:0 auto;padding:0 16px 36px;font-size:14px}
.scrub button{font:inherit;padding:7px 14px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:4px;cursor:pointer;min-width:118px}
.scrub input{flex:1;accent-color:var(--ink)}
.scrub output{min-width:78px;text-align:right;font-variant-numeric:tabular-nums}
.scrub small{display:block;color:#666;font-size:12px;margin-top:2px}
/* zwierzęta */
.critter .fur{fill:#a8957d;stroke:var(--ink);stroke-width:.8}
.critter .ear{fill:#bba78f;stroke:var(--ink);stroke-width:.7}
.critter .tailw{fill:#fff;stroke:var(--ink);stroke-width:.6}
.critter .hide{fill:#b9824f;stroke:var(--ink);stroke-width:.8;stroke-linejoin:round}
.critter .rump{fill:#f6efe2;stroke:var(--ink);stroke-width:.5}
.critter .leg{fill:none;stroke:#3a2a1c;stroke-width:1.3;stroke-linecap:round;stroke-linejoin:round}
.critter .eye{fill:var(--ink)}
.snowlayer{fill:url(#snowg)} .snowedge{fill:none;stroke:#8fa6bb;stroke-width:1.1;stroke-linejoin:round}
.flake{fill:#fff;stroke:#7f95aa;stroke-width:.45}
/* jeden aktor naraz: w święto gra scena świąteczna, reszta milknie */
body.feast-on .zoo,body.feast-on .tourists,body.feast-on .liftg,body.feast-on .plow{display:none!important}
body.feast-on .hut,body.feast-on .fire{display:none}
/* tryb statyczny (oszczędzanie danych): wszystko od razu w stanie końcowym */
html.static *{animation-duration:0s!important;animation-delay:0s!important;animation-iteration-count:1!important;transition:none!important}
/* napisy widoczne od początku */
.peak,.peak.on{opacity:1!important;animation:none!important}
#text{opacity:1!important;animation:none!important}
'''
SCRUB=r'''
// ===== suwak czasu: przewijanie wszystkich animacji =====
const tl=document.getElementById('tl'),tlv=document.getElementById('tlv'),playB=document.getElementById('play');
const MAXT=3600,v2t=v=>MAXT*Math.pow(v/1000,3),t2v=t=>Math.round(1000*Math.cbrt(Math.min(1,Math.max(0,t)/MAXT)));
const fmt=t=>t<60?t.toFixed(1)+' s':Math.floor(t/60)+':'+String(Math.floor(t%60)).padStart(2,'0')+' min';
const cssAnims=()=>document.getAnimations().filter(a=>typeof CSSAnimation!=='undefined'&&a instanceof CSSAnimation);
function seek(t,full){
 paused=true;pausedT=t;scrubbed=true;
 cssAnims().forEach(a=>{if(a.__st===undefined)a.__st=a.startTime!=null?a.startTime:(document.timeline.currentTime-(a.currentTime||0));
  a.pause();a.currentTime=Math.max(0,t*1000-a.__st)});
 syncLeaves(full?1e9:6000);drawPile(true);
 snowTick();
 upd(t)}
function upd(t){tlv.value=fmt(t);playB.textContent='▶ Odtwórz';playB.setAttribute('aria-pressed','true')}
function resume(){clockOff=pausedT-performance.now()/1000;paused=false;cssAnims().forEach(a=>{const ct=a.effect&&a.effect.getComputedTiming();if(!ct||ct.endTime===Infinity||a.currentTime<ct.endTime)a.play()});
 playB.textContent='⏸ Pauza';playB.setAttribute('aria-pressed','false')}
let dragging=false;
tl.addEventListener('input',()=>{dragging=true;seek(v2t(+tl.value),false)});
tl.addEventListener('change',()=>{dragging=false;seek(v2t(+tl.value),true)});
playB.onclick=()=>paused?resume():seek(now(),true);
document.getElementById('toEnd').onclick=()=>{const [,w]=hourPos();let d=HOUR-240-w;if(d<0)d+=HOUR;seek(now()+d,true)};
const clk=document.getElementById('clk');setInterval(()=>{const w=wall(),dt=new Date(w*1000);clk.value=dt.toLocaleTimeString('pl-PL')},250);
(function follow(){if(!paused&&!dragging){tl.value=t2v(now());tlv.value=fmt(now())}requestAnimationFrame(follow)})();
'''
FCSS='''
/* ===== rok kościelny ===== */
.fdraw{stroke-dasharray:1;stroke-dashoffset:1;animation:fdraw 1.1s ease-in-out var(--fd) both,ffill .9s ease calc(var(--fd) + .8s) both}
@keyframes fdraw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes ffill{from{fill-opacity:0}to{fill-opacity:1}}
@keyframes ffade{from{opacity:0}to{opacity:1}}
@keyframes glowP{0%{opacity:.55}35%{opacity:1}60%{opacity:.7}100%{opacity:.95}}
.tongue{fill:#ff9a2e;stroke:#d9531c;stroke-width:.5}
.hide-feast{display:none}
.fi{fill:none;stroke:#1d1d1b;stroke-width:1;stroke-linecap:round;stroke-linejoin:round}
.ff{stroke:#1d1d1b;stroke-width:.8;stroke-linejoin:round}
.thin{fill:none;stroke:#1d1d1b;stroke-width:.5;opacity:.7}
.needle{fill:none;stroke:#244a37;stroke-width:1.1;stroke-linecap:round}
.flame{fill:#ffb238;stroke:#d96a1c;stroke-width:.4;transform-box:fill-box;transform-origin:50% 100%;animation:flameF .7s ease-in-out infinite alternate}
@keyframes flameF{0%{transform:scale(1,1) skewX(0)}30%{transform:scale(.84,1.14) skewX(5deg)}55%{transform:scale(1.06,.9) skewX(-3deg)}80%{transform:scale(.9,1.08) skewX(-6deg)}100%{transform:scale(1.03,.95) skewX(2deg)}}
.leaflet{fill:none;stroke:#4f8a3a;stroke-width:1.1;stroke-linecap:round} .rib{fill:none;stroke:#3d6b2c;stroke-width:1.6;stroke-linecap:round}
.frond{animation:frond 4.5s ease-in-out infinite alternate} @keyframes frond{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
.stem{fill:none;stroke:#5f8f3e;stroke-width:1} .wheat{fill:none;stroke:#b8952f;stroke-width:1}
.birchleaf{fill:#8cc45a;opacity:.92} .twig{fill:none;stroke:#5b4a3a;stroke-width:.6} .crownf{fill:var(--beech)} .cloudf{fill:#fffdf8} .eye2{fill:#1d1d1b}
.ray2{stroke:#f2c14e;stroke-width:1.4;stroke-linecap:round;animation:rayp 3s ease-in-out infinite alternate}
@keyframes rayp{from{opacity:.3}to{opacity:.95}}
.starbody{fill:#fff3c4;stroke:#d9a62e;stroke-width:.8} .startail{fill:none;stroke:#fff3c4;stroke-width:2;opacity:.65;stroke-linecap:round}
.star circle{animation:twinkle 2.6s ease-in-out infinite alternate}
@keyframes graze{from{transform:translateY(0)}to{transform:translateY(2px)}}
body.f-boze .moong,body.f-boze .liftg{display:none}
body.f-pasja #hero{filter:saturate(.55)}
body.f-pasja #sky{background:linear-gradient(to bottom,#b3aed0 0%,#d9d4e6 38%,transparent 72%)!important}
body.f-palmowa #hero{filter:saturate(.85)}
body.f-pasja .flowers,body.f-wpiatek .flowers,body.f-wsobota .flowers{display:none}
body.f-wpiatek #hero{filter:grayscale(1) contrast(.92)}
body.f-wsobota #hero{filter:grayscale(.65)}
body.f-wpiatek .zoo,body.f-wsobota .zoo{display:none}
body.f-wpiatek .tree{animation:none!important}
body.f-wpiatek .rowtree{animation:fade .9s ease forwards var(--d)!important}
body.f-wielkanoc #sky{background:linear-gradient(to bottom,#a9bde6 0%,#f6cfc6 30%,#ffe6b3 50%,transparent 80%)!important}
body.f-wiecznosc #sky{background:linear-gradient(to bottom,#3d4672 0%,#8e7ea8 32%,#ead0ae 54%,transparent 80%)!important}
.datebar{display:flex;flex-wrap:wrap;align-items:center;gap:10px;max-width:880px;margin:0 auto;padding:0 16px 40px;font-size:14px}
.datebar input,.datebar select,.datebar button{font:inherit;padding:6px 10px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:4px}
.datebar output{font-weight:700}
'''
DEFS='''<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><radialGradient id="fglow"><stop offset="0" stop-color="#ffcf6b" stop-opacity=".75"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient><radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".85"/><stop offset=".6" stop-color="#e8a24a" stop-opacity=".35"/><stop offset="1" stop-color="#e8a24a" stop-opacity="0"/></radialGradient><radialGradient id="starglow"><stop offset="0" stop-color="#fff6d0" stop-opacity=".9"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></radialGradient><radialGradient id="whiteglow"><stop offset="0" stop-color="#fffdf2" stop-opacity=".95"/><stop offset="1" stop-color="#fff8dc" stop-opacity="0"/></radialGradient><linearGradient id="snowg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d6e1eb"/></linearGradient></defs></svg>'''
DATEBAR='''<div class="datebar"><label>Data podglądu: <input type="date" id="dt"></label><select id="jump"><option value="">skocz do święta…</option></select><button id="todayB">Dziś</button><output id="fname"></output></div>'''
DJS=r'''
// ===== podgląd daty =====
(function(){const dt=document.getElementById('dt'),jump=document.getElementById('jump'),y=new Date().getFullYear();
 [y,y+1].forEach(yy=>feastList(yy).forEach(([n,d])=>{const o=document.createElement('option');o.value=iso(d);o.textContent=d.getDate()+'.'+String(d.getMonth()+1).padStart(2,'0')+'.'+d.getFullYear()+' – '+n;jump.appendChild(o)}));
 const go=v=>{SIMDATE=v||null;dt.value=iso(today());applyDate(today())};
 dt.value=iso(today());dt.onchange=()=>go(dt.value);jump.onchange=()=>{if(jump.value)go(jump.value)};
 document.getElementById('todayB').onclick=()=>{jump.value='';go(null)};
 const f=feastOf(today());document.getElementById('fname').value=f?f.name:'zwykły dzień'})();
'''
extra='''
/* sezonowe dodatki */
.deco{display:none}
body[data-season="wiosna"] .only-wiosna,body[data-season="lato"] .only-lato,body[data-season="jesien"] .only-jesien,body[data-season="zima"] .only-zima{display:inline}
.sun{fill:#f7dc85;stroke:var(--ink);stroke-width:1}
.rays line{stroke:#d9a62e;stroke-width:1.3;stroke-linecap:round}
.rays{animation:spin 80s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.pylon{stroke:var(--ink);stroke-width:1.2}
.cable{fill:none;stroke:var(--ink);stroke-width:.6}
.station{fill:var(--paper);stroke:var(--ink);stroke-width:1}
.chair line,.chair path{fill:none;stroke:var(--ink);stroke-width:1;stroke-linecap:round}
.stem{fill:none;stroke:#5f8f3e;stroke-width:1}
.bloom{fill:#d2382f;stroke:#8f1f1a;stroke-width:.5}
.leafwrap{animation:fall linear infinite}
@keyframes fall{from{transform:translate(var(--x),-20px)}to{transform:translate(calc(var(--x) + var(--dx)),var(--H))}}
.leafx{stroke:#6b3a14;stroke-width:.5;transform-box:fill-box;transform-origin:50% 50%;animation:flutter ease-in-out infinite alternate}
.l1{fill:#d08a2e}.l2{fill:#b5562a}
@keyframes flutter{from{transform:rotate(-50deg)}to{transform:rotate(50deg)}}
/* rząd drzewek */
.rowtree{opacity:0;animation:fade .9s ease forwards var(--d),windRow 5s ease-in-out var(--w) infinite alternate}
@keyframes windRow{from{transform:rotate(-1.6deg)}to{transform:rotate(1.4deg)}}
@keyframes windTree{from{transform:rotate(-.9deg)}to{transform:rotate(.8deg)}}
.rleaf{fill:color-mix(in srgb,var(--spruce) 62%,var(--paper))}
.rowtree.b .rleaf{fill:color-mix(in srgb,var(--spruce) 80%,var(--paper))}
body[data-season="zima"] .rleaf:nth-of-type(2){fill:#eef0ee}
.rline{fill:none;stroke:var(--ink);stroke-width:.8;stroke-linecap:round;stroke-linejoin:round;opacity:.65}
.clouds{opacity:0;animation:fade 2s ease forwards .8s}
.peak{font-size:clamp(13px,1vw,16px)}
'''
h=h.replace("/* podgląd */",extra+CSSW+FCSS+"\n/* podgląd */")
# po zmianie rozmiaru: pokaż wszystko od razu
h=h.replace("land.querySelectorAll('.rowtree').forEach(e=>e.style.setProperty('--d','0s'));",
 "land.querySelectorAll('.rowtree,.clouds,.ridge-fill').forEach(e=>e.style.opacity=1);")
glow=('<defs><linearGradient id="litg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd37a"/><stop offset="1" stop-color="#f4a443"/></linearGradient></defs>'
 '<polygon class="lit w1" points="80.5,141 100,141 100,150 67,191 67,195 39,195"/>'
 '<polygon class="lit w2" points="119,141 141,141 186,195 156,195 156,191 119,150"/>'
 '<polygon class="lit w3" points="110.3,157 89,190 134,190"/>')
h=h.replace('<g class="logo">',glow+'<g class="logo">',1)
h=h.replace('</script>\n</body>',"setTimeout(()=>document.body.classList.add('ready'),6500);\n</script>\n</body>")
h=h.replace('<button id="again">Rysuj ponownie</button>\n</div>','<button id="again">Rysuj ponownie</button>\n</div>\n<div class="scrub"><button id="play" aria-pressed="false">⏸ Pauza</button><label style="flex:1"><input type="range" id="tl" min="0" max="1000" value="0" step="1" style="width:100%" aria-label="Czas od otwarcia strony"><small>Czas od otwarcia strony: początek suwaka to rysowanie (pierwsze sekundy), koniec to godzina.</small></label><output id="tlv">0.0 s</output></div><div class="scrub" style="padding-top:0"><button id="toEnd">⏩ 4 min przed pełną godziną</button><span>Zegar sceny: <output id="clk"></output> (liście i śnieg liczone od pełnej godziny)</span></div>',1)
h=h.replace('</script>\n</body>',SCRUB+'\n</script>\n</body>',1)
FEAST=open('feasts_js.txt').read()
assert "const mo=new Date().getMonth();" in h
h=h.replace("const mo=new Date().getMonth();",FEAST+"\nconst mo=new Date().getMonth();",1)
h=h.replace('<header id="hero">',DEFS+'<header id="hero">',1)
h=h.replace('</output></div>','</output></div>'+DATEBAR,1)
h=h.replace('</script>\n</body>',DJS+'\n</script>\n</body>',1)
open('naglowek-kompakt.html','w').write(h)
print('ok')
