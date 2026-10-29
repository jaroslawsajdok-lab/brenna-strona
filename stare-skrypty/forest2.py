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
    tier_h = (h * 0.86) / tiers
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


def scene(kind):
    rng = random.Random(11 if kind == 'h' else 23)
    if kind == 'h':
        vb = "-62 -6 466 256"
        ridge = "M-60,168 C-30,150 -5,140 20,126 S70,110 95,118 S150,96 190,104 S260,92 300,106 S360,116 402,102"
        ridge_bottom = 244
        mask = (".09", ".2", ".84", ".93")
        back = (row(rng, -58, 30, 214, 30, 46, 11, 'far') + row(rng, 300, 404, 214, 30, 48, 11, 'far'))
        mid = (row(rng, -56, 40, 228, 40, 62, 14, 'mid') + row(rng, 312, 404, 228, 40, 64, 14, 'mid')
               + row(rng, 226, 300, 224, 18, 26, 10, 'mid', beech_p=0))
        near = (row(rng, -60, 50, 244, 52, 84, 19, 'near', avoid=[(32, 50)])
                + row(rng, 160, 220, 244, 22, 34, 13, 'near', beech_p=.3)
                + row(rng, 300, 404, 244, 52, 84, 19, 'near'))
        g = grass(rng, -60, 402, 244, 80)
        ground = "M-60,244 H402"
    else:
        vb = "6 -10 338 368"
        ridge = "M6,214 C40,200 70,206 100,200 S170,186 210,194 S290,200 344,188"
        ridge_bottom = 352
        mask = ("0", "0", "1", "1")  # bez wygaszania – grzbiet jest pod logo
        back = row(rng, 8, 344, 252, 24, 40, 9, 'far', avoid=[(76, 150)], beech_p=.12, jitter=3)
        mid = row(rng, 4, 346, 300, 36, 56, 13, 'mid', beech_p=.18)
        near = row(rng, -2, 352, 352, 54, 82, 21, 'near', beech_p=.2)
        g = grass(rng, 6, 344, 352, 70)
        ground = "M6,352 H344"
    m0, m1, m2, m3 = mask
    defs = (f'<defs><linearGradient id="fx-{kind}" x1="-60" x2="400" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="#fff"/><stop offset="{m0}" stop-color="#fff"/><stop offset="{m1}" stop-color="#000"/>'
            f'<stop offset="{m2}" stop-color="#000"/><stop offset="{m3}" stop-color="#fff"/><stop offset="1" stop-color="#fff"/></linearGradient>'
            f'<mask id="m-{kind}" maskUnits="userSpaceOnUse" x="-70" y="-20" width="480" height="420"><rect x="-70" y="-20" width="480" height="420" fill="url(#fx-{kind})"/></mask></defs>')
    if kind == 'v':
        defs = defs.replace(f'fill="url(#fx-{kind})"', 'fill="#fff"')
    logo_k = inner
    # w pionie dalszy plan za logo jest niżej niż słup – rysujemy go PRZED logo; reszta przed nim
    return (f'<svg class="scene" data-kind="{kind}" viewBox="{vb}" role="img" '
            f'aria-label="Logo Parafii Ewangelicko-Augsburskiej Brenna-Górki na tle beskidzkiego lasu">{defs}'
            f'<g mask="url(#m-{kind})"><path class="ridge-fill" d="{ridge} V{ridge_bottom} H-60 Z"/>'
            f'<path pathLength="1" class="rd" d="{ridge}"/></g>'
            f'<g class="forest">{"".join(back)}</g>'
            f'<g class="logo">{logo_k}</g>'
            f'<g class="forest">{"".join(mid)}{"".join(near)}</g>'
            f'<g class="grass">{"".join(g)}</g><path class="ground" d="{ground}"/></svg>')


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
.logo .wh{{fill:var(--paper)}}
.ln,.fl,.rd,.gr{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw .9s ease-in-out forwards}}
.fl{{fill:none;stroke:var(--ink);stroke-width:.85;stroke-linecap:round;stroke-linejoin:round}}
.far .fl{{stroke-width:.6;opacity:.6}}
.rd{{fill:none;stroke:var(--ink);stroke-width:.6;opacity:.5;animation-duration:2.6s}}
.gr{{fill:none;stroke:var(--grass);stroke-width:.8;stroke-linecap:round;animation-duration:.6s}}
.ridge-fill{{fill:var(--ridge);opacity:0;animation:fade 1.4s ease forwards 3.2s}}
#fills,#text{{opacity:0;animation:fade 1s ease forwards}}
#fills{{animation-delay:3.1s}}#text{{animation-delay:3.6s}}
.leaf{{stroke:none;transform-box:fill-box;transform-origin:50% 100%;transform:scaleY(0);opacity:0;
 animation:grow .9s cubic-bezier(.3,1.4,.5,1) forwards}}
.sp-f{{fill:var(--spruce)}} .bk-f{{fill:var(--beech)}}
.far .sp-f{{fill:color-mix(in srgb,var(--spruce) 45%,var(--paper))}}
.far .bk-f{{fill:color-mix(in srgb,var(--beech) 50%,var(--paper))}}
.mid .sp-f{{fill:color-mix(in srgb,var(--spruce) 75%,var(--paper))}}
.mid .bk-f{{fill:color-mix(in srgb,var(--beech) 80%,var(--paper))}}
.near .sp-f:nth-child(even){{fill:color-mix(in srgb,var(--spruce) 85%,#000)}}
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
<body data-season="jesien" data-layout="v"><div class="wrap">
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><pattern id="hatch" width="2.2" height="20" patternUnits="userSpaceOnUse"><rect width="0.6" height="20" fill="#1d1d1b"/></pattern></defs></svg>
<div id="stage">{scene('h')}{scene('v')}</div>
<div class="bar">
 <button data-l="v">Pionowo</button><button data-l="h">Poziomo</button><span></span>
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
   const d=1.2+plane*.5+(i%14)*.1;
   t.querySelectorAll('.fl').forEach(p=>p.style.animationDelay=d+'s');
   t.querySelectorAll('.leaf').forEach((l,j)=>l.style.animationDelay=(3.9+plane*.35+(i%14)*.05+j*.06)+'s');
  }});
  sc.querySelectorAll('.gr').forEach((g,i)=>g.style.animationDelay=(4.8+(i%20)*.04)+'s');
 }});
}}
function replay(){{stage.innerHTML=tpl;stagger()}}
setS(mo<2||mo==11?'zima':mo<5?'wiosna':mo<8?'lato':'jesien');
setL(matchMedia('(min-aspect-ratio: 1/1)').matches?'h':'v');
document.querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>setS(b.dataset.s));
document.querySelectorAll('[data-l]').forEach(b=>b.onclick=()=>setL(b.dataset.l));
document.getElementById('again').onclick=replay;
</script></body></html>'''
open('logo-las.html', 'w').write(html)
print('ok', len(html) // 1024, 'KB')
