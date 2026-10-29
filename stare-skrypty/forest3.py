"""logo-las.html: logo Brenna-Górki + gęsty las w 3 planach, wersja pozioma i pionowa."""
import re, random

logo = open('logo.svg').read()
inner = re.search(r'<svg[^>]*>(.*)</svg>', logo, re.S).group(1)
inner = re.sub(r'<title>.*?</title>', '', inner, flags=re.S)
inner = re.sub(r'<defs>.*?</defs>', '', inner, flags=re.S)
inner = re.sub(r'<style>.*?</style>', '', inner, flags=re.S)
inner = inner.replace('class="ln', 'pathLength="1" class="ln')


def spruce(x, base, h, w, plane):
    tiers = 5 if h > 45 else 4 if h > 26 else 3
    top = base - h
    tier_h = (h * 0.97) / tiers
    fills, outline = [], []
    for i in range(tiers):
        ty = top + i * tier_h * 0.78
        by = ty + tier_h * 1.35
        half = w * (0.28 + 0.72 * (i + 1) / tiers) / 2
        fills.append(f'<polygon class="leaf sp-f" points="{x:.1f},{ty:.1f} {x-half:.1f},{by:.1f} {x+half:.1f},{by:.1f}"/>')
        outline.append(f"M{x-half:.1f},{by:.1f} L{x:.1f},{ty:.1f} L{x+half:.1f},{by:.1f}")
    d = f"M{x:.1f},{top:.1f} V{base:.1f} " + " ".join(outline)
    return (f'<g class="tree {plane}" style="transform-origin:{x:.1f}px {base:.1f}px">' + ''.join(fills)
            + f'<path pathLength="1" class="fl" d="{d}"/></g>')


def beech(x, base, h, r, plane):
    cy = base - h + r
    blobs = [(x, cy, r), (x - r*.62, cy + r*.35, r*.72), (x + r*.64, cy + r*.3, r*.75), (x + r*.1, cy - r*.45, r*.7)]
    d = (f"M{x:.1f},{base:.1f} V{cy+r*.3:.1f} M{x:.1f},{cy+r*.75:.1f} L{x-r*.45:.1f},{cy+r*.2:.1f} "
         f"M{x:.1f},{cy+r*.55:.1f} L{x+r*.5:.1f},{cy+r*.05:.1f}")
    return (f'<g class="tree {plane}" style="transform-origin:{x:.1f}px {base:.1f}px">'
            + ''.join(f'<circle class="leaf bk-f" cx="{a:.1f}" cy="{b:.1f}" r="{c:.1f}"/>' for a, b, c in blobs)
            + f'<path pathLength="1" class="fl" d="{d}"/>'
            + f'<circle pathLength="1" class="fl" cx="{x:.1f}" cy="{cy:.1f}" r="{r:.1f}"/></g>')


def row(rng, x0, x1, base, hmin, hmax, step, plane, avoid=(), beech_p=.18, jitter=4):
    out, x = [], x0
    while x < x1:
        xx = x + rng.uniform(-step * .3, step * .3)
        if not any(a <= xx <= b for a, b in avoid):
            bb = base + rng.uniform(-jitter, jitter)
            h = rng.uniform(hmin, hmax)
            if rng.random() < beech_p:
                out.append(beech(xx, bb, h * .7, h * .19, plane))
            else:
                out.append(spruce(xx, bb, h, h * rng.uniform(.36, .44), plane))
        x += step * rng.uniform(.75, 1.15)
    return out


def grass(rng, x0, x1, base, n):
    out = []
    for i in range(n):
        x = x0 + (x1 - x0) * i / n + rng.uniform(-1.5, 1.5)
        hh, lean = rng.uniform(3, 7), rng.uniform(-2, 2)
        out.append(f'<path pathLength="1" class="gr" d="M{x:.1f},{base:.1f} q{lean:.1f},{-hh*.6:.1f} {lean*1.6:.1f},{-hh:.1f}"/>')
    return out


SIL = ("M108.5,47.5 L118.5,59 V89.5 L146.4,121.1 L177,101 V61 H181.5 L196,14 L211,61 H215.5 V101.5 "
       "L256,124 H217 V202 L186,195 H160 L157,190 H153.5 V204 H152 V216 L94,240 H74 V204 H70.5 V190 H67 "
       "L64.5,195 H39 L28,182 L98.5,91 V59 Z")

def scene(kind):
    rng = random.Random(5)
    vb = "-62 -6 466 256"
    ridge = "M-60,150 C-30,132 -5,124 20,112 S70,96 95,104 S150,84 190,92 S260,80 300,94 S360,104 402,90"
    far, back = [], []
    x = -58
    while x < 404:   # dalszy plan: jaśniejszy
        h = rng.uniform(88, 128)
        if 208 < x < 338: h = rng.uniform(34, 44)   # pod napisem tylko niskie
        if rng.random() < .22: far.append(beech(x, 244, h*.7, h*.19, 'far'))
        else: far.append(spruce(x, 244, h, h*rng.uniform(.36,.42), 'far'))
        x += rng.uniform(34, 46)
    for x, h, b in [(-44,150,0),(-10,172,0),(22,118,1),(58,160,0),(132,168,0),(168,150,0),(244,42,0),(296,38,1),(356,176,0),(386,138,0),(404,160,0)]:
        x += rng.uniform(-4, 4)
        back.append(beech(x, 245, h*.72, h*.2, 'near') if b else spruce(x, 245, h, h*rng.uniform(.36,.42), 'near'))
    g = grass(rng, -60, 402, 244, 70)
    return (f'<svg class="scene" data-kind="h" viewBox="{vb}" role="img" '
            f'aria-label="Logo Parafii Ewangelicko-Augsburskiej Brenna-Górki na tle beskidzkiego lasu">'
            f'<path class="ridge-fill" d="{ridge} V244 H-60 Z"/><path pathLength="1" class="rd" d="{ridge}"/>'
            f'<g class="forest">{"".join(far)}{"".join(back)}</g>'
            f'<defs><filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="7"/></filter></defs>'
            f'<path class="sil" d="{SIL}"/>'
            f'<g class="logo">{inner}</g>'
            f'<g class="grass">{"".join(g)}</g><path class="ground" d="M-60,244 H402"/></svg>')


css_logo = re.search(r'<style>(.*?)</style>', logo, re.S).group(1)

html = f'''<!doctype html><html lang="pl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Brenna-Górki – logo i las</title>
<style>{css_logo}
:root{{--paper:#f7f5ef;--grid:#e4e0d3;--ink:#1d1d1b;--spruce:#2f5d45;--beech:#6f9a4a;--grass:#7aa35a;--ridge:#c9d6c2}}
body[data-season="wiosna"]{{--spruce:#3d7354;--beech:#9cc95f;--grass:#a6cf6b;--ridge:#d5e4cf}}
body[data-season="lato"]{{--spruce:#2f5d45;--beech:#5f8f3e;--grass:#78a552;--ridge:#c4d5bd}}
body[data-season="jesien"]{{--spruce:#2f5a44;--beech:#d08a2e;--grass:#b3a35a;--ridge:#e2d3b5}}
body[data-season="zima"]{{--spruce:#3c5a4c;--beech:#b9b4a6;--grass:#dcdcd4;--ridge:#e9ece9}}
*{{box-sizing:border-box}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--paper);
 background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);
 background-size:20px 20px;font-family:system-ui,sans-serif;color:var(--ink)}}
.wrap{{width:min(96vw,980px);text-align:center;padding:16px}}
.scene{{width:100%;height:auto;display:none}}
body[data-layout="h"] .scene[data-kind="h"]{{display:block}}
body[data-layout="v"] .wrap{{width:min(96vw,520px)}}
body[data-layout="v"] .scene[data-kind="v"]{{display:block;max-height:82vh;margin:0 auto}}
.logo .wh,.sil{{fill:var(--paper)}}
#text path{{stroke:var(--paper);stroke-width:0;stroke-linejoin:round;paint-order:stroke}}
.ln,.fl,.rd,.gr{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .9s ease-in-out forwards}}
.fl{{fill:none;stroke:var(--ink);stroke-width:.85;stroke-linecap:round;stroke-linejoin:round}}
.far .fl{{stroke-width:.7;opacity:.55}} .near .fl{{stroke-width:1}}
.rd{{fill:none;stroke:var(--ink);stroke-width:.6;opacity:.5;animation-duration:2.6s}}
.gr{{fill:none;stroke:var(--grass);stroke-width:.8;stroke-linecap:round;animation-duration:.6s}}
.ridge-fill{{fill:var(--ridge);opacity:0;animation:fade 1.4s ease forwards 3.2s}}
#fills,#text{{opacity:0;animation:fade 1s ease forwards}}
#fills{{animation-delay:3.1s}}#text{{animation-delay:3.6s}}
.leaf{{stroke:none;transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);opacity:0;
 animation:grow .9s cubic-bezier(.3,1.4,.5,1) forwards}}
.sp-f{{fill:var(--spruce)}} .bk-f{{fill:var(--beech)}}
.far .sp-f{{fill:color-mix(in srgb,var(--spruce) 50%,var(--paper))}}
.far .bk-f{{fill:color-mix(in srgb,var(--beech) 50%,var(--paper))}}
.mid .sp-f{{fill:color-mix(in srgb,var(--spruce) 75%,var(--paper))}}
.mid .bk-f{{fill:color-mix(in srgb,var(--beech) 80%,var(--paper))}}
.near .sp-f:nth-child(even){{fill:color-mix(in srgb,var(--spruce) 88%,#000)}}
body[data-season="zima"] .sp-f:nth-child(odd){{fill:#eef0ee}}
.tree{{animation:sway 6s ease-in-out infinite alternate 6s}}
.tree:nth-child(3n){{animation-duration:7.5s}} .tree:nth-child(2n){{animation-direction:alternate-reverse}}
.ground{{stroke:var(--ink);stroke-width:1.2;fill:none}}
@keyframes draw{{to{{stroke-dashoffset:0}}}} @keyframes fade{{to{{opacity:1}}}}
@keyframes grow{{to{{transform:scaleY(1);opacity:1}}}}
@keyframes sway{{from{{transform:rotate(-.7deg)}}to{{transform:rotate(.7deg)}}}}
@media (prefers-reduced-motion:reduce){{.ln,.fl,.rd,.gr{{animation:none;stroke-dashoffset:0}}
 #fills,#text,.ridge-fill{{animation:none;opacity:1}} .leaf{{animation:none;transform:none;opacity:1}} .tree{{animation:none}}}}
.bar{{margin-top:14px;display:flex;gap:8px;justify-content:center;flex-wrap:wrap}}
.bar span{{width:12px}}
button{{font:inherit;font-size:14px;padding:7px 14px;border:1px solid var(--ink);background:transparent;color:var(--ink);border-radius:4px;cursor:pointer}}
button[aria-pressed="true"]{{background:var(--ink);color:var(--paper)}}
</style></head>
<body data-season="jesien" data-layout="h"><div class="wrap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><pattern id="hatch" width="2.2" height="20" patternUnits="userSpaceOnUse"><rect width="0.6" height="20" fill="#1d1d1b"/></pattern></defs></svg>
<div id="stage">{scene('h')}</div>
<div class="bar">
 <button data-s="wiosna">Wiosna</button><button data-s="lato">Lato</button>
 <button data-s="jesien">Jesień</button><button data-s="zima">Zima</button><span></span>
 <button id="again">Rysuj ponownie</button>
</div></div>
<script>
const body=document.body,stage=document.getElementById('stage'),tpl=stage.innerHTML;
const mo=new Date().getMonth();
function setS(s){{body.dataset.season=s;document.querySelectorAll('[data-s]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===s))}}
function setL(l){{body.dataset.layout=l;document.querySelectorAll('[data-l]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.l===l));replay()}}
function stagger(){{
 document.querySelectorAll('.scene').forEach(sc=>{{
  sc.querySelectorAll('.logo .ln').forEach((p,i)=>p.style.animationDelay=(i*.11)+'s');
  sc.querySelectorAll('.tree').forEach((t,i)=>{{
   const plane=t.classList.contains('far')?0:t.classList.contains('mid')?1:2;
   const d=3.2+plane*.4+(i%12)*.12;
   t.querySelectorAll('.fl').forEach(p=>p.style.animationDelay=d+'s');
   t.querySelectorAll('.leaf').forEach((l,j)=>l.style.animationDelay=(4.6+plane*.3+(i%12)*.06+j*.06)+'s');
  }});
  sc.querySelectorAll('.gr').forEach((g,i)=>g.style.animationDelay=(4.8+(i%20)*.04)+'s');
 }});
}}
function replay(){{stage.innerHTML=tpl;stagger()}}
setS(mo<2||mo==11?'zima':mo<5?'wiosna':mo<8?'lato':'jesien');
replay();
document.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>setS(b.dataset.s));

document.getElementById('again').onclick=replay;
</script></body></html>'''
open('logo-las.html', 'w').write(html)
print('ok', len(html) // 1024, 'KB')
