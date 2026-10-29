"""Drzwi do kościoła narysowane kreską jak logo: obramienie z kamiennych klinów + dwa skrzydła z deskami,
okuciami i Różą Lutra. Wynik: door_frame.svg, door_leaf_l.svg, door_leaf_r.svg (fragmenty do wklejenia)."""
import math
C=500; RI=433; RO=492
INK='#1d1d1b'

def P(d,cls='dl',extra=''):return f'<path class="{cls}" pathLength="1" d="{d}" {extra}/>'
def circ(cx,cy,r,cls='dl',extra=''):return f'<circle class="{cls}" pathLength="1" cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" {extra}/>'

# ---------- obramienie: łuk z klinów (jak rysunek architektoniczny) ----------
def frame():
    out=[f'<path class="df stone" d="M{C-RO},{C} a{RO},{RO} 0 1,0 {2*RO},0 a{RO},{RO} 0 1,0 {-2*RO},0 Z M{C-RI},{C} a{RI},{RI} 0 1,1 {2*RI},0 a{RI},{RI} 0 1,1 {-2*RI},0 Z" fill-rule="evenodd"/>']
    n=28
    for i in range(n):
        a0=(i/n)*2*math.pi-math.pi/2;a1=((i+1)/n)*2*math.pi-math.pi/2
        if True:     # kliny drewniane, na przemian jaśniejsze i ciemniejsze
            pts=[(C+RI*math.cos(a0),C+RI*math.sin(a0)),(C+RO*math.cos(a0),C+RO*math.sin(a0)),(C+RO*math.cos(a1),C+RO*math.sin(a1)),(C+RI*math.cos(a1),C+RI*math.sin(a1))]
            out.append(f'<path class="df {"fw1" if i%2 else "fw2"}" d="M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+'Z"/>')
    for i in range(n):
        a=(i/n)*2*math.pi-math.pi/2
        out.append(P(f'M{C+RI*math.cos(a):.1f},{C+RI*math.sin(a):.1f} L{C+RO*math.cos(a):.1f},{C+RO*math.sin(a):.1f}','dl thin'))
    out.append(circ(C,C,RO,'dl bold'));out.append(circ(C,C,RI,'dl bold'));out.append(circ(C,C,RI+9,'dl thin'))
    # zwornik u góry
    k=f'M{C-24},{C-RO-10} L{C+24},{C-RO-10} L{C+17},{C-RI+4} L{C-17},{C-RI+4} Z'
    out.append(f'<path class="df key" d="{k}"/>'+P(k,'dl bold'))
    return ''.join(out)

# ---------- skrzydło (całe drzwi rysowane raz, przycinane do połówki) ----------
def door():
    o=[]
    clipc=f'M{C-RI},{C} a{RI},{RI} 0 1,0 {2*RI},0 a{RI},{RI} 0 1,0 {-2*RI},0 Z'
    o.append(f'<path class="df wood" d="{clipc}"/>')
    xs=list(range(C-RI,C+RI+62,62))
    for k,x in enumerate(xs[:-1]):
        o.append(f'<rect class="df plank{k%3}" x="{x}" y="0" width="62" height="1000"/>')
    # deski: pionowe linie przycięte do koła
    for x in xs[1:-1]:
        if abs(x-C)<4: continue
        h=math.sqrt(max(0,RI*RI-(x-C)**2))
        o.append(P(f'M{x},{C-h+2:.1f} V{C+h-2:.1f}','dl plank'))
    # słoje drewna: krótkie, rzadkie kreski
    import random;rnd=random.Random(4)
    for _ in range(70):
        x=rnd.uniform(C-RI+30,C+RI-30);y=rnd.uniform(C-RI+40,C+RI-40)
        if (x-C)**2+(y-C)**2>(RI-30)**2 or (x-C)**2+(y-C)**2<185**2: continue
        L=rnd.uniform(18,46);o.append(P(f'M{x:.1f},{y:.1f} q2,{L/2:.1f} 0,{L:.1f}','dl grain'))
    # pas obwodowy
    o.append(circ(C,C,RI-22,'dl thin'))
    # okucia: pasy zawiasów od strony zawiasu, zakończone krzyżem
    for y in (C-200,C+200):
        for side in (-1,1):
            x0=C+side*(RI*math.cos(math.asin((y-C)/RI))-6); x1=C+side*205
            a,b=min(x0,x1),max(x0,x1)
            strap=f'M{a:.1f},{y-13} L{b:.1f},{y-13} L{b:.1f},{y+13} L{a:.1f},{y+13} Z'
            tip=x1; s=-side
            cross=(f'M{tip:.1f},{y-13} l{s*0:.1f},0 l{-s*0:.1f},0 '
                   f'M{tip:.1f},{y-30} l{s*-14:.1f},12 l0,10 l{s*-10:.1f},0 l0,-0 ')
            o.append(f'<path class="df iron" d="{strap}"/>')
            # krzyżowe zakończenie (trójlistne)
            for dy in (-34,0,34):
                cx=tip+s*(28 if dy==0 else 6);cy=y+dy*(0.75 if dy else 0)
                o.append(f'<circle class="df iron" cx="{cx:.1f}" cy="{cy:.1f}" r="12"/>')
            o.append(f'<path class="df iron" d="M{tip:.1f},{y-30} L{tip+s*10:.1f},{y} L{tip:.1f},{y+30} L{tip-s*6:.1f},{y} Z"/>')
            for k in range(4):
                rx=x0+(x1-x0)*(k+.6)/4.6;o.append(f'<circle class="rivet light" cx="{rx:.1f}" cy="{y}" r="4.2"/>')
    # nity na obwodzie
    for i in range(36):
        a=i/36*2*math.pi
        if abs(math.sin(a))<.05: continue
        o.append(f'<circle class="rivet" cx="{C+(RI-40)*math.cos(a):.1f}" cy="{C+(RI-40)*math.sin(a):.1f}" r="5"/>')
    # medalion z Różą Lutra: złoty pierścień, zielone pole, biała róża, czerwone serce, czarny krzyż
    o.append(f'<circle class="df field" cx="{C}" cy="{C}" r="172"/>')
    petal="M-16,-46 C-62,-58 -84,-112 -50,-140 C-34,-152 -12,-150 0,-136 C12,-150 34,-152 50,-140 C84,-112 62,-58 16,-46 Z"
    for i in range(5):
        o.append(f'<path class="df petal" d="{petal}" transform="translate({C} {C}) rotate({i*72})"/>')
    for i in range(5):
        o.append(f'<path class="dl" pathLength="1" d="{petal}" transform="translate({C} {C}) rotate({i*72})"/>')
        o.append(f'<path class="dl thin" pathLength="1" d="M0,-58 Q-4,-96 0,-128 M-18,-60 Q-34,-92 -40,-120 M18,-60 Q34,-92 40,-120" transform="translate({C} {C}) rotate({i*72})"/>')
    # serce
    heart=f'M{C},{C+70} C{C-26},{C+50} {C-74},{C+20} {C-74},{C-20} C{C-74},{C-54} {C-44},{C-70} {C-20},{C-66} C{C-8},{C-64} {C},{C-54} {C},{C-46} C{C},{C-54} {C+8},{C-64} {C+20},{C-66} C{C+44},{C-70} {C+74},{C-54} {C+74},{C-20} C{C+74},{C+20} {C+26},{C+50} {C},{C+70} Z'
    o.append(f'<path class="df heart" d="{heart}"/>'+P(heart,'dl bold'))
    cr=f'M{C-6},{C-46} H{C+6} V{C-22} H{C+30} V{C-10} H{C+6} V{C+36} H{C-6} V{C-10} H{C-30} V{C-22} H{C-6} Z'
    o.append(f'<path class="df crossf" d="{cr}"/>')
    o.append(f'<circle class="dl gold" pathLength="1" cx="{C}" cy="{C}" r="172"/>')
    o.append(circ(C,C,180,'dl thin'))
    # kołatki
    for side in (-1,1):
        x=C+side*62;y=C+250
        o.append(f'<path class="df iron" d="M{x-9:.1f},{y-30} L{x+9:.1f},{y-30} L{x+5:.1f},{y-12} L{x-5:.1f},{y-12} Z"/>')
        o.append(circ(x,y+6,24,'dl iron-ring'))
    # szczelina między skrzydłami
    o.append(P(f'M{C},{C-RI} V{C+RI}','dl bold'))
    return clipc,''.join(o)

clipc,body=door()
def leaf(side):
    vb='0 0 500 1000' if side=='l' else '500 0 500 1000'
    half=f'<rect x="{0 if side=="l" else C}" y="0" width="{C}" height="1000"/>'
    return (f'<svg class="dleaf {side}" viewBox="{vb}" aria-hidden="true"><defs><clipPath id="dc{side}"><path d="{clipc}"/></clipPath>'
            f'<clipPath id="dh{side}">{half}</clipPath></defs><g clip-path="url(#dh{side})"><g clip-path="url(#dc{side})">{body}</g></g></svg>')
fr=f'<svg class="dframe" viewBox="0 0 1000 1000" aria-hidden="true"><defs><pattern id="dhatch" width="7" height="20" patternUnits="userSpaceOnUse" patternTransform="rotate(-35)"><rect width="1.6" height="20" fill="{INK}"/></pattern></defs>{frame()}</svg>'
open('door_parts.html','w').write(fr+'\n<div class="doors">'+leaf('l')+leaf('r')+'</div>')
print('ok',len(fr)+len(body)*2)
