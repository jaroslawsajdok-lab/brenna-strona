s=open('header2_js.txt').read()
anchor=" land.appendChild(row);\n"
assert anchor in s
winter=r""" land.appendChild(row);

 // ===== ZIMOWY WIECZÓR: gwiazdy, chata z kominkiem, ognisko =====
 const stars=el('g',{class:'deco only-zima stars'});
 for(let j=0;j<(mobile?14:34);j++){const x=rnd()*W,y=rnd()*H*.32,r=(.6+rnd()*1.1)*k;
  const c=el('circle',{cx:x.toFixed(1),cy:y.toFixed(1),r:r.toFixed(2)});c.style.animationDelay=(-rnd()*4)+'s';c.style.animationDuration=(2.5+rnd()*3)+'s';stars.appendChild(c)}
 land.insertBefore(stars,land.firstChild);

 const ws=Math.max(.7,th/52);                                  // skala chaty
 const cx=mobile?W*.06+30*ws:(W-sceneW)/2-th*1.9, gy=groundY;   // przy lewym skraju sceny
 row.querySelectorAll('.rowtree').forEach(t=>{const tx=parseFloat(t.style.transformOrigin);if(Math.abs(tx-cx)<46*ws||Math.abs(tx-(cx+44*ws))<22*ws)t.classList.add('hide-zima')});
 const hut=el('g',{class:'deco only-zima hut'});
 const bw=40*ws,bh=20*ws,rh=22*ws,x0=cx-bw/2;
 // komin + dym
 hut.appendChild(el('rect',{class:'hut-wall',x:x0+bw*.66,y:gy-bh-rh*.95,width:5*ws,height:rh*.6}));
 const smoke=el('g',{class:'smoke'});
 for(let j=0;j<5;j++){const p=el('circle',{cx:x0+bw*.66+2.5*ws,cy:gy-bh-rh*.98,r:3*ws});p.style.animationDelay=(j*.9)+'s';smoke.appendChild(p)}
 hut.appendChild(smoke);
 // ściana z bali
 hut.appendChild(el('rect',{class:'hut-wall',x:x0,y:gy-bh,width:bw,height:bh}));
 for(let j=1;j<5;j++)hut.appendChild(el('line',{class:'hut-log',x1:x0,x2:x0+bw,y1:gy-bh*j/5,y2:gy-bh*j/5}));
 // okna z ciepłym światłem
 [[.22],[.62]].forEach(([f])=>{const wx=x0+bw*f,wy=gy-bh*.72,ww=7*ws,wh=7*ws;
  hut.appendChild(el('rect',{class:'glow',x:wx-ww*.9,y:wy-wh*.9,width:ww*2.8,height:wh*2.8,rx:ww}));
  hut.appendChild(el('rect',{class:'win',x:wx,y:wy,width:ww,height:wh}));
  hut.appendChild(el('path',{class:'hut-line',d:`M${wx+ww/2},${wy} V${wy+wh} M${wx},${wy+wh/2} H${wx+ww}`}))});
 // stromy góralski dach ze śniegiem
 hut.appendChild(el('path',{class:'hut-roof',d:`M${x0-5*ws},${gy-bh} L${cx},${gy-bh-rh} L${x0+bw+5*ws},${gy-bh} Z`}));
 hut.appendChild(el('path',{class:'snowcap',d:`M${x0-5*ws},${gy-bh} L${cx},${gy-bh-rh} L${x0+bw+5*ws},${gy-bh} L${x0+bw+1*ws},${gy-bh+1.5*ws} L${cx},${gy-bh-rh+5*ws} L${x0-1*ws},${gy-bh+1.5*ws} Z`}));
 hut.appendChild(el('path',{class:'hut-line',d:`M${x0-5*ws},${gy-bh} L${cx},${gy-bh-rh} L${x0+bw+5*ws},${gy-bh} M${x0},${gy-bh} V${gy} M${x0+bw},${gy-bh} V${gy}`}));
 land.appendChild(hut);

 // ognisko obok chaty
 const fx=cx+bw*.5+16*ws,fire=el('g',{class:'deco only-zima fire'});
 fire.appendChild(el('ellipse',{class:'fglow',cx:fx,cy:gy-4*ws,rx:22*ws,ry:14*ws}));
 fire.appendChild(el('path',{class:'hut-line logs',d:`M${fx-8*ws},${gy} L${fx+8*ws},${gy-4*ws} M${fx+8*ws},${gy} L${fx-8*ws},${gy-4*ws}`}));
 [[0,1,'f1'],[-3,.7,'f2'],[3,.75,'f2'],[0,.5,'f3']].forEach(([dx,s,c],j)=>{const h=13*ws*s,w=5*ws*s,bx=fx+dx*ws,by=gy-3*ws;
  const f=el('path',{class:'flame '+c,d:`M${bx-w},${by} Q${bx-w},${by-h*.55} ${bx},${by-h} Q${bx+w},${by-h*.55} ${bx+w},${by} Z`,style:`transform-origin:${bx}px ${by}px`});
  f.style.animationDelay=(-j*.23)+'s';fire.appendChild(f)});
 for(let j=0;j<6;j++){const sp=el('circle',{class:'spark',cx:fx+(rnd()-.5)*6*ws,cy:gy-12*ws,r:.9*ws});
  sp.style.setProperty('--sx',((rnd()-.5)*18*ws)+'px');sp.style.setProperty('--sy',(-(24+rnd()*20)*ws)+'px');sp.style.animationDelay=(-rnd()*2.4)+'s';fire.appendChild(sp)}
 land.appendChild(fire);
"""
s=s.replace(anchor,winter,1)
open('header2_js.txt','w').write(s)

m=open('make_compact.py').read()
css=r'''
/* ===== zimowy wieczór ===== */
body[data-season="zima"]{--ridge:#e6e9ee;--ridge2:#d3dae4}
body[data-season="zima"] #sky{background:linear-gradient(to bottom,#24395a 0%,#4f6a8f 28%,#b9b7c4 52%,#f0d2b4 66%,transparent 80%)}
body[data-season="zima"] .cloud path{fill:color-mix(in srgb,#c9d3e2 70%,transparent);stroke-opacity:.2}
.stars circle{fill:#fff6dc;animation:twinkle ease-in-out infinite alternate}
@keyframes twinkle{from{opacity:.25}to{opacity:1}}
.hut-wall{fill:#8a6a4a;stroke:var(--ink);stroke-width:.9}
.hut-log{stroke:#5b4330;stroke-width:.6}
.hut-roof{fill:#5a4636}
.snowcap{fill:#f7f8fa}
.hut-line{fill:none;stroke:var(--ink);stroke-width:1;stroke-linecap:round;stroke-linejoin:round}
.win{fill:#ffcf6b;stroke:var(--ink);stroke-width:.8;animation:flick 3.2s ease-in-out infinite alternate}
.glow{fill:#ffb347;opacity:.35;filter:blur(4px);animation:flick 2.6s ease-in-out infinite alternate}
@keyframes flick{0%{opacity:.85}40%{opacity:1}70%{opacity:.78}100%{opacity:.95}}
.smoke circle{fill:#c9cdd4;opacity:0;animation:smoke 4.5s ease-out infinite}
@keyframes smoke{0%{opacity:0;transform:translate(0,0) scale(.6)}15%{opacity:.7}100%{opacity:0;transform:translate(10px,-34px) scale(2.4)}}
.smoke circle{transform-box:fill-box;transform-origin:50% 50%}
.fglow{fill:#ff9a3c;opacity:.35;filter:blur(6px);animation:pulse 1.6s ease-in-out infinite alternate}
@keyframes pulse{from{opacity:.25}to{opacity:.5}}
.flame{animation:burn .5s ease-in-out infinite alternate}
.f1{fill:#f08a24}.f2{fill:#e2552a}.f3{fill:#ffd765}
@keyframes burn{from{transform:scale(1,1) skewX(0)}to{transform:scale(.92,1.15) skewX(4deg)}}
.logs{stroke:#5b4330;stroke-width:2.2}
.spark{fill:#ffd765;animation:spark 2.4s linear infinite}
@keyframes spark{0%{opacity:1;transform:translate(0,0)}100%{opacity:0;transform:translate(var(--sx),var(--sy))}}
body[data-season="zima"] .hide-zima{display:none}
/* ciepłe okno kościoła w Górkach */
body[data-season="zima"] .logo path.bk[d^="M190,105.5"]{fill:#ffcf6b;filter:drop-shadow(0 0 3px #ffb347) drop-shadow(0 0 7px #ff9a3c);animation:flick 3.6s ease-in-out infinite alternate}
'''
m=m.replace("/* podgląd */",css+"\n/* podgląd */") if "/* podgląd */" in m else m
m=m.replace("h=h.replace(\"/* podgląd */\",extra+\"\\n/* podgląd */\")","h=h.replace(\"/* podgląd */\",extra+CSSW+\"\\n/* podgląd */\")")
m=m.replace("extra='''","CSSW='''"+css+"'''\nextra='''",1)
open('make_compact.py','w').write(m)
print('ok')
