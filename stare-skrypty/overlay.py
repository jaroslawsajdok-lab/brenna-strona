import sys, cairosvg, io
from PIL import Image, ImageOps
import re
svg=re.sub(r"viewBox=\"[^\"]*\" width=\"\d+\" height=\"\d+\"","viewBox=\"0 0 340 240\"",open(sys.argv[1]).read(),count=1)
S=4
png=cairosvg.svg2png(bytestring=svg.encode(),output_width=340*S,output_height=240*S)
mine=Image.open(io.BytesIO(png)).convert('RGBA')
bg=Image.new('RGBA',mine.size,'white');bg.alpha_composite(mine);mine=bg.convert('L')
orig=Image.open('/mnt/user-data/uploads/1791621466493_image.png').convert('L').resize(mine.size,Image.LANCZOS)
# orig in light gray-blue, mine in red
o=ImageOps.invert(orig); m=ImageOps.invert(mine)
r=Image.merge('RGB',(Image.eval(o,lambda v:255-int(v*0.15)).point(lambda v:v), Image.eval(o,lambda v:255-int(v*0.55)), Image.eval(o,lambda v:255-int(v*0.25))))
red=Image.new('RGB',mine.size,(220,0,0))
out=Image.composite(red,r,m.point(lambda v:min(255,int(v*0.85))))
out.save(sys.argv[2])
mine.save(sys.argv[2].replace('.png','_mine.png'))
