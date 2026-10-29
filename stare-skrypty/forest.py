"""Generuje logo-las.html: logo Brenna-Górki + żywy las w stylu rysunku technicznego."""
import re, random
random.seed(7)

logo = open('logo.svg').read()
inner = re.search(r'<svg[^>]*>(.*)</svg>', logo, re.S).group(1)
inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
inner = inner.replace('class="ln', 'pathLength="1" class="ln')

GROUND = 240.5
ink = []      # kreski lasu (rysowane)
greens = []   # wypełnienia (rosną)

def spruce(x, base, h, w, kind='sp'):
    """Świerk: pień + 4-5 pięter trójkątnych gałęzi."""
    tiers = 5 if h > 40 else 4
    top = base - h
    pts_outline = []
    fill_polys = []
    tier_h = (h * 0.86) / tiers
    for i in range(tiers):
        ty = top + i * tier_h * 0.78
        by = ty + tier_h * 1.35
        half = w * (0.28 + 0.72 * (i + 1) / tiers) / 2
        poly = f"{x:.1f},{ty:.1f} {x - half:.1f},{by:.1f} {x + half:.1f},{by:.1f}"
        fill_polys.append(poly)
        pts_outline.append(f"M{x - half:.1f},{by:.1f} L{x:.1f},{ty:.1f} L{x + half:.1f},{by:.1f}")
    trunk = f"M{x:.1f},{top:.1f} V{base:.1f}"
    g = f'<g class="tree {kind}" style="transform-origin:{x:.1f}px {base:.1f}px">'
    g += ''.join(f'<polygon class="leaf {kind}-f" points="{p}"/>' for p in fill_polys)
    g += f'<path pathLength="1" class="fl" d="{trunk} {" ".join(pts_outline)}"/>'
    g += '</g>'
    return g

def beech(x, base, h, r):
    """Buk/liściaste: pień z rozwidleniem + korona z kilku kół (obrys cyrklem)."""
    cy = base - h + r
    blobs = [(x, cy, r), (x - r * 0.62, cy + r * 0.35, r * 0.72), (x + r * 0.64, cy + r * 0.3, r * 0.75), (x + r * 0.1, cy - r * 0.45, r * 0.7)]
    g = f'<g class="tree bk" style="transform-origin:{x:.1f}px {base:.1f}px">'
    g += ''.join(f'<circle class="leaf bk-f" cx="{cx:.1f}" cy="{cy2:.1f}" r="{rr:.1f}"/>' for cx, cy2, rr in blobs)
    d = f"M{x:.1f},{base:.1f} V{cy + r * 0.3:.1f} M{x:.1f},{cy + r * 0.75:.1f} L{x - r * 0.45:.1f},{cy + r * 0.2:.1f} M{x:.1f},{cy + r * 0.55:.1f} L{x + r * 0.5:.1f},{cy + r * 0.05:.1f}"
    g += f'<path pathLength="1" class="fl" d="{d}"/>'
    g += ''.join(f'<circle pathLength="1" class="fl" cx="{cx:.1f}" cy="{cy2:.1f}" r="{rr:.1f}"/>' for cx, cy2, rr in blobs[:1])
    g += '</g>'
    return g

# --- grzbiet gór (tło) ---
ridge = "M-60,170 C-30,150 -5,142 20,128 S70,112 95,120 S150,96 190,104 S260,92 300,108 S360,118 400,104"
ridge2 = "M-60,190 C-20,176 10,170 40,166 S120,160 160,168 S260,150 320,160 S380,170 400,164"

trees = []
# lewa kępa (za/obok kościoła w Brennej)
for x, h, w in [(-50, 46, 20), (-32, 66, 26), (-12, 80, 30), (6, 54, 22)]:
    trees.append(spruce(x, GROUND, h, w))
trees.append(beech(28, GROUND, 42, 12))
# prawa kępa (za napisem)
for x, h, w in [(338, 70, 28), (360, 54, 24), (380, 76, 30), (396, 46, 20)]:
    trees.append(spruce(x, GROUND, h, w))
trees.append(beech(318, GROUND, 40, 11))
# małe świerki pod napisem, przy Górkach
for x, h, w in [(232, 30, 14), (248, 24, 12), (296, 28, 13)]:
    trees.append(spruce(x, GROUND, h, w))

# trawa / paprocie przy ziemi
grass = []
for i in range(70):
    x = -60 + i * 6.7 + random.uniform(-1.5, 1.5)
    if 70 < x < 160:   # pod słupem zostaw czysto
        continue
    hh = random.uniform(3, 7)
    lean = random.uniform(-2, 2)
    grass.append(f"M{x:.1f},{GROUND} q{lean:.1f},{-hh * 0.6:.1f} {lean * 1.6:.1f},{-hh:.1f}")

html = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brenna-Górki – logo i las</title>
<style>
:root{{--paper:#f7f5ef;--grid:#e4e0d3;--ink:#1d1d1b;
 --spruce:#2f5d45;--spruce2:#244a37;--beech:#6f9a4a;--grass:#7aa35a;--ridge:#c9d6c2}}
body[data-season="wiosna"]{{--spruce:#3d7354;--beech:#9cc95f;--grass:#a6cf6b;--ridge:#d5e4cf}}
body[data-season="lato"]{{--spruce:#2f5d45;--beech:#5f8f3e;--grass:#78a552;--ridge:#c4d5bd}}
body[data-season="jesien"]{{--spruce:#2f5a44;--beech:#d08a2e;--grass:#b3a35a;--ridge:#e2d3b5}}
body[data-season="zima"]{{--spruce:#3c5a4c;--beech:#b9b4a6;--grass:#dcdcd4;--ridge:#e9ece9}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--paper);
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
 background-size:20px 20px;font-family:system-ui,sans-serif;color:var(--ink);transition:background-color .6s}}
.wrap{{width:min(96vw,980px);text-align:center;padding:16px}}
svg{{width:100%;height:auto;overflow:visible}}
/* kreślenie */
.ln,.fl,.rd,.gr{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .9s ease-in-out forwards}}
.fl{{fill:none;stroke:var(--ink);stroke-width:.9;stroke-linecap:round;stroke-linejoin:round}}
.rd{{fill:none;stroke:var(--ink);stroke-width:.6;opacity:.55;animation-duration:2.6s}}
.gr{{fill:none;stroke:var(--grass);stroke-width:.8;stroke-linecap:round;animation-duration:.6s}}
.ridge-fill{{fill:var(--ridge);opacity:0;animation:fade 1.4s ease forwards 3.2s;transition:fill .6s}}
#fills,#text{{opacity:0;animation:fade 1s ease forwards}}
#fills{{animation-delay:3.1s}}#text{{animation-delay:3.6s}}
/* las rośnie */
.leaf{{stroke:none;transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);opacity:0;
 animation:grow .9s cubic-bezier(.3,1.4,.5,1) forwards;transition:fill .6s}}
.sp-f{{fill:var(--spruce)}} .sp-f:nth-child(even){{fill:var(--spruce2)}}
body[data-season="zima"] .sp-f:nth-child(odd){{fill:#e9ecea}}
.bk-f{{fill:var(--beech);opacity:.92}}
.tree{{animation:sway 6s ease-in-out infinite alternate;animation-delay:6s}}
.tree:nth-of-type(3n){{animation-duration:7.5s}} .tree:nth-of-type(2n){{animation-direction:alternate-reverse}}
#logo .wh{{fill:var(--paper)}}
.ground{{stroke:var(--ink);stroke-width:1.2;fill:none}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes grow{{to{{transform:scaleY(1);opacity:1}}}}
@keyframes sway{{from{{transform:rotate(-.8deg)}}to{{transform:rotate(.8deg)}}}}
@media (prefers-reduced-motion:reduce){{
 .ln,.fl,.rd,.gr{{animation:none;stroke-dashoffset:0}}
 #fills,#text,.ridge-fill{{animation:none;opacity:1}}
 .leaf{{animation:none;transform:none;opacity:1}} .tree{{animation:none}}}}
.bar{{margin-top:14px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap}}
button{{font:inherit;font-size:14px;padding:7px 14px;border:1px solid var(--ink);background:transparent;color:var(--ink);border-radius:4px;cursor:pointer}}
button[aria-pressed="true"]{{background:var(--ink);color:var(--paper)}}
</style></head>
<body data-season="jesien"><div class="wrap">
<svg viewBox="-62 -6 466 252" role="img" aria-label="Logo Parafii Ewangelicko-Augsburskiej Brenna-Górki na tle beskidzkiego lasu">
 <defs><linearGradient id="fadeX" x1="-60" x2="400" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#fff"/><stop offset=".09" stop-color="#fff"/><stop offset=".2" stop-color="#000"/><stop offset=".84" stop-color="#000"/><stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient><mask id="sides" maskUnits="userSpaceOnUse" x="-70" y="-10" width="480" height="260"><rect x="-70" y="-10" width="480" height="260" fill="url(#fadeX)"/></mask><pattern id="hatch" width="2.2" height="20" patternUnits="userSpaceOnUse"><rect width="0.6" height="20" fill="#1d1d1b"/></pattern></defs>
 <g id="bg" mask="url(#sides)">
  <path class="ridge-fill" d="{ridge} V{GROUND} H-60 Z"/>
  <path pathLength="1" class="rd" d="{ridge}"/>
  <path pathLength="1" class="rd" d="{ridge2}" style="animation-delay:.4s;opacity:.35"/>
 </g>
 <g id="forest">{''.join(trees)}</g>
 <g id="logo">{inner}</g>
 <g id="grass">{''.join(f'<path pathLength="1" class="gr" d="{d}"/>' for d in grass)}</g>
 <path class="ground" d="M-60,{GROUND} H402"/>
</svg>
<div class="bar" role="group" aria-label="Pora roku">
 <button data-s="wiosna">Wiosna</button><button data-s="lato">Lato</button>
 <button data-s="jesien">Jesień</button><button data-s="zima">Zima</button>
 <button id="again">Rysuj ponownie</button>
</div></div>
<script>
const body=document.body;
const m=new Date().getMonth();
const auto=m<2||m==11?'zima':m<5?'wiosna':m<8?'lato':'jesien';
function setS(s){{body.dataset.season=s;document.querySelectorAll('[data-s]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===s))}}
setS(auto);
document.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>setS(b.dataset.s));
function stagger(){{
 document.querySelectorAll('#logo .ln').forEach((p,i)=>p.style.animationDelay=(i*.11)+'s');
 document.querySelectorAll('#forest .tree').forEach((t,i)=>{{
   const d=1.6+i*.14;
   t.querySelectorAll('.fl').forEach(p=>p.style.animationDelay=d+'s');
   t.querySelectorAll('.leaf').forEach((l,j)=>l.style.animationDelay=(4.1+i*.08+j*.07)+'s');
 }});
 document.querySelectorAll('#grass .gr').forEach((g,i)=>g.style.animationDelay=(4.4+(i%20)*.04)+'s');
}}
stagger();
document.getElementById('again').onclick=()=>{{const s=document.querySelector('svg');const c=s.cloneNode(true);s.replaceWith(c);stagger();}};
</script></body></html>'''
open('logo-las.html', 'w').write(html)
print('ok', len(html))
