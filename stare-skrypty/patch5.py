s=open('header2_js.txt').read()

# ---------- 1. liście: lecą na kupkę i zsuwają się po zboczu (bez teleportu); RNG z ziarnem ----------
i=s.index("function stepLeaves(dt){"); j=s.index("function layout(){")
s=s[:i]+r"""let lseed=12345;const lr=()=>(lseed=(lseed*16807)%2147483647)/2147483647;
let simT=0;                                    // ile sekund "żyje" jesień na stronie
function settleAt(bb,f){const {W,groundY,k,H,mobile}=G,maxH=H*(mobile?.08:.15);
 if(heights[bb]>=maxH||settled.length>=2600)return;
 const hh=heights[bb];heights[bb]+=1.3*k*f.s;heights[bb-1]+=.5*k;heights[bb+1]+=.5*k;
 const L={fx:bb*BIN/W,h:hh+1.5*k,rot:f.rot,c:f.c,s:f.s};settled.push(L);
 leafPile.appendChild(leafEl(bb*BIN,groundY-L.h,L.rot,L.c,L.s*k))}
function downhill(bb){const lim=4.6*G.k;      // kąt usypu – w którą stronę liść się stoczy
 const l=heights[bb-1],r=heights[bb+1],h=heights[bb];
 if(h>l+lim&&(l<=r||h<=r+lim)&&bb>1)return -1;if(h>r+lim&&bb<heights.length-2)return 1;return 0}
function stepLeaves(dt,fast){
 if(!G||document.body.dataset.season!=='jesien')return;
 simT+=dt;
 const {W,H,groundY,k,mobile}=G;
 spawnAcc+=dt*(mobile?1:1.7);
 while(spawnAcc>1&&falling.length<(mobile?10:22)){spawnAcc-=1;
  // liść startuje w okolicy kupki i wiatr niesie go nad nią
  const c=centers[(lr()*centers.length)|0]*W,targeted=lr()<.85;
  const tx=targeted?c+(lr()-.5)*W*.05:lr()*W, x0=tx+(lr()-.5)*W*.22;
  const f={x0,tx,x:x0,y:-12,vy:(18+lr()*16)*Math.max(.7,k),ph:lr()*6.3,sw:(8+lr()*12),rot:lr()*360,vr:(lr()-.5)*160,
   c:LEAFC[(lr()*LEAFC.length)|0],s:.8+lr()*.5,st:'air'};
  f.node=leafEl(f.x,f.y,f.rot,f.c,f.s*k);leafFall.appendChild(f.node);falling.push(f)}
 if(spawnAcc>1)spawnAcc=1;
 for(let i=falling.length-1;i>=0;i--){const f=falling[i];
  if(f.st==='air'){
   f.y+=f.vy*dt;f.ph+=dt*1.6;f.rot+=f.vr*dt;
   const prog=Math.min(1,Math.max(0,f.y/groundY)),ease=prog*prog*(3-2*prog);
   f.x=f.x0+(f.tx-f.x0)*ease+Math.sin(f.ph)*f.sw*(1-prog*.6);
   const b=Math.max(1,Math.min(heights.length-2,Math.round(f.x/BIN)));
   if(f.y>=groundY-heights[b]-1.5*k){f.st='roll';f.b=b;f.y=groundY-heights[b]-1.5*k;f.vr*=.4;f.acc=0}
  }else{                                           // toczy się po zboczu kupki aż znajdzie miejsce
   const dir=downhill(f.b);
   if(dir===0){f.rot=((f.rot%360)+360)%360;settleAt(f.b,f);f.node.remove();falling.splice(i,1);continue}
   f.acc+=dt*55*k;                                 // ok. 55 px/s
   while(f.acc>=BIN){f.acc-=BIN;f.b+=dir;if(downhill(f.b)!==dir)break}
   const tx=f.b*BIN+dir*f.acc;f.x+=(tx-f.x)*Math.min(1,dt*12);
   const ty=groundY-heights[f.b]-1.5*k;f.y+=(ty-f.y)*Math.min(1,dt*12);f.rot+=dir*240*dt}
  if(!fast)f.node.setAttribute('transform',`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`)}
}
function resetLeaves(){lseed=12345;simT=0;spawnAcc=0;settled=[];falling.forEach(f=>f.node.remove());falling=[];
 if(heights)heights.fill(0);if(leafPile)leafPile.innerHTML=''}
"""+s[j:]
# pozycja liścia w locie po przebudowie (resize)
s=s.replace("falling.forEach(f=>{f.node=leafEl(0,0,0,f.c,f.s*k);leafFall.appendChild(f.node)});",
            "falling.forEach(f=>{f.node=leafEl(f.x,f.y,f.rot,f.c,f.s*k);leafFall.appendChild(f.node)});")

# ---------- 2. zegar sceny: wspólny czas, pauza i przewijanie ----------
s=s.replace("let SKY=null,","let clockOff=0,paused=false,pausedT=0;\nconst now=()=>paused?pausedT:performance.now()/1000+clockOff;\nlet SKY=null,",1)
s=s.replace("if(!SKY)return;const season=document.body.dataset.season,t=ts/1000,","if(!SKY)return;const season=document.body.dataset.season,t=now(),")
s=s.replace(" stepLeaves(last?Math.min(.05,(ts-last)/1000):0);"," if(!paused)stepLeaves(last?Math.min(.05,(ts-last)/1000):0);")
# krzesełka wyciągu też stoją na pauzie
s=s.replace("const dt=last?(ts-last)/1000:0;","const dt=paused?0:(last?(ts-last)/1000:0);")

# ---------- 3. księżyc w pełni ----------
a=s[s.index(" moonG.appendChild(el('path',{class:'moon'"):]
a=a[:a.index("\n")+1]
s=s.replace(a,""" moonG.appendChild(el('circle',{class:'moon',r:mr}));
 [[-.32,-.22,.2],[.28,.1,.15],[-.05,.42,.12],[.18,-.42,.09],[-.45,.25,.08]].forEach(([x,y,r])=>moonG.appendChild(el('circle',{class:'crater',cx:x*mr,cy:y*mr,r:r*mr})));
""")
s=s.replace("moonG.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(-25+50*p).toFixed(1)})`);",
            "moonG.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)})`);")

# ---------- 4. czystsze kolory: trzy pasy (góra / środek / horyzont) ----------
k0=s.index("const SKYK=");k1=s.index("function arc(p)")
s=s[:k0]+r"""// [faza, góra, środek, horyzont] – sąsiednie stany są blisko siebie, więc przejścia nie brudzą się
const SKYK=[[0,'#6f7fc4','#e9a9c4','#ffc58f'],[.05,'#86a0d8','#f4c1cf','#ffdcb0'],[.12,'#9fc4e8','#d6e6f0','#f6efe2'],
 [.44,'#a8d0ec','#d4e8f3','#eef5f4'],[.7,'#9fc4e8','#d9e6ee','#f6ead8'],[.78,'#7f8fd0','#efb2c0','#ffc78c'],
 [.84,'#5c5ca8','#e07fa2','#ff9e5e'],[.88,'#41408a','#b35f95','#f0805f'],[.93,'#2b2f66','#5d4a8a','#a8698d'],
 [.97,'#3d4a8e','#a07db0','#e1a1a8'],[1,'#6f7fc4','#e9a9c4','#ffc58f']];
function skyAt(ph){let i=0;while(i<SKYK.length-2&&ph>SKYK[i+1][0])i++;const A=SKYK[i],B=SKYK[i+1],t=(ph-A[0])/(B[0]-A[0]);
 return [mix(A[1],B[1],t),mix(A[2],B[2],t),mix(A[3],B[3],t)]}
"""+s[k1:]
a=s[s.index("  if(ts-lastSkyPaint>80||reduce){"):]
a=a[:a.index("skyDirty=true}")+len("skyDirty=true}")]
s=s.replace(a,"""  if(ts-lastSkyPaint>80||reduce||paused){lastSkyPaint=ts;const [top,mid,hor]=skyAt(ph);
   skyEl.style.background=`linear-gradient(to bottom,${top} 0%,${mid} 26%,${hor} 46%,color-mix(in srgb,${hor} 45%,transparent) 62%,transparent 80%)`;
   skyDirty=true}""")
s=s.replace("const ph=reduce?.36:(t/DAY)%1,","const ph=reduce&&!scrubbed?.36:(t/DAY)%1,")
s=s.replace("const ph=reduce?.42:((t+NIGHT*.02)/NIGHT)%1,","const ph=reduce&&!scrubbed?.42:((t+NIGHT*.02)/NIGHT)%1,")
s=s.replace("let clockOff=0,","let scrubbed=false,clockOff=0,",1)
open('header2_js.txt','w').write(s)
print('ok')
