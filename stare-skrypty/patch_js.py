s=open('header2_js.txt').read()
R=[("const sceneW=Math.min(mobile?W*.98:W*.46, 860, (H*.94)*VB.w/VB.h);","const sceneW=Math.min(mobile?W*.98:W*.46, 860, (H*.88)*VB.w/VB.h);"),
("const sx=W*.86,sy=H*.24,sr=22*k;","const sx=W*(mobile?.85:.8),sy=H*.2,sr=20*k;"),
("""let lx0=W*(mobile?.66:.74),lx1=W*(mobile?.95:.94);
 if(yb(lx0)<yb(lx1))[lx0,lx1]=[lx1,lx0];""",
"""const span=W*(mobile?.28:.2),a0=(W+sceneW)/2+10,a1=W-span-10;let lx0=a0,lx1=a0+span,best=-1;
 for(let x=a0;x<=Math.max(a0,a1);x+=8){const d=Math.abs(yb(x)-yb(x+span));if(d>best){best=d;lx0=x;lx1=x+span}}
 if(yb(lx0)<yb(lx1))[lx0,lx1]=[lx1,lx0];const kl=k*1.5;"""),
("const ph=14*k;","const ph=16*kl;"),
("lift.appendChild(el('line',{class:'pylon',x1:x-3*k,y1:y-ph,x2:x+3*k,y2:y-ph}))});","lift.appendChild(el('line',{class:'pylon',x1:x-3.5*kl,y1:y-ph,x2:x+3.5*kl,y2:y-ph}))});"),
("lift.appendChild(el('polyline',{class:'cable',points:top.map(([x,y])=>`${x+dx*k},${y}`).join(' ')}))});","lift.appendChild(el('polyline',{class:'cable',points:top.map(([x,y])=>`${x+dx*kl},${y}`).join(' ')}))});"),
("lift.appendChild(el('rect',{class:'station',x:x-6*k*s,y:y-9*k*s,width:12*k*s,height:9*k*s})));","lift.appendChild(el('path',{class:'station',d:`M${x-7*kl*s},${y} v${-8*kl*s} l${7*kl*s},${-5*kl*s} l${7*kl*s},${5*kl*s} v${8*kl*s} Z`})));"),
("c.appendChild(el('line',{x1:0,y1:0,x2:0,y2:5*k}));c.appendChild(el('path',{d:`M${-2.4*k},${5*k} h${4.8*k} v${2.2*k}`}));","c.appendChild(el('line',{x1:0,y1:0,x2:0,y2:6*kl}));c.appendChild(el('path',{d:`M${-3*kl},${6*kl} h${6*kl} v${2.6*kl} M${-3*kl},${6*kl} v${-2.6*kl}`}));"),
("for(let i=0;i<10;i++){const c=el('g',{class:'chair'});","for(let i=0;i<8;i++){const c=el('g',{class:'chair'});"),
("cg.appendChild(c);chairs.push({el:c,t:i/10})}","cg.appendChild(c);chairs.push({el:c,t:i/8})}"),
("dx=(up?-2:2)*Math.min(1,hero.clientHeight/380);","dx=(up?-2:2)*1.5*Math.max(.55,Math.min(1,hero.clientHeight/380));"),
("if(rnd()<.22){const fh=(6+rnd()*7)*k,fx=x+l;","if(rnd()<.4){const fh=(9+rnd()*9)*k,fx=x+l;"),
("""fl.appendChild(el('path',{class:'bloom',d:`M${(fx-2.2*k).toFixed(1)},${(groundY-fh).toFixed(1)} q${(.4*k).toFixed(1)},${(-3.6*k).toFixed(1)} ${(2.2*k).toFixed(1)},${(-3.2*k).toFixed(1)} q${(1.8*k).toFixed(1)},${(-.4*k).toFixed(1)} ${(2.2*k).toFixed(1)},${(3.2*k).toFixed(1)} Z`}))}}""",
"""const b=3.4*k,by=groundY-fh;
   fl.appendChild(el('path',{class:'bloom',d:`M${(fx-b).toFixed(1)},${(by-b*1.6).toFixed(1)} L${(fx-b*.45).toFixed(1)},${(by-b*.9).toFixed(1)} L${fx.toFixed(1)},${(by-b*1.7).toFixed(1)} L${(fx+b*.45).toFixed(1)},${(by-b*.9).toFixed(1)} L${(fx+b).toFixed(1)},${(by-b*1.6).toFixed(1)} Q${(fx+b).toFixed(1)},${by.toFixed(1)} ${fx.toFixed(1)},${by.toFixed(1)} Q${(fx-b).toFixed(1)},${by.toFixed(1)} ${(fx-b).toFixed(1)},${(by-b*1.6).toFixed(1)} Z`}))}}"""),
]
for a,b in R:
    assert a in s,a[:60]; s=s.replace(a,b)
open('header2_js.txt','w').write(s)
print('patched')
