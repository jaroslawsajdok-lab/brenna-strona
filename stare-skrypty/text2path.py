from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen
f=TTFont('font/pts/package/files/pt-sans-latin-400-normal.woff')
gs=f.getGlyphSet();cmap=f.getBestCmap();upm=f['head'].unitsPerEm
capH=f['OS/2'].sCapHeight
lines=[("PARAFIA",222,141.5,52.5),("EWANGELICKO-",222,156,93.5),("AUGSBURSKA",222.5,170.5,88.5),("BRENNA-",222,184.5,56.5),("GÓRKI",222,198.5,39.5)]
cap=9.6; s=cap/capH  # scale so cap height = 9px
out=[]
for txt,x,y,w in lines:
    adv=0;parts=[]
    for ch in txt:
        g=cmap[ord(ch)];pen=SVGPathPen(gs);gs[g].draw(pen)
        parts.append((adv,pen.getCommands()));adv+=gs[g].width
    # ink width: subtract right sidebearing of last glyph roughly
    bp=BoundsPen(gs);gs[cmap[ord(txt[-1])]].draw(bp)
    ink=adv-gs[cmap[ord(txt[-1])]].width+bp.bounds[2]
    bp=BoundsPen(gs);gs[cmap[ord(txt[0])]].draw(bp);lsb=bp.bounds[0]
    sx=w/((ink-lsb)*s)
    g='<g transform="translate(%.2f %.2f) scale(%.4f %.4f) translate(%.1f 0)">'%(x,y,s*sx,-s,-lsb)
    g+=''.join('<path transform="translate(%d 0)" d="%s"/>'%(a,d) for a,d in parts)+'</g>'
    out.append((txt,sx,g))
for t,sx,_ in out: print(t,round(sx,3))
open('text_paths.txt','w').write('\n    '.join(g for _,_,g in out))
