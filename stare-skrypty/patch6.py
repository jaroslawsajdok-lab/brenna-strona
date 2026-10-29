s=open('header2_js.txt').read()

# ---------- wiatr: fala od lewej do prawej przez wszystkie drzewa ----------
a="  t.style.setProperty('--d',(4.4+(i++%20)*.05)+'s');row.appendChild(t)}"
b="  t.style.setProperty('--d',(4.4+(i++%20)*.05)+'s');t.style.setProperty('--w',(x/W*4-12).toFixed(2)+'s');row.appendChild(t)}"
assert a in s;s=s.replace(a,b)
a="if(!first){land.querySelectorAll('.draw,.ridge-fill,.clouds,.rowtree').forEach(e=>{e.style.animation='none';e.style.opacity=1;if(e.classList.contains('draw'))e.style.strokeDashoffset=0});"
b="if(!first){land.querySelectorAll('.draw,.ridge-fill,.clouds').forEach(e=>{e.style.animation='none';e.style.opacity=1;if(e.classList.contains('draw'))e.style.strokeDashoffset=0});\n  land.querySelectorAll('.rowtree').forEach(e=>{e.style.opacity=1;e.style.animation='windRow 5s ease-in-out infinite alternate '+e.style.getPropertyValue('--w')});"
assert a in s;s=s.replace(a,b)
s=s.replace("  land.querySelectorAll('.rowtree').forEach(e=>e.style.setProperty('--d','0s'));\n","")
a="  t.querySelectorAll('.leaf').forEach((l,j)=>l.style.animationDelay=(4.6+pl*.3+(i%12)*.06+j*.06)+'s')});"
b=a+"""
 scene.querySelectorAll('.tree').forEach(t=>{const x=parseFloat(t.style.transformOrigin),f=.27+((x+96)/540)*.46;   // ta sama fala wiatru
  t.style.animation=`windTree 5s ease-in-out ${(f*4-12).toFixed(2)}s infinite alternate`});"""
assert a in s;s=s.replace(a,b)

# ---------- królik i sarenka (wiosna) ----------
a=" front.appendChild(gr);front.appendChild(fl);"
b=a+r"""

 // zwierzęta (wiosna): rysunki w układzie „pyszczek w prawo”, pozycje liczy critterTick()
 const zoo=el('g',{class:'deco only-wiosna zoo'});
 const mk=(tag,at,par)=>{const e=el(tag,at);par.appendChild(e);return e};
 rabbit=mk('g',{class:'critter'},zoo);
 const rb=mk('g',{},rabbit);
 mk('path',{class:'ear',d:'M4.2,-12 C3,-17 1.6,-21.5 0.6,-21.3 C-.3,-21 1.2,-16 2.6,-11.6 Z'},rb);
 mk('path',{class:'ear',d:'M5.6,-12.2 C5.4,-17.6 4.8,-22 3.8,-22 C2.8,-22 3.2,-17 4,-11.8 Z'},rb);
 mk('ellipse',{class:'fur',cx:0,cy:-6.5,rx:7.4,ry:4.6},rb);
 mk('circle',{class:'fur',cx:6.2,cy:-10,r:3.4},rb);
 mk('circle',{class:'tailw',cx:-7.4,cy:-7.6,r:2},rb);
 mk('circle',{class:'eye',cx:7.4,cy:-10.6,r:.55},rb);
 rabbit.pA=mk('path',{class:'leg',d:'M-3.6,-3.6 L-11.5,-1.2 M3.6,-3.4 L9.6,-1.4'},rb);       // w locie – wyciągnięty
 rabbit.pB=mk('path',{class:'leg',d:'M-3,-2.8 L-5.4,0 L-.6,0 M3.4,-2.8 L4.4,0'},rb);         // przyziemienie – skulony
 deer=mk('g',{class:'critter'},zoo);
 const db=mk('g',{},deer);
 deer.pS=mk('path',{class:'leg',d:'M9,-19 L9.6,-9 L10,0 M5.6,-19 L5.4,0 M-11,-19 L-12.6,-9.5 L-11.4,0 M-7.6,-19 L-8.2,0'},db);
 deer.pA=mk('path',{class:'leg',d:'M9,-19 L18,-10 L22.5,-4 M6,-19 L14,-12 L19,-7 M-11,-19 L-20,-11 L-25.5,-7 M-8,-19 L-17,-13 L-23,-10'},db);
 deer.pB=mk('path',{class:'leg',d:'M9,-19 L6,-11 L9.5,-6 M6,-19 L3,-12 L6.5,-7 M-11,-19 L-4,-12 L-1,-7 M-8,-19 L-2,-13 L1.5,-9'},db);
 mk('path',{class:'hide',d:'M-15.5,-24.5 C-15,-30 -6,-31.5 4,-30.5 C11,-30 15.5,-27.5 15,-22 C14.5,-18 8,-17.5 0,-17.8 C-8,-18 -15.8,-19 -15.5,-24.5 Z'},db);
 mk('ellipse',{class:'rump',cx:-14,cy:-24,rx:2.6,ry:3.6},db);
 deer.head=mk('g',{style:'transform-origin:11px -27px'},db);
 mk('path',{class:'hide',d:'M8,-28.5 L13.5,-41 L18.5,-40 L15,-25 Z'},deer.head);
 mk('path',{class:'hide',d:'M13.2,-41.6 C14,-44.6 19,-44.6 23.6,-40.8 C25.2,-39.6 24.4,-38 22.4,-38 C19.6,-37.8 15.4,-37.6 14,-38.6 C12.8,-39.4 12.6,-40.4 13.2,-41.6 Z'},deer.head);
 deer.ears=mk('g',{style:'transform-origin:15px -43px'},deer.head);
 mk('path',{class:'hide',d:'M14.6,-42.6 C13,-46 12.6,-49.4 14,-49.6 C15.4,-49.6 16.4,-46.4 16.4,-43 Z'},deer.ears);
 mk('path',{class:'hide',d:'M16.4,-43 C16.4,-46.8 17.8,-49.8 19,-49.4 C20.2,-49 19.2,-45.4 18,-42.6 Z'},deer.ears);
 mk('circle',{class:'eye',cx:18.6,cy:-41.4,r:.7},deer.head);
 mk('circle',{class:'eye',cx:24,cy:-39.4,r:.75},deer.head);
 front.appendChild(zoo);
 CR={W,groundY,k:k*1.05};critterTick();"""
assert a in s;s=s.replace(a,b,1)

# globalne + logika ruchu (czysta funkcja czasu → działa z suwakiem)
a="let clockOff=0,"
s=s.replace("let scrubbed=false,clockOff=0,","""let rabbit=null,deer=null,CR=null;
const hsh=n=>{const v=Math.sin(n*12.9898+78.233)*43758.5453;return v-Math.floor(v)};
function show(a,on){a.style.display=on?'':'none'}
function critterTick(){
 if(!CR||!rabbit)return;const {W,groundY,k}=CR,t=now();
 // KRÓLIK: raz na ok. 35 s przebiega przez całą stronę, kicając
 {const P=35,v=Math.max(150,W/6.5),dur=(W+120)/v,n=Math.floor(t/P),off=n===0?9:4+hsh(n)*Math.max(0,P-dur-6),u=t-n*P-off;
  if(u<0||u>dur){rabbit.style.display='none'}else{
   const dir=n===0||hsh(n+.5)<.6?1:-1,x=dir>0?-60+v*u:W+60-v*u,hop=.4,ph=(u%hop)/hop,air=Math.sin(Math.PI*ph),s=k*1.15;
   rabbit.style.display='';show(rabbit.pA,air>.35);show(rabbit.pB,air<=.35);
   rabbit.setAttribute('transform',`translate(${x.toFixed(1)} ${(groundY-air*9*k).toFixed(1)}) scale(${dir*s} ${s}) rotate(${((ph-.5)*-14).toFixed(1)})`)}}
 // SARENKA: raz na ok. 55 s wbiega, staje w pół drogi, nasłuchuje i ucieka
 {const P=55,n=Math.floor(t/P),off=n===0?20:6+hsh(n+3)*30,u=t-n*P-off,dir=n%2===0?1:-1;
  const x0=dir>0?-70:W+70,xs=dir>0?W*.3:W*.7,v=Math.max(140,W/8.5),T1=Math.abs(xs-x0)/v*1.35,T2=3.6,T3=Math.abs(xs-x0)/(v*2.1)*1.2;
  if(u<0||u>T1+T2+T3){deer.style.display='none'}else{
   deer.style.display='';const s=k*1.2;let x,face=dir,pose='S',bob=0,head=0,ear=0;
   if(u<T1){const q=u/T1,e=1-(1-q)*(1-q);x=x0+(xs-x0)*e;const sp=2*(1-q);   // zwalnia do zatrzymania
    if(sp>.25){const d=Math.abs(x-x0)/16;pose=Math.floor(d)%2?'A':'B';bob=Math.abs(Math.sin(d*Math.PI))*4*Math.min(1,sp)}}
   else if(u<T1+T2){x=xs;const w=u-T1;head=w>.5&&w<2.6?-14*Math.min(1,(w-.5)/.3,(2.6-w)/.3):0;ear=(w>1.6&&w<1.8)||(w>2.9&&w<3.05)?-18:0}
   else{const q=(u-T1-T2)/T3,e=Math.pow(q,1.4);x=xs+(x0-xs)*e;face=-dir;const d=Math.abs(x-xs)/20;pose=Math.floor(d)%2?'A':'B';bob=Math.abs(Math.sin(d*Math.PI))*7}
   show(deer.pS,pose==='S');show(deer.pA,pose==='A');show(deer.pB,pose==='B');
   deer.head.setAttribute('transform',`rotate(${head})`);deer.ears.setAttribute('transform',`rotate(${ear})`);
   deer.setAttribute('transform',`translate(${x.toFixed(1)} ${(groundY-bob*k).toFixed(1)}) scale(${face*s} ${s})`)}}
}
let scrubbed=false,clockOff=0,""",1)
s=s.replace("function tick(ts){\n skyTick(ts);\n","function tick(ts){\n skyTick(ts);critterTick();\n",1)
open('header2_js.txt','w').write(s)
print('ok')
