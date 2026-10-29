s=open('header2_js.txt').read()
i=s.index(" // liście (jesień) – spadają po całej szerokości"); j=s.index(" front.appendChild(lv);\n")+len(" front.appendChild(lv);\n")
s=s[:i]+""" // liście (jesień): warstwa na spadające i leżące; stan przeżywa zmianę rozmiaru okna
 const lv=el('g',{class:'deco only-jesien'});leafFall=el('g');leafPile=el('g');lv.appendChild(leafPile);lv.appendChild(leafFall);front.appendChild(lv);
 G={W,H,groundY,k,mobile,sc0,sc1};
 const nb=Math.ceil(W/BIN)+2;if(!heights||heights.length!==nb){heights=new Float32Array(nb);   // przelicz kopki na nową szerokość
  settled.forEach(l=>{const b=Math.round(l.fx*W/BIN);if(b>=0&&b<nb)heights[b]=Math.max(heights[b],l.h)})}
 if(!centers.length){for(let c=0;c<(mobile?3:7);c++)centers.push(.04+.92*rnd())}
 settled.forEach(l=>leafPile.appendChild(leafEl(l.fx*W,groundY-l.h,l.rot,l.c,l.s*k)));
 falling.forEach(f=>{f.node=leafEl(0,0,0,f.c,f.s*k);leafFall.appendChild(f.node)});
"""+s[j:]

# globals
s=s.replace("let first=true,chairs=[],liftPath=null,raf=0;","""let first=true,chairs=[],liftPath=null,raf=0;
// --- symulacja liści ---
const BIN=4;let G=null,heights=null,settled=[],falling=[],centers=[],leafFall=null,leafPile=null,spawnAcc=0;
const LEAFC=['#d08a2e','#b5562a','#e0a440','#9c4a22','#c9772a'];
function leafEl(x,y,rot,c,q){const p=el('path',{class:'lf',fill:c,
 d:`M0,${-5*q} C${4*q},${-3*q} ${4*q},${3*q} 0,${5*q} C${-4*q},${3*q} ${-4*q},${-3*q} 0,${-5*q} Z M0,${-5*q} V${6.5*q}`,
 transform:`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${rot.toFixed(0)})`});return p}
function stepLeaves(dt){
 if(!G||document.body.dataset.season!=='jesien')return;
 const {W,H,groundY,k,mobile}=G, maxH=H*.12;
 // nowe liście: ok. 1 na 0,6 s (telefon rzadziej)
 spawnAcc+=dt*(mobile?1:1.7);
 while(spawnAcc>1&&falling.length<(mobile?10:22)){spawnAcc-=1;
  const f={x:Math.random()*W,y:-12,vy:(18+Math.random()*16)*Math.max(.7,k),ph:Math.random()*6.3,sw:(10+Math.random()*16),rot:Math.random()*360,vr:(Math.random()-.5)*160,
   c:LEAFC[(Math.random()*LEAFC.length)|0],s:.8+Math.random()*.5};
  f.node=leafEl(f.x,f.y,f.rot,f.c,f.s*k);leafFall.appendChild(f.node);falling.push(f)}
 if(spawnAcc>1)spawnAcc=1;
 for(let i=falling.length-1;i>=0;i--){const f=falling[i];
  f.y+=f.vy*dt;f.ph+=dt*1.6;f.rot+=f.vr*dt;const x=f.x+Math.sin(f.ph)*f.sw;
  const b=Math.max(0,Math.min(heights.length-1,Math.round(x/BIN)));
  if(f.y>=groundY-heights[b]-2){                   // lądowanie
   // zsuwa się w stronę najbliższej kopki
   let cx=centers.reduce((a,c)=>Math.abs(c*W-x)<Math.abs(a-x)?c*W:a,Infinity);
   let nx=x+(cx-x)*(.25+Math.random()*.6);
   let bb=Math.max(1,Math.min(heights.length-2,Math.round(nx/BIN)));
   for(let n=0;n<40;n++){const l=heights[bb-1],r=heights[bb+1],h=heights[bb],lim=2.4*k;   // kąt usypu
    if(h>l+lim&&(l<=r||h<=r+lim)&&bb>1)bb--;else if(h>r+lim&&bb<heights.length-2)bb++;else break}
   if(heights[bb]<maxH){
    const hh=heights[bb];heights[bb]+=1.1*k*f.s;heights[bb-1]+=.35*k;heights[bb+1]+=.35*k;
    const L={fx:bb*BIN/W,h:hh+1.5*k,rot:(Math.random()-.5)*150,c:f.c,s:f.s};
    settled.push(L);leafPile.appendChild(leafEl(bb*BIN,groundY-L.h,L.rot,L.c,L.s*k));
    if(settled.length>1400){settled.shift();leafPile.firstChild&&leafPile.firstChild.remove()}
   }
   f.node.remove();falling.splice(i,1);continue}
  f.node.setAttribute('transform',`translate(${x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`)}
}""")
# sc0/sc1 must exist before use: they are defined in row-tree block above (const sc0...) -> ok since leaves block comes later
# hook into tick
s=s.replace("function tick(ts){","function tick(ts){\n stepLeaves(last?Math.min(.05,(ts-last)/1000):0);")
open('header2_js.txt','w').write(s)
print('ok')
