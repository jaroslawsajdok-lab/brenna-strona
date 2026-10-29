import re, random
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
src = open('forest3.py').read()
# reuse helpers (spruce, beech, grass, SIL, logo inner, css) from forest3 without running its output
ns = {}
exec(src.split("css_logo =")[0], ns)
css_logo = re.search(r'<style>(.*?)</style>', open('logo.svg').read(), re.S).group(1)
f = TTFont('font/pts/package/files/pt-sans-latin-400-normal.woff'); gs = f.getGlyphSet(); cmap = f.getBestCmap()

def line(txt, cx, base, width, track=0):
    parts, adv = [], 0
    for ch in txt:
        g = cmap[ord(ch)]; pen = SVGPathPen(gs); gs[g].draw(pen)
        parts.append((adv, pen.getCommands())); adv += gs[g].width + track
    adv -= track
    s = width / adv
    x0 = cx - width / 2
    return (f'<g transform="translate({x0:.2f} {base:.2f}) scale({s:.5f} {-s:.5f})">'
            + ''.join(f'<path transform="translate({a} 0)" d="{d}"/>' for a, d in parts if d) + '</g>')

inner = re.sub(r'<g id="text".*?</g>\s*</g>', '', ns['inner'], flags=re.S)  # bez bocznego napisu
assert 'id="text"' not in inner
CX = 142
text = ('<g id="text" fill="#1d1d1b">' + line('PARAFIA EWANGELICKO-AUGSBURSKA', CX, 266, 196, 60)
        + line('BRENNA-GÓRKI', CX, 296, 196, 70) + '</g>')

rng = random.Random(9)
ridge = "M-10,140 C10,124 40,112 70,104 S130,86 170,92 S230,80 260,90 S290,96 300,92"
far, back = [], []
x = -8
while x < 300:
    h = rng.uniform(86, 124)
    far.append(ns['beech'](x, 244, h*.7, h*.19, 'far') if rng.random() < .2 else ns['spruce'](x, 244, h, h*rng.uniform(.36, .42), 'far'))
    x += rng.uniform(30, 40)
for x, h, b in [(2,158,0),(30,182,0),(58,118,1),(84,150,0),(136,172,0),(172,140,0),(232,120,1),(258,176,0),(286,150,0)]:
    x += rng.uniform(-3, 3)
    back.append(ns['beech'](x, 245, h*.72, h*.2, 'near') if b else ns['spruce'](x, 245, h, h*rng.uniform(.36, .42), 'near'))
g = ns['grass'](rng, -6, 292, 244, 46)

svg = (f'<svg class="scene" viewBox="-6 -12 298 324" role="img" aria-label="Logo Parafii Ewangelicko-Augsburskiej Brenna-Górki na tle beskidzkiego lasu">'
       f'<path class="ridge-fill" d="{ridge} V244 H-10 Z"/><path pathLength="1" class="rd" d="{ridge}"/>'
       f'<g class="forest">{"".join(far)}{"".join(back)}</g>'
       f'<path class="sil" d="{ns["SIL"]}"/><g class="logo">{inner}{text}</g>'
       f'<g class="grass">{"".join(g)}</g><path class="ground" d="M-6,244 H292"/></svg>')

page = open('logo-las.html').read()
page = re.sub(r'<div id="stage">.*?</div>\n<div class="bar">', '<div id="stage">' + svg.replace('\\', '\\\\') + '</div>\n<div class="bar">', page, flags=re.S)
page = page.replace('<title>Brenna-Górki – logo i las</title>', '<title>Brenna-Górki – logo pionowe</title>')
page = page.replace('.wrap{width:min(96vw,980px)', '.wrap{width:min(96vw,520px)')
page = page.replace('.scene{width:100%;height:auto;display:none}', '.scene{width:100%;height:auto;display:block;max-height:84vh;margin:0 auto}')
open('logo-las-pion.html', 'w').write(page)
print('ok')
