import re
s=open('feasts_js.txt').read()
L=s.split('\n')
def block(start_pat,end_pat):
    i=next(n for n,l in enumerate(L) if l.startswith(start_pat))
    j=next(n for n in range(i+1,len(L)) if L[n].startswith(end_pat))
    return i,j
def replace(start_pat,end_pat,new):
    global L
    i,j=block(start_pat,end_pat)
    L=L[:i]+new.strip('\n').split('\n')+['']+L[j:]

# ---------- lista dat: wszystkie 4 niedziele adwentu ----------
s='\n'.join(L)
s=s.replace("['1. niedziela adwentu',A],\n  ['3. niedziela adwentu',addD(A,14)],","['1. niedziela adwentu',A],\n  ['2. niedziela adwentu',addD(A,7)],['3. niedziela adwentu',addD(A,14)],['4. niedziela adwentu',addD(A,21)],")
assert "4. niedziela adwentu" in s
L=s.split('\n')

# ---------- drawFeast + rysowanie kreską ----------
replace("function drawFeast(){","// --- Adwent",r"""
function drawFeast(){
 if(!LY)return;
 const f=FEAST=feastOf(today()),b=document.body;
 b.className=b.className.replace(/\bf-\S+/g,'').trim();
 if(f){b.classList.add('f-'+f.id);if(f.pasja)b.classList.add('f-pasja')}
 [skyL,ridgeL,groundL].forEach(l=>l&&(l.innerHTML=''));for(const k in FX)delete FX[k];
 hideRowNear(-1,-1);
 if(!f)return;
 const {W,H,groundY,k,mobile,sceneW,th}=LY;
 const HT={boze:60,adwent:34,palmowa:44,wczwartek:40,wpiatek:66,wsobota:38,wielkanoc:38,wniebo:40,zielone:40,zniwa:48,reformacja:76,zmarli:28,wiecznosc:28};
 const sR=(W+sceneW)/2, sc=mobile?Math.max(.7,th/50)*.55:Math.min(th/50*1.45,(th*1.75-6)/(HT[f.id]||50)), px=mobile?W-34:sR+(W-sR)*.5;
 const G=E('g',{transform:`translate(${px.toFixed(1)} ${groundY.toFixed(1)}) scale(${sc.toFixed(3)})`},groundL);
 const hide=(a,b)=>hideRowNear(px+a*sc,px+b*sc);
 const base=firstFeast?4.6:.2;FX.t0=now()+base+1.5;           // historie ruszają, gdy scena jest już narysowana
 const draw={boze,adwent,palmowa,wczwartek,wpiatek,wsobota,wielkanoc,wniebo,zielone,zniwa,reformacja,zmarli:groby,wiecznosc:groby}[f.id];
 if(draw)draw(G,{px,sc,hide,f});
 drawIn(base);
 firstFeast=false;
}
// scena świąteczna kreśli się kreska po kresce, potem wypełniają się kolory (jak kościół)
function drawIn(base){let i=0;const D=()=>(base+(i++)*.022).toFixed(2);
 [skyL,ridgeL,groundL].forEach(Ly=>Ly.querySelectorAll('path,rect,circle,ellipse,polygon,line,polyline').forEach(el=>{
  if(el.closest('.nodraw')||el.closest('.rays')||el.closest('.star'))return;
  const d=D();
  if(el.classList.contains('flame')){el.style.animation=`ffade .6s ease ${d}s both,flameF ${(.38+(i%4)*.07).toFixed(2)}s ease-in-out ${-(i%5)*.11}s infinite alternate`;return}
  if(el.style.animationName){el.style.animation=`ffade .8s ease ${d}s both,`+el.style.animation;return}
  el.setAttribute('pathLength','1');el.classList.add('fdraw');el.style.setProperty('--fd',d+'s')}));
 [skyL,ridgeL,groundL].forEach(Ly=>Ly.querySelectorAll('.rays,.star').forEach(g=>g.style.animation=`ffade 1.2s ease ${D()}s both`))}
const tau=()=>now()-(FX.t0||0);
const put=(g,x,y,face,s,rot=0)=>g.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${(face*s).toFixed(3)} ${s.toFixed(3)})${rot?` rotate(${rot.toFixed(1)})`:''}`);
const actor=(par,color,opt)=>{const p=person(par,color,opt);p.classList.add('nodraw');p.style.display='none';return p};
""")

# ---------- Boże Narodzenie ----------
replace("// --- Boże Narodzenie","// --- Niedziela Palmowa",r"""
// --- Boże Narodzenie: stajenka z życiem w środku, gwiazda, pasterz, anioł; Królowie idą przez góry; 6.01 pokłon ---
function boze(G,{px,sc,hide,f}){const d=today(),epi=d.getMonth()===0&&d.getDate()===6;hide(-94,epi?96:48);
 const R=E('g',{},G);FX.nat={bow:[],epi};
 E('path',{class:'ff',fill:'#4a3a2c',d:'M-34,0 V-36 L0,-50 L34,-36 V0 Z'},R);
 FX.nat.warm=E('ellipse',{cx:0,cy:-12,rx:30,ry:20,fill:'url(#warm)'},R);
 // wół i osioł – osobne głowy, żeby mogły się ruszać
 const ox=E('g',{},R);E('path',{class:'ff',fill:'#6f5845',d:'M-29,-27 q1,-7 7,-7 q3,4 1,9 q-4,2 -8,-2 Z'},ox);E('path',{class:'fi',d:'M-26,-33 l-3,-3 M-21,-34 l2,-3'},ox);
 const don=E('g',{},R);E('path',{class:'ff',fill:'#8c857c',d:'M20,-31 q4,-6 8,-2 l-1,7 q-4,2 -7,-1 Z'},don);
 FX.nat.ear=E('path',{class:'fi',d:'M24,-33 l-1,-6 M26,-33 l2,-5'},don);
 FX.nat.ox=ox;FX.nat.don=don;
 E('rect',{class:'ff',fill:'#9a7048',x:-37,y:-38,width:4.5,height:38},R);E('rect',{class:'ff',fill:'#9a7048',x:32.5,y:-38,width:4.5,height:38},R);
 E('path',{class:'ff',fill:'#d9b45a',d:'M-45,-33 L0,-59 L45,-33 L40,-30 L0,-53 L-40,-30 Z'},R);
 for(let i=-4;i<=4;i++)E('path',{class:'thin',d:`M${i*1.2},-57.5 L${i*9.4},-31.5`},R);
 // żłóbek z Dzieciątkiem
 E('path',{class:'fi',d:'M-7,0 L-3,-6 M7,0 L3,-6'},R);E('path',{class:'ff',fill:'#9a7048',d:'M-9,-9 L9,-9 L6,-4 L-6,-4 Z'},R);
 E('path',{class:'ff',fill:'#e8c96a',d:'M-10,-9 Q-5,-13 0,-11 Q5,-14 10,-9 Z'},R);
 FX.nat.halo=E('circle',{cx:3.6,cy:-12.8,r:7,fill:'url(#fglow)'},R);
 E('ellipse',{class:'ff',fill:'#f6f2e8',cx:-.6,cy:-11.6,rx:4.6,ry:2.3},R);E('circle',{class:'ff',fill:SKIN,cx:3.8,cy:-12.6,r:1.9},R);
 // Maryja (pochyla się nad żłobkiem) i Józef z latarnią
 const mary=E('g',{},R);FX.nat.mary=mary;
 E('path',{class:'ff',fill:'#5b7fb5',d:'M-25,0 Q-25,-9 -20,-15 L-15,-15 Q-12,-8 -11,0 Z'},mary);
 E('path',{class:'ff',fill:'#7f9fcf',d:'M-21.8,-14 Q-21.8,-23.4 -17.6,-23.4 Q-13.6,-23.4 -13.4,-14 Z'},mary);E('circle',{class:'ff',fill:SKIN,cx:-17.4,cy:-19.4,r:2.6},mary);
 E('path',{class:'fi',d:'M-14.6,-15 L-9.6,-11.4'},mary);
 E('path',{class:'ff',fill:'#8a6a4a',d:'M13,0 L14.6,-21 Q18,-24 21.4,-21 L23,0 Z'},R);E('circle',{class:'ff',fill:SKIN,cx:18,cy:-25,r:2.9},R);
 E('path',{class:'ff',fill:'#7a6552',d:'M15.4,-24 Q18,-19.6 20.6,-24 Q18,-22.4 15.4,-24 Z'},R);E('path',{class:'fi',d:'M25.6,0 L25,-33 Q25,-36 27.6,-35.4'},R);
 E('path',{class:'fi',d:'M14.6,-17 L10.6,-14 L10.6,-12'},R);
 E('circle',{cx:10.6,cy:-9,r:6,fill:'url(#fglow)'},R);E('rect',{class:'ff',fill:'#3a3328',x:8.8,y:-11.6,width:3.6,height:5,rx:.6},R);
 E('path',{class:'flame',d:'M10.6,-10.8 Q11.8,-9 10.6,-7.6 Q9.4,-9 10.6,-10.8 Z'},R);
 // na zewnątrz: pasterz z owcami
 const O=E('g',{transform:'translate(-58 0)'},G);
 const sh=E('g',{},O);const p=person(sh,'#8b7d5c',{scarf:'#b9a77f'});E('path',{class:'fi',d:'M5,0 L5.6,-27 Q5.8,-31 8.6,-30'},sh);FX.nat.bow.push([sh,0,.6,22]);
 FX.nat.sheep=[];
 [[-14,0],[-26,0],[-20,3]].forEach(([x,y],i)=>{const sp=E('g',{},O);sp.dataset.x=x;sp.dataset.y=y;
  E('path',{class:'fi',d:'M-3,-3 V0 M3,-3 V0'},sp);E('ellipse',{class:'ff',fill:'#f6f3ec',cx:0,cy:-5.2,rx:5.8,ry:3.8},sp);
  const hd=E('ellipse',{class:'ff',fill:'#2d2a26',cx:6,cy:-6,rx:2,ry:1.5},sp);FX.nat.sheep.push([sp,hd,i])});
 // Trzej Królowie przy stajence (6.01)
 if(epi){const K=E('g',{transform:'translate(62 0) scale(-1 1)'},G);['#a83a32','#2f6a55','#6a4a8c'].forEach((c,i)=>{const m=E('g',{},K);magus(m,c,i);m.dataset.x=-12+i*12;FX.nat.bow.push([m,-12+i*12,i*.35,30])})}
 // anioł nad stajenką – co jakiś czas się pojawia
 const A=E('g',{class:'nodraw'},G);FX.nat.angel=A;A.style.opacity=0;
 FX.nat.wl=E('path',{class:'ff',fill:'#fffdf6',d:'M-1,-6 Q-12,-14 -14,-4 Q-8,-4 -2,-2 Z'},A);FX.nat.wr=E('path',{class:'ff',fill:'#fffdf6',d:'M1,-6 Q12,-14 14,-4 Q8,-4 2,-2 Z'},A);
 E('path',{class:'ff',fill:'#fffdf6',d:'M-4,8 L-2.6,-6 Q0,-8 2.6,-6 L4,8 Z'},A);E('circle',{class:'ff',fill:SKIN,cx:0,cy:-9,r:2.6},A);
 E('circle',{cx:0,cy:-9,r:4.4,fill:'none',stroke:'#e2b43c','stroke-width':.8},A);E('path',{class:'fi',d:'M-2.4,-4 L-6,-12 M2.4,-4 L6,-12'},A);
 // gwiazda betlejemska
 const S=E('g',{class:'star',transform:`translate(${(LY.mobile?LY.W*.66:px).toFixed(1)} ${(LY.H*.12).toFixed(1)}) scale(1.4)`},skyL);
 E('circle',{r:22*LY.k,fill:'url(#starglow)'},S);
 E('path',{class:'startail',d:`M0,0 Q${-40*LY.k},${18*LY.k} ${-92*LY.k},${30*LY.k}`},S);
 const r1=11*LY.k,r2=2.2*LY.k,r3=6*LY.k;let dd='';for(let i=0;i<16;i++){const a=i*Math.PI/8-Math.PI/2,r=i%4===0?r1:i%2===0?r3:r2;dd+=(i?'L':'M')+(Math.cos(a)*r).toFixed(1)+','+(Math.sin(a)*r).toFixed(1)}
 E('path',{class:'starbody',d:dd+'Z'},S);
 // Królowie w drodze przez góry (25.12 – 5.01): karawana wędruje grzbietem i znika za zboczem
 if(!epi&&!(d.getMonth()===11&&d.getDate()===24)){const g=E('g',{class:'nodraw'},ridgeL);FX.magi={figs:[]};
  ['#a83a32','#2f6a55','#6a4a8c'].forEach((c,i)=>{const m=E('g',{},g);magus(m,c,i);FX.magi.figs.push(m)});
  const cam=E('g',{},g);camel(cam);FX.magi.figs.push(cam)}}
function magus(m,c,i){E('path',{class:'ff',fill:'#b98d5a',d:'M-5.6,-14 Q-8.6,-12 -7.4,-8 Q-5,-7 -3.6,-9 Z'},m);   // tobołek na plecach
 E('path',{class:'ff',fill:c,d:'M-4.2,0 L-3.2,-15 Q0,-17.4 3.2,-15 L4.2,0 Z'},m);E('circle',{class:'ff',fill:i===1?'#b98b62':SKIN,cx:0,cy:-18.4,r:2.6},m);
 E('path',{class:'ff',fill:'#e2b43c',d:'M-2.6,-20.4 L-2.6,-23.6 L-1.3,-22 L0,-24.2 L1.3,-22 L2.6,-23.6 L2.6,-20.4 Z'},m);
 E(i===2?'path':'rect',i===2?{class:'ff',fill:'#d9b24a',d:'M3,-12 Q3,-15.6 5,-15.6 Q7,-15.6 7,-12 L6.4,-10 L3.6,-10 Z'}:{class:'ff',fill:i?'#d9b24a':'#c9a24a',x:3,y:-13.4,width:4.2,height:3.6},m)}
function camel(g){g.lA=E('path',{class:'fi',d:'M-8,-9 L-10,0 M-5,-9 L-4,0 M6,-9 L5,0 M9,-9 L11,0'},g);g.lB=E('path',{class:'fi',d:'M-8,-9 L-6,0 M-5,-9 L-7,0 M6,-9 L8,0 M9,-9 L8,0',style:'display:none'},g);
 E('path',{class:'ff',fill:'#c79a62',d:'M-11,-10 Q-10,-17 -4,-18 Q-1,-23 3,-18 Q8,-17 10,-12 L13,-20 Q14,-24 17,-23 L18,-21 L15,-19 L12.5,-9 Q0,-7 -11,-10 Z'},g);
 E('rect',{class:'ff',fill:'#8a5a3a',x:-6,y:-20,width:6,height:5,rx:1},g);E('rect',{class:'ff',fill:'#6a7a4a',x:1,y:-21,width:5,height:5.4,rx:1},g)}
""")

# ---------- Niedziela Palmowa ----------
replace("// --- Niedziela Palmowa","// --- Wielki Czwartek",r"""
// --- Niedziela Palmowa: Jezus wjeżdża na osiołku, ludzie machają gałązkami i rzucają je na drogę ---
function frondSmall(par,len){let d=`M0,0 L0,${-len}`;for(let s=.2;s<.95;s+=.16){const y=-len*s,l=(1-s)*5+1.4;d+=` M0,${y.toFixed(1)} l${-l},${(-l*.7).toFixed(1)} M0,${y.toFixed(1)} l${l},${(-l*.7).toFixed(1)}`}
 return E('path',{class:'leaflet',d},par)}
function donkeyRider(par){const g=E('g',{class:'nodraw'},par);
 g.lA=E('path',{class:'fi',d:'M-9,-9 L-11,0 M-6,-9 L-5,0 M7,-9 L9,0 M10,-9 L11,0'},g);g.lB=E('path',{class:'fi',d:'M-9,-9 L-7,0 M-6,-9 L-8,0 M7,-9 L5,0 M10,-9 L12,0',style:'display:none'},g);
 E('path',{class:'fi',d:'M-12,-12 Q-15,-10 -14,-6'},g);
 E('path',{class:'ff',fill:'#9a948c',d:'M18.5,-21.5 L17,-27 L19.5,-22 Z M20.5,-21.8 L21,-27.4 L22,-21.6 Z'},g);
 E('path',{class:'ff',fill:'#9a948c',d:'M-12,-10 Q-12,-16 -4,-16 L8,-16 Q12,-16 13,-14 L17,-20 Q19,-23 22,-21 L23,-18 L19,-15 L15,-9 Q2,-7 -12,-10 Z'},g);
 E('circle',{cx:0,cy:-32.4,r:4.6,fill:'none',stroke:'#e2b43c','stroke-width':.8},g);
 E('path',{class:'ff',fill:'#f4f0e6',d:'M-4,-15 L-3,-29 Q0,-31.4 3,-29 L4,-15 Z'},g);
 E('path',{class:'ff',fill:'#b8433a',d:'M-3.6,-28 Q-6,-20 -4.6,-13.6 L-1,-13.6 L-.6,-28 Z'},g);
 E('path',{class:'fi',d:'M1,-16 L3.6,-11 L3.8,-7.6 M2.6,-26 L7,-20'},g);
 E('circle',{class:'ff',fill:SKIN,cx:0,cy:-32.4,r:2.8},g);E('path',{class:'ff',fill:'#5a3a22',d:'M-2.9,-32.6 Q-3,-36 0,-35.6 Q3,-36 2.9,-32.6 Q2.6,-29 0,-29.2 Q-2.6,-29 -2.9,-32.6 Z M-1.6,-31.6 Q0,-30.4 1.6,-31.6 Q1.6,-33.8 0,-34 Q-1.6,-33.8 -1.6,-31.6 Z'},g);
 E('circle',{class:'ff',fill:SKIN,cx:0,cy:-32.4,r:1.6},g);
 return g}
function palmowa(G,{px,sc,hide}){const {W,groundY}=LY;hideRowNear(W*.58,W+10);
 FX.palm={rider:donkeyRider(groundL),crowd:[],laid:E('g',{class:'nodraw'},groundL)};
 const cols=[['#a8463a',{scarf:'#d9c7a0'}],['#3f6a8c',{hair:'#5a3a22'}],['#6b7a3a',{hair:'#2d2a26'}],['#8c5a8a',{scarf:'#e6d9b8'}],['#b07a3a',{hair:'#3a2a1c'}]];
 cols.forEach(([c,o],i)=>{const p=actor(groundL,c,o);p.armsDown.style.display='none';p.armsUp.setAttribute('d','M-3.2,-17 L-5,-10 M3.2,-17 L6,-24');p.armsUp.style.display='';
  const fr=E('g',{transform:'translate(6 -24)'},p);frondSmall(fr,12);p.fr=fr;p.xf=W*(.93-i*.075);FX.palm.crowd.push(p)});
 // kilka gałęzi przy drodze, żeby było widać od pierwszej chwili
 [[-30,-6],[30,8]].forEach(([x,a])=>{const g=E('g',{transform:`translate(${x} 0) rotate(${a})`},G);frondSmall(g,26)})}
""")

# ---------- Wielka Sobota / Wielkanoc ----------
replace("// --- Wielka Sobota i Wielkanoc","// --- Wniebowstąpienie",r"""
// --- Wielka Sobota i Wielkanoc: grób zamknięty / otwarty, anioł na kamieniu, kobiety biegną do grobu ---
function tomb(G,open){
 E('path',{class:'ff',fill:'#b7ab95',d:'M-50,0 Q-46,-30 -12,-36 Q28,-38 50,0 Z'},G);E('path',{class:'thin',d:'M-34,-18 l8,-3 M22,-24 l9,4 M-20,-30 l6,1'},G);
 E('path',{class:'ff',fill:'#2f2a22',d:'M-9,0 V-13 Q0,-24 9,-13 V0 Z'},G);
 if(open){const L=E('g',{class:'rays'},G);for(let i=0;i<11;i++){const a=Math.PI*(1+i/10);E('path',{class:'ray2',d:`M${(Math.cos(a)*11).toFixed(1)},${(-8+Math.sin(a)*11).toFixed(1)} L${(Math.cos(a)*30).toFixed(1)},${(-8+Math.sin(a)*30).toFixed(1)}`,style:`animation-delay:${-i*.3}s`},L)}
  E('ellipse',{cx:0,cy:-8,rx:12,ry:10,fill:'url(#whiteglow)'},G);
  E('circle',{class:'ff',fill:'#9c9483',cx:24,cy:-11,r:11.5},G);E('path',{class:'thin',d:'M17,-15 q6,-3 12,1 M19,-7 q5,2 10,-1'},G);
  // anioł siedzący na odsuniętym kamieniu (Mk 16,5)
  const A=E('g',{transform:'translate(25 -22)'},G);FX.angelE=A;
  E('path',{class:'ff',fill:'#fffdf6',d:'M-1,-8 Q-11,-17 -12,-6 Q-7,-6 -2,-3 Z'},A);
  E('path',{class:'ff',fill:'#fffdf6',d:'M-4,0 L-3,-10 Q0,-12.4 3,-10 L3.6,-3 L7,-1 L7,1 L-4,1 Z'},A);
  E('circle',{class:'ff',fill:SKIN,cx:0,cy:-13,r:2.5},A);E('circle',{cx:0,cy:-13,r:4.2,fill:'none',stroke:'#e2b43c','stroke-width':.7},A);
  [[-40,0],[-33,1],[38,0]].forEach(([x,y])=>{E('path',{class:'stem',d:`M${x},${y} Q${x+1},${y-8} ${x},${y-14}`},G);
   E('path',{class:'ff',fill:'#fffdf6',d:`M${x},${y-14} l-3.4,-4 l2.2,.6 l1.2,-3.4 l1.2,3.4 l2.2,-.6 Z`},G)})}
 else{E('circle',{class:'ff',fill:'#9c9483',cx:0,cy:-11,r:12.5},G);E('path',{class:'thin',d:'M-7,-15 q6,-3 12,1 M-5,-7 q5,2 10,-1'},G)}}
function wsobota(G,{hide}){hide(-52,52);tomb(G,false)}
function wielkanoc(G,{px,sc,hide}){hide(-52,52);tomb(G,true);
 FX.easter={px,sc,women:[]};
 [['#8c5a8a','#e6d9b8'],['#3f6a8c','#d9c7a0'],['#a8463a','#efe6cf']].forEach(([c,s])=>{const w=actor(groundL,c,{scarf:s});
  E('path',{class:'ff',fill:'#c9a46a',d:'M4.6,-12 h3 v3.4 q-1.5,1 -3,0 Z'},w);FX.easter.women.push(w)})}
""")

# ---------- Zielone Świątki ----------
replace("// --- Zesłanie Ducha","// --- Święto Żniw",r"""
// --- Zesłanie Ducha Świętego: gołębica, ogniste języki spływają nad głowy zebranych ---
function birch(par,x,h,i){const t=E('g',{class:'frond',style:`transform-origin:${x}px 0px;animation-delay:${-i}s`},par);
 E('path',{class:'ff',fill:'#f4f1ea',d:`M${x-1.7},0 L${x-.7},${-h} L${x+.7},${-h} L${x+1.7},0 Z`},t);
 E('path',{class:'thin',d:`M${x-1.5},${-h*.18} h2.2 M${x-1.1},${-h*.42} h1.6 M${x-1.3},${-h*.64} h1.6`},t);
 for(let j=0;j<6;j++){const yy=-h+4+j*h*.12,side=j%2?1:-1,len=12-j*.5,ex=x+side*len,ey=yy+len*.9;
  E('path',{class:'twig',d:`M${x},${yy} Q${(x+side*len*.7).toFixed(1)},${(yy-2).toFixed(1)} ${ex.toFixed(1)},${ey.toFixed(1)}`},t);
  for(let q=.3;q<=1.01;q+=.23){const lx=x+side*len*q*(1-.15*q),ly=yy-2*q+(ey-yy+2)*q*q;
   E('ellipse',{class:'birchleaf',cx:lx.toFixed(1),cy:(ly+1.2).toFixed(1),rx:1.15,ry:1.7,transform:`rotate(${side*20} ${lx.toFixed(1)} ${(ly+1.2).toFixed(1)})`},t)}}}
function zielone(G,{px,sc,hide}){hide(-62,62);birch(G,-54,50,0);birch(G,56,56,1);
 FX.pent={px,sc,people:[],flames:[]};
 const cols=[['#a8463a',{hair:'#5a3a22'}],['#3f6a8c',{scarf:'#e6d9b8'}],['#6b7a3a',{hair:'#2d2a26'}],['#8c5a8a',{hair:'#3a2a1c'}],['#b07a3a',{scarf:'#d9c7a0'}]];
 cols.forEach(([c,o],i)=>{const p=actor(groundL,c,o);p.xo=(i-2)*15;FX.pent.people.push(p);
  const fl=E('path',{class:'tongue nodraw',d:'M0,-7 Q2.6,-3 0,0 Q-2.6,-3 0,-7 Z',style:'display:none'},groundL);FX.pent.flames.push(fl)});
 FX.dove=E('g',{class:'nodraw'},skyL);const d=FX.dove;
 E('circle',{r:16,fill:'url(#whiteglow)'},d);
 FX.dove.w1=E('path',{class:'ff',fill:'#fff',d:'M-1,-1 Q-6,-12 -13,-11 Q-8,-5 -3,1 Z'},d);
 E('path',{class:'ff',fill:'#fff',d:'M-10,1 Q-4,-3 4,-2 Q9,-2 10,-5 Q12,-5 12,-3 L14,-2.6 L12,-1.6 Q10,3 2,3.4 Q-4,3.6 -10,1 L-14,3 L-13,-.6 Z'},d);
 FX.dove.w2=E('path',{class:'ff',fill:'#fff',d:'M1,-1 Q-2,-13 -9,-14 Q-6,-6 -2,1 Z'},d);E('circle',{class:'eye2',cx:10.6,cy:-3.4,r:.6},d)}
""")

s='\n'.join(L)
# ---------- Reformacja: czas od narysowania sceny, postacie nie „kreślą się” ----------
R=[("const Lg=E('g',{},groundL);FX.ref.L=Lg;","const Lg=E('g',{class:'nodraw'},groundL);FX.ref.L=Lg;"),
("const p=person(groundL,c,o);p.style.display='none';FX.ref.P.push(p)})}","const p=actor(groundL,c,o);FX.ref.P.push(p)})}"),
("lp.sheet=E('rect',","lp.style.display='none';lp.sheet=E('rect',")]
for a,b in R:
    assert a in s,a[:50]; s=s.replace(a,b)
open('feasts_js.txt','w').write(s)
print('ok')
