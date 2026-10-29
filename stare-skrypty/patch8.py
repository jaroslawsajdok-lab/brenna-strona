s=open('header2_js.txt').read()
R=[("moonG=el('g',{class:'deco only-zima'});","moonG=el('g',{class:'deco only-zima moong'});"),
(" land.appendChild(clouds);\n"," land.appendChild(clouds);\n skyL=el('g',{class:'feast'});land.appendChild(skyL);\n"),
("const bl=el('path',{class:'ridge-line back draw',d:toD(back)});land.appendChild(bl);","const bl=el('path',{class:'ridge-line back draw',d:toD(back)});land.appendChild(bl);\n ridgeL=el('g',{class:'feast'});land.appendChild(ridgeL);"),
("fl=el('g',{class:'deco only-wiosna'});","fl=el('g',{class:'deco only-wiosna flowers'});"),
(" front.appendChild(zoo);"," groundL=el('g',{class:'feast'});front.appendChild(groundL);\n front.appendChild(zoo);"),
("\n first=false;\n","\n LY={W,H,groundY,k,mobile,sceneW,th,topBack,row};drawFeast();\n first=false;\n"),
(" skyTick(ts);critterTick();\n"," skyTick(ts);critterTick();feastTick();\n"),
("setS(mo<2||mo==11?'zima':mo<5?'wiosna':mo<8?'lato':'jesien');","applyDate(today());"),
]
for a,b in R:
    assert s.count(a)==1,(s.count(a),a[:60]); s=s.replace(a,b)
open('header2_js.txt','w').write(s)

m=open('make_compact.py').read()
FCSS=r'''
/* ===== rok kościelny ===== */
.feast{opacity:0;animation:fade 1.2s ease 4.4s forwards} body.ready .feast{animation-delay:0s}
.hide-feast{display:none}
.fi{fill:none;stroke:#1d1d1b;stroke-width:1;stroke-linecap:round;stroke-linejoin:round}
.ff{stroke:#1d1d1b;stroke-width:.8;stroke-linejoin:round}
.thin{fill:none;stroke:#1d1d1b;stroke-width:.5;opacity:.7}
.needle{fill:none;stroke:#244a37;stroke-width:1.1;stroke-linecap:round}
.flame{fill:#ffb238;stroke:#d96a1c;stroke-width:.4;transform-box:fill-box;transform-origin:50% 100%;animation:flameF .7s ease-in-out infinite alternate}
@keyframes flameF{0%{transform:scale(1,1) skewX(0)}50%{transform:scale(.9,1.1) skewX(3deg)}100%{transform:scale(1.04,.93) skewX(-2deg)}}
.leaflet{fill:none;stroke:#4f8a3a;stroke-width:1.1;stroke-linecap:round} .rib{fill:none;stroke:#3d6b2c;stroke-width:1.6;stroke-linecap:round}
.frond{animation:frond 4.5s ease-in-out infinite alternate} @keyframes frond{from{transform:rotate(-3deg)}to{transform:rotate(3deg)}}
.stem{fill:none;stroke:#5f8f3e;stroke-width:1} .wheat{fill:none;stroke:#b8952f;stroke-width:1}
.birch{fill:#9fd06a} .crownf{fill:var(--beech)} .cloudf{fill:#fffdf8} .eye2{fill:#1d1d1b}
.ray2{stroke:#f2c14e;stroke-width:1.4;stroke-linecap:round;animation:rayp 3s ease-in-out infinite alternate}
@keyframes rayp{from{opacity:.3}to{opacity:.95}}
.starbody{fill:#fff3c4;stroke:#d9a62e;stroke-width:.8} .startail{fill:none;stroke:#fff3c4;stroke-width:2;opacity:.65;stroke-linecap:round}
.star circle{animation:twinkle 2.6s ease-in-out infinite alternate}
@keyframes graze{from{transform:translateY(0)}to{transform:translateY(2px)}}
body.f-boze .moong{display:none}
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
DEFS='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'+ \
 '<radialGradient id="fglow"><stop offset="0" stop-color="#ffcf6b" stop-opacity=".75"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient>'+ \
 '<radialGradient id="warm"><stop offset="0" stop-color="#ffd27a" stop-opacity=".85"/><stop offset=".6" stop-color="#e8a24a" stop-opacity=".35"/><stop offset="1" stop-color="#e8a24a" stop-opacity="0"/></radialGradient>'+ \
 '<radialGradient id="starglow"><stop offset="0" stop-color="#fff6d0" stop-opacity=".9"/><stop offset="1" stop-color="#fff6d0" stop-opacity="0"/></radialGradient>'+ \
 '<radialGradient id="whiteglow"><stop offset="0" stop-color="#fffdf2" stop-opacity=".95"/><stop offset="1" stop-color="#fff8dc" stop-opacity="0"/></radialGradient>'+ \
 '</defs></svg>'
DATEBAR='<div class="datebar"><label>Data podglądu: <input type="date" id="dt"></label><select id="jump"><option value="">skocz do święta…</option></select><button id="todayB">Dziś</button><output id="fname"></output></div>'
DJS=r'''
// ===== podgląd daty =====
(function(){const dt=document.getElementById('dt'),jump=document.getElementById('jump'),y=new Date().getFullYear();
 [y,y+1].forEach(yy=>feastList(yy).forEach(([n,d])=>{const o=document.createElement('option');o.value=iso(d);o.textContent=d.getDate()+'.'+String(d.getMonth()+1).padStart(2,'0')+'.'+d.getFullYear()+' – '+n;jump.appendChild(o)}));
 const go=v=>{SIMDATE=v||null;dt.value=iso(today());applyDate(today())};
 dt.value=iso(today());dt.onchange=()=>go(dt.value);jump.onchange=()=>{if(jump.value)go(jump.value)};
 document.getElementById('todayB').onclick=()=>{jump.value='';go(null)};
 const f=feastOf(today());document.getElementById('fname').value=f?f.name:'zwykły dzień'})();
'''
FEAST=open('feasts_js.txt').read()
m=m.replace("extra='''","FCSS='''"+FCSS+"'''\nDEFS='''"+DEFS+"'''\nDATEBAR='''"+DATEBAR+"'''\nDJS=r'''"+DJS+"'''\nextra='''",1)
m=m.replace('h=h.replace("/* podgląd */",extra+CSSW+"\\n/* podgląd */")','h=h.replace("/* podgląd */",extra+CSSW+FCSS+"\\n/* podgląd */")')
m=m.replace("open('naglowek-kompakt.html','w').write(h)","""FEAST=open('feasts_js.txt').read()
assert "const mo=new Date().getMonth();" in h
h=h.replace("const mo=new Date().getMonth();",FEAST+"\\nconst mo=new Date().getMonth();",1)
h=h.replace('<header id="hero">',DEFS+'<header id="hero">',1)
h=h.replace('</output></div>','</output></div>'+DATEBAR,1)
h=h.replace('</script>\\n</body>',DJS+'\\n</script>\\n</body>',1)
open('naglowek-kompakt.html','w').write(h)""",1)
open('make_compact.py','w').write(m)
print('ok')
