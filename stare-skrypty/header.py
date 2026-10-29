"""naglowek.html — prototyp nagłówka strony Brenna-Górki:
niebo z chmurami, linia gór przez całą szerokość z wpisanym menu (jak opisy poziomic),
logo z lasem w tle (drzewa w całości)."""
import re, random

ns = {}
exec(open('forest3.py').read().split("def scene")[0], ns)
spruce, beech, inner, SIL = ns['spruce'], ns['beech'], ns['inner'], ns['SIL']
css_logo = re.search(r'<style>(.*?)</style>', open('logo.svg').read(), re.S).group(1)

rng = random.Random(5)
far, back = [], []
x = -58
while x < 404:
    h = rng.uniform(88, 128)
    if 208 < x < 338:
        h = rng.uniform(34, 44)
    far.append(beech(x, 244, h*.7, h*.19, 'far') if rng.random() < .22 else spruce(x, 244, h, h*rng.uniform(.36, .42), 'far'))
    x += rng.uniform(34, 46)
for x, h, b in [(-44,150,0),(-10,172,0),(22,118,1),(58,160,0),(132,168,0),(168,150,0),(244,42,0),(296,38,1),(356,176,0),(386,138,0),(404,160,0)]:
    x += rng.uniform(-4, 4)
    back.append(beech(x, 245, h*.72, h*.2, 'near') if b else spruce(x, 245, h, h*rng.uniform(.36, .42), 'near'))

# viewBox obejmuje całe korony skrajnych drzew (najszersze ~±40 jednostek)
VB = "-96 -8 540 254"
SIL = SIL.replace("H153.5 V204 H152 V216 L94,240 H74 V204 H70.5", "H153.5 V204 H70.5")
scene = (f'<svg id="scene" viewBox="{VB}" role="img" aria-label="Kościoły w Brennej i Górkach na tle beskidzkiego lasu">'
         '<defs><pattern id="hatch" width="2.2" height="20" patternUnits="userSpaceOnUse"><rect width="0.6" height="20" fill="#1d1d1b"/></pattern></defs>'
         f'<g class="forest">{"".join(far)}{"".join(back)}</g>'
         f'<rect class="sil-post" x="70.5" y="203" width="83" height="42"/><path class="sil" d="{SIL}"/><g class="logo">{inner}</g></svg>')

MENU = [("Aktualności", "#aktualnosci"), ("Nabożeństwa", "#nabozenstwa"),
        ("Parafia", "#parafia"), ("Jak dojechać", "#dojazd"), ("Kontakt", "#kontakt")]
menu_html = ''.join(f'<a class="peak" href="{h}">{t}</a>' for t, h in MENU)

html = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Parafia Ewangelicko-Augsburska Brenna-Górki</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap" rel="stylesheet">
<style>{css_logo}
:root{{--paper:#f7f5ef;--grid:#e6e2d6;--ink:#1d1d1b;--sky:#cfe2ec;--spruce:#2f5d45;--beech:#6f9a4a;--grass:#7aa35a;--ridge:#c9d6c2;--ridge2:#e3eadf}}
body[data-season="wiosna"]{{--spruce:#3d7354;--beech:#9cc95f;--grass:#a6cf6b;--ridge:#d5e4cf;--ridge2:#e8f0e3;--sky:#d3e7f2}}
body[data-season="lato"]{{--spruce:#2f5d45;--beech:#5f8f3e;--grass:#78a552;--ridge:#c4d5bd;--ridge2:#e0e9dc;--sky:#c6dfee}}
body[data-season="jesien"]{{--spruce:#2f5a44;--beech:#d08a2e;--grass:#b3a35a;--ridge:#e2d3b5;--ridge2:#eee6d4;--sky:#d4e2ea}}
body[data-season="zima"]{{--spruce:#3c5a4c;--beech:#b9b4a6;--grass:#dcdcd4;--ridge:#eceeed;--ridge2:#f3f4f3;--sky:#dfe6ea}}
*{{box-sizing:border-box}}
html,body{{margin:0}}
body{{background:var(--paper);color:var(--ink);font-family:'PT Sans',system-ui,sans-serif;
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:24px 24px}}

/* ===== NAGŁÓWEK ===== */
#hero{{position:relative;height:clamp(520px,78vh,800px);overflow:hidden}}
@media (max-width:900px){{#hero{{height:calc(min(100vw,560px)*1.02 + 90px)}}}}
#sky{{position:absolute;inset:0;background:linear-gradient(to bottom,var(--sky) 0%,color-mix(in srgb,var(--sky) 45%,transparent) 38%,transparent 62%);opacity:0;animation:fade 2s ease forwards .2s}}
#land{{position:absolute;inset:0;width:100%;height:100%;overflow:visible}}
#scene{{position:absolute;left:50%;bottom:var(--groundGap);transform:translateX(-50%);width:var(--sceneW);height:auto;overflow:visible}}
#front{{position:absolute;inset:0;width:100%;height:100%;pointer-events:none}}

/* chmury: obrys cyrklem + miękkie wypełnienie, powoli dryfują */
.cloud{{animation:drift linear infinite}}
.cloud path{{fill:color-mix(in srgb,#fff 82%,transparent);stroke:var(--ink);stroke-width:1;stroke-opacity:.35}}
@keyframes drift{{from{{transform:translateX(var(--from))}}to{{transform:translateX(var(--to))}}}}

/* linia gór */
.ridge-line{{fill:none;stroke:var(--ink);stroke-width:1.3;stroke-linecap:round}}
.ridge-line.back{{stroke-width:.8;opacity:.4}}
.ridge-fill.back{{fill:var(--ridge2)}}
.draw{{stroke-dasharray:var(--len);stroke-dashoffset:var(--len);animation:draw 2.4s ease-in-out forwards}}
.ridge-fill{{opacity:0;animation:fade 1.6s ease forwards 2.2s}}

/* menu wpisane w linię gór – jak opis poziomicy */
nav{{position:absolute;inset:0;pointer-events:none}}
.peak{{position:absolute;left:0;top:0;pointer-events:auto;font-size:clamp(14px,1.05vw,17px);letter-spacing:.06em;text-transform:uppercase;
 color:var(--ink);text-decoration:none;white-space:nowrap;padding:6px 4px;line-height:1;
 transform-origin:50% 50%;opacity:0;transition:color .2s}}
.peak.on{{animation:fade .6s ease forwards}}
.peak::after{{content:"";position:absolute;left:50%;bottom:-1px;width:0;height:2px;background:var(--spruce);transition:all .25s;transform:translateX(-50%)}}
.peak:hover,.peak:focus-visible{{color:var(--spruce);outline:none}}
.peak:hover::after,.peak:focus-visible::after{{width:100%}}
.tick{{stroke:var(--ink);stroke-width:1}}

/* las i logo (jak w prototypie) */
.logo .wh,.sil{{fill:var(--paper)}} .sil,.sil-post{{opacity:0;animation:fade 1s ease forwards 2.4s}} .sil-post{{fill:color-mix(in srgb,var(--ridge) 55%,var(--paper))}}
.ln,.fl{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .9s ease-in-out forwards}}
.fl{{fill:none;stroke:var(--ink);stroke-width:.85;stroke-linecap:round;stroke-linejoin:round}}
.far .fl{{stroke-width:.7;opacity:.55}} .near .fl{{stroke-width:1}}
#fills,#text{{opacity:0;animation:fade 1s ease forwards}}
#fills{{animation-delay:3.4s}}#text{{animation-delay:3.9s}}
.leaf{{stroke:none;transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);opacity:0;animation:grow .9s cubic-bezier(.3,1.4,.5,1) forwards}}
.sp-f{{fill:var(--spruce)}} .bk-f{{fill:var(--beech)}}
.far .sp-f{{fill:color-mix(in srgb,var(--spruce) 50%,var(--paper))}} .far .bk-f{{fill:color-mix(in srgb,var(--beech) 50%,var(--paper))}}
.near .sp-f:nth-child(even){{fill:color-mix(in srgb,var(--spruce) 88%,#000)}}
body[data-season="zima"] .sp-f:nth-child(odd){{fill:#eef0ee}}
.tree{{animation:sway 6s ease-in-out infinite alternate 7s}}
.tree:nth-child(3n){{animation-duration:7.5s}} .tree:nth-child(2n){{animation-direction:alternate-reverse}}
.ground{{stroke:var(--ink);stroke-width:1.3}}
.gr{{fill:none;stroke:var(--grass);stroke-width:1.1;stroke-linecap:round;opacity:0;animation:fade .8s ease forwards 5s}}

@keyframes draw{{to{{stroke-dashoffset:0}}}} @keyframes fade{{to{{opacity:1}}}}
@keyframes grow{{to{{transform:scaleY(1);opacity:1}}}} @keyframes sway{{from{{transform:rotate(-.7deg)}}to{{transform:rotate(.7deg)}}}}

/* telefon: menu chowa się pod przyciskiem */
#burger{{display:none;position:absolute;top:14px;right:14px;z-index:5;font:inherit;font-size:15px;letter-spacing:.06em;text-transform:uppercase;
 background:var(--paper);border:1px solid var(--ink);padding:8px 12px;border-radius:3px;cursor:pointer}}
@media (max-width:900px){{
 #burger{{display:block}}
 nav{{position:absolute;inset:auto 14px auto auto;top:58px;z-index:5;display:none;flex-direction:column;background:var(--paper);border:1px solid var(--ink);padding:6px 4px;pointer-events:auto}}
 nav.open{{display:flex}}
 .peak{{position:static;transform:none!important;opacity:1!important;animation:none!important;padding:10px 14px}}
}}
@media (prefers-reduced-motion:reduce){{
 *{{animation-duration:0s!important;animation-delay:0s!important}}
 .cloud,.tree{{animation:none!important}}
}}

/* podgląd */
.bar{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;padding:22px 16px 40px}}
.bar button{{font:inherit;font-size:14px;padding:7px 14px;border:1px solid var(--ink);background:var(--paper);color:var(--ink);border-radius:4px;cursor:pointer}}
.bar button[aria-pressed="true"]{{background:var(--ink);color:var(--paper)}}
.below{{max-width:880px;margin:0 auto;padding:10px 20px 0;color:#555;font-size:15px;text-align:center}}
</style></head>
<body data-season="jesien">
<header id="hero">
 <div id="sky"></div>
 <svg id="land" aria-hidden="true"></svg>
 {scene}
 <svg id="front" aria-hidden="true"></svg>
 <button id="burger" aria-expanded="false" aria-controls="menu">Menu</button>
 <nav id="menu" aria-label="Menu główne">{menu_html}</nav>
</header>
<p class="below">Prototyp nagłówka. Poniżej będą nabożeństwa, aktualności z Facebooka i reszta strony.</p>
<div class="bar" role="group" aria-label="Pora roku">
 <button data-s="wiosna">Wiosna</button><button data-s="lato">Lato</button><button data-s="jesien">Jesień</button><button data-s="zima">Zima</button>
 <button id="again">Rysuj ponownie</button>
</div>
<script>
const NS='http://www.w3.org/2000/svg';
const hero=document.getElementById('hero'),land=document.getElementById('land'),front=document.getElementById('front'),
      scene=document.getElementById('scene'),nav=document.getElementById('menu'),peaks=[...nav.querySelectorAll('.peak')];
const VB={{x:-96,y:-8,w:540,h:254}};          // viewBox sceny
const el=(t,a={{}})=>{{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);return e}};

// profil Beskidu: suma łagodnych fal, stały kształt niezależny od szerokości
function ridgeY(x,W,H,top,amp){{const t=x/Math.max(W,1150);
 return H*(top+amp*(.55*Math.sin(t*6.283*1.15+.6)+.3*Math.sin(t*6.283*2.7+1.9)+.12*Math.sin(t*6.283*6.1+.4)+.05*Math.sin(t*6.283*13+2)))}}

let first=true;
function layout(){{
 const W=hero.clientWidth,H=hero.clientHeight,mobile=W<=900;
 // scena: na szerokim ekranie zostawia boki na menu; zawsze w całości
 const sceneW=Math.min(mobile?W*1.04:W*.56, 980, (H*.86)*VB.w/VB.h);
 const groundGap=Math.round(H*.05);
 hero.style.setProperty('--sceneW',sceneW+'px');hero.style.setProperty('--groundGap',groundGap+'px');
 const sceneH=sceneW*VB.h/VB.w, sceneTop=H-groundGap-sceneH, groundY=H-groundGap- sceneH*(VB.h-(244-VB.y))/VB.h;
 const u=sceneH/VB.h;                         // 1 jednostka sceny w px
 land.setAttribute('viewBox',`0 0 ${{W}} ${{H}}`);front.setAttribute('viewBox',`0 0 ${{W}} ${{H}}`);
 land.innerHTML='';front.innerHTML='';

 // chmury
 const clouds=el('g');[[.12,.13,1],[.46,.07,.8],[.78,.17,1.1],[.3,.24,.7]].forEach(([cx,cy,s],i)=>{{
  const g=el('g',{{class:'cloud'}});const k=s*Math.min(1,W/1200)*1.1;
  const p=el('path',{{d:`M${{-60*k}},0 a${{22*k}},${{22*k}} 0 0 1 ${{30*k}},${{-18*k}} a${{30*k}},${{30*k}} 0 0 1 ${{52*k}},${{-6*k}} a${{20*k}},${{20*k}} 0 0 1 ${{36*k}},${{10*k}} a${{14*k}},${{14*k}} 0 0 1 ${{2*k}},${{14*k}} Z`}});
  g.appendChild(p);g.style.setProperty('--from',(cx*W-40)+'px');g.style.setProperty('--to',(cx*W+40)+'px');
  g.style.animationDuration=(60+i*17)+'s';g.style.animationDirection=i%2?'alternate-reverse':'alternate';
  const wrap=el('g',{{transform:`translate(0 ${{cy*H}})`}});wrap.appendChild(g);clouds.appendChild(wrap)}});
 clouds.style.opacity=0;clouds.style.animation='fade 2s ease forwards .8s';land.appendChild(clouds);

 // dwie linie gór: dalsza (jaśniejsza) i główna z menu
 const step=6,pts=(top,amp,shift=0)=>{{const a=[];for(let x=-10;x<=W+10;x+=step)a.push([x,ridgeY(x+shift,W,H,top,amp)]);return a}};
 const toD=a=>'M'+a.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' L');
 const topMain=Math.min(.5,(sceneTop+ sceneH*.30)/H), back=pts(topMain-.09,.05,W*.37), main=pts(topMain,.075);
 land.appendChild(el('path',{{class:'ridge-fill back',d:toD(back)+` L${{W+10}},${{H}} L-10,${{H}} Z`}}));
 const bl=el('path',{{class:'ridge-line back draw',d:toD(back)}});land.appendChild(bl);
 const defs=el('defs');const lg=el('linearGradient',{{id:'rg',x1:0,x2:0,y1:0,y2:1}});
 lg.appendChild(el('stop',{{offset:0,'stop-color':'var(--ridge)'}}));lg.appendChild(el('stop',{{offset:1,'stop-color':'color-mix(in srgb,var(--ridge) 45%,var(--paper))'}}));
 defs.appendChild(lg);land.appendChild(defs);
 land.appendChild(el('path',{{class:'ridge-fill',fill:'url(#rg)',d:toD(main)+` L${{W+10}},${{H}} L-10,${{H}} Z`}}));

 // pozycje menu: na bokach, poza sceną (na telefonie menu jest w liście)
 const gaps=[];
 if(!mobile){{
  const sL=(W-sceneW)/2+sceneW*.06, sR=(W+sceneW)/2-sceneW*.04;
  const left=peaks.slice(0,3),right=peaks.slice(3);
  const place=(arr,x0,x1)=>{{const ws=arr.map(a=>a.offsetWidth),gap=Math.max(14,((x1-x0)-ws.reduce((p,c)=>p+c,0))/(arr.length+1));let cur=x0+gap;
   arr.forEach((a,i)=>{{
   const x=cur+ws[i]/2; cur+=ws[i]+gap; const y=ridgeY(x,W,H,topMain,.075);
   const dy=ridgeY(x+8,W,H,topMain,.075)-ridgeY(x-8,W,H,topMain,.075);
   const ang=Math.max(-8,Math.min(8,Math.atan2(dy,16)*180/Math.PI));
   const w=a.offsetWidth;
   a.style.transform=`translate(${{x-w/2}}px,${{y-a.offsetHeight/2}}px) rotate(${{ang}}deg)`;
   gaps.push([x-w/2-10,x+w/2+10]);}})}};
  place(left,24,sL); place(right,sR,W-24);
 }}
 // główna linia z przerwami na opisy
 const segs=[];let cur=null;
 for(const [x,y] of main){{const inGap=gaps.some(([a,b])=>x>a&&x<b);
  if(inGap){{cur=null;continue}} if(!cur){{cur=[];segs.push(cur)}} cur.push([x,y])}}
 const d=segs.filter(sg=>sg.length&&sg[sg.length-1][0]-sg[0][0]>30).map(sg=>'M'+sg.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' L')).join(' ');
 const ml=el('path',{{class:'ridge-line draw',d}});land.appendChild(ml);
 [bl,ml].forEach(p=>{{const L=p.getTotalLength();p.style.setProperty('--len',L)}});
 if(!first){{[bl,ml].forEach(p=>{{p.style.animation='none';p.style.strokeDashoffset=0}});land.querySelectorAll('.ridge-fill,g').forEach(g=>{{g.style.animation='none';g.style.opacity=1}})}}

 // ziemia i trawa na całą szerokość (z przodu)
 front.appendChild(el('line',{{class:'ground',x1:0,x2:W,y1:groundY,y2:groundY}}));
 const gr=el('g');let s=1;const rnd=()=>(s=(s*16807)%2147483647)/2147483647;
 for(let x=4;x<W;x+=9+rnd()*6){{const h=4+rnd()*7,l=(rnd()-.5)*5;
  gr.appendChild(el('path',{{class:'gr',d:`M${{x.toFixed(1)}},${{groundY}} q${{l.toFixed(1)}},${{(-h*.6).toFixed(1)}} ${{(l*1.6).toFixed(1)}},${{(-h).toFixed(1)}}`}}))}}
 if(!first)gr.querySelectorAll('.gr').forEach(g=>{{g.style.animation='none';g.style.opacity=1}});
 front.appendChild(gr);
 // menu pojawia się, gdy linia dojdzie do miejsca opisu
 peaks.forEach((a,i)=>{{a.classList.add('on');a.style.animationDelay=first?(1.2+i*.25)+'s':'0s'}});
 first=false;
}}
function stagger(){{
 scene.querySelectorAll('.logo .ln').forEach((p,i)=>p.style.animationDelay=(.6+i*.1)+'s');
 scene.querySelectorAll('.tree').forEach((t,i)=>{{const pl=t.classList.contains('far')?0:1,d=3.4+pl*.4+(i%12)*.12;
  t.querySelectorAll('.fl').forEach(p=>p.style.animationDelay=d+'s');
  t.querySelectorAll('.leaf').forEach((l,j)=>l.style.animationDelay=(4.8+pl*.3+(i%12)*.06+j*.06)+'s')}});
}}
stagger();
Promise.race([document.fonts?document.fonts.ready:Promise.resolve(),new Promise(r=>setTimeout(r,700))]).then(()=>{{
 layout();let rt;addEventListener('resize',()=>{{clearTimeout(rt);rt=setTimeout(layout,120)}})}});
const burger=document.getElementById('burger');
burger.onclick=()=>{{const o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)}};
const mo=new Date().getMonth();
function setS(s){{document.body.dataset.season=s;document.querySelectorAll('[data-s]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===s))}}
setS(mo<2||mo==11?'zima':mo<5?'wiosna':mo<8?'lato':'jesien');
document.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>setS(b.dataset.s));
document.getElementById('again').onclick=()=>location.reload();
</script></body></html>'''
open('naglowek.html', 'w').write(html)
print('ok', len(html)//1024, 'KB')
