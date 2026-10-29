s=open('header2_js.txt').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80]); s=s.replace(a,b)

# ===== zegar ścienny (wspólny dla wszystkich odwiedzających) =====
rep("let lseed=12345;const lr=()=>(lseed=(lseed*16807)%2147483647)/2147483647;\nlet simT=0;                                    // ile sekund \"żyje\" jesień na stronie",
r"""let lseed=12345;const lr=()=>(lseed=(lseed*16807)%2147483647)/2147483647;
// Liście i śnieg liczone są od PEŁNEJ GODZINY zegara, nie od otwarcia strony –
// każdy odwiedzający o tej samej porze widzi to samo. Zegar korygowany nagłówkiem Date z serwera.
const HOUR=3600,STEP=.05,RAKE_D=180;
let simT=0,simN=0,simHour=null,WALLBASE=null;
const wall=()=>{if(WALLBASE===null)WALLBASE=Date.now()/1000-now();return WALLBASE+now()};
const hourPos=()=>{const w=wall(),h=Math.floor(w/HOUR);return [h,w-h*HOUR]};
try{fetch(location.href,{method:'HEAD',cache:'no-store'}).then(r=>{const d=r.headers.get('Date');if(!d)return;
 const skew=(new Date(d).getTime()-Date.now())/1000;if(Math.abs(skew)>2){wall();WALLBASE+=skew}}).catch(()=>{})}catch(e){}""")

# ===== krok symulacji liści: bez rysowania, z zapamiętaniem poprzedniej pozycji =====
rep(" simT+=dt;\n const {W,H,groundY,k,mobile}=G;\n spawnAcc+=dt*(mobile?1:1.7);",
    " simT+=dt;\n const {W,H,groundY,k,mobile}=G;\n spawnAcc+=simT<HOUR-RAKE_D?dt*(mobile?1:1.7):0;      // gdy przychodzi ksiądz, wiatr cichnie")
rep("   c:LEAFC[(lr()*LEAFC.length)|0],s:.8+lr()*.5,st:'air'};",
    "   c:LEAFC[(lr()*LEAFC.length)|0],s:.8+lr()*.5,st:'air'};f.px=f.x;f.py=f.y;f.pr=f.rot;")
rep(" for(let i=falling.length-1;i>=0;i--){const f=falling[i];\n  if(f.st==='air'){",
    " for(let i=falling.length-1;i>=0;i--){const f=falling[i];f.px=f.x;f.py=f.y;f.pr=f.rot;\n  if(f.st==='air'){")
rep("function resetLeaves(){PR.cycle=0;PR.active=false;lseed=12345;simT=0;",
    "function resetLeaves(hr){PR.active=false;PR.done=false;simHour=hr;lseed=1+(((hr||0)*2654435761)>>>0)%2147483645;simN=0;simT=0;")
rep("let rabbit=null,deer=null,CR=null,tourists=[],priestG=null;\nconst PR={cycle:0,active:false,x:-40,acc:0,raking:false};",
    "let rabbit=null,deer=null,CR=null,tourists=[],priestG=null;\nconst PR={active:false,done:false,x:-40,acc:0,raking:false};")

# ===== ksiądz: wchodzi 3 min przed pełną godziną, kończy równo o pełnej =====
i=s.index("function rakeStep(dt,fast){");j=s.index("// LATO: turyści")
s=s[:i]+r"""function rakeStep(dt){if(!G||!heights)return;const {W,k}=G;
 if(!PR.active&&!PR.done&&simT>=HOUR-RAKE_D){PR.active=true;PR.x=-40;PR.acc=0}
 if(!PR.active)return;
 const left=HOUR-simT,walkT=(W+40-PR.x)/(36*k),rate=Math.max(24,settled.length/Math.max(2,left-walkT-4));
 const reach=PR.x+14*k,R=9*k,near=[];for(const L of settled)if(Math.abs(L.fx*W-reach)<R)near.push(L);
 if(near.length){PR.raking=true;PR.acc+=dt*rate;
  while(PR.acc>=1&&near.length){PR.acc-=1;let bi=0;for(let q=1;q<near.length;q++)if(near[q].h>near[bi].h)bi=q;
   const L=near.splice(bi,1)[0];settled.splice(settled.indexOf(L),1);L.node&&L.node.remove();
   const b=Math.round(L.fx*W/BIN);heights[b]=Math.max(0,heights[b]-1.3*k*L.s);if(b>0)heights[b-1]=Math.max(0,heights[b-1]-.5*k);if(b<heights.length-1)heights[b+1]=Math.max(0,heights[b+1]-.5*k)}}
 else{PR.raking=false;PR.acc=0;PR.x+=dt*36*k*Math.max(1,walkT/Math.max(1,left-2));
  const b0=Math.max(0,Math.round((reach-R)/BIN)),b1=Math.min(heights.length-1,Math.round((reach+R)/BIN));for(let b=b0;b<=b1;b++)heights[b]=0}
 if(PR.x>W+40){PR.active=false;PR.done=true}}
function renderLeaves(a){
 falling.forEach(f=>{const x=f.px+(f.x-f.px)*a,y=f.py+(f.y-f.py)*a,r=f.pr+(f.rot-f.pr)*a;f.node.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${r.toFixed(0)})`)});
 if(!priestG||!G)return;const {groundY,k}=G;priestG.style.display=PR.active?'':'none';if(!PR.active)return;const s=k*1.15;
 priestG.setAttribute('transform',`translate(${PR.x.toFixed(1)} ${groundY.toFixed(1)}) scale(${s} ${s})`);
 if(PR.raking){walkLegs(priestG,0);priestG.rake.setAttribute('transform',`rotate(${(Math.sin(simT*7)*14).toFixed(1)} 3.6 -15)`)}
 else{walkLegs(priestG,PR.x/s);priestG.rake.setAttribute('transform','')}}
// doprowadza stan liści do bieżącej chwili godziny (stały krok = identyczny wynik u każdego)
function syncLeaves(maxSteps=15000){
 if(!G||!heights||document.body.dataset.season!=='jesien')return;
 const [hr,within]=hourPos(),target=Math.floor(within/STEP);
 if(hr!==simHour||target<simN)resetLeaves(hr);
 let n=0;while(simN<target&&n<maxSteps){stepLeaves(STEP,true);simN++;n++}
 renderLeaves(simN<target?1:Math.min(1,(within-simN*STEP)/STEP))}

"""+s[j:]
rep(" rakeStep(dt,fast)\n}"," rakeStep(dt)\n}")
rep(" priestG=makePriest(lv);rakeStep(0,false);"," priestG=makePriest(lv);")
rep(" if(!paused)stepLeaves(last?Math.min(.05,(ts-last)/1000):0);"," syncLeaves();snowTick();")

# ===== ZIMA: śnieg i odśnieżarka =====
rep(" priestG=makePriest(lv);",r""" priestG=makePriest(lv);
 // śnieg (zima): warstwa liczona wprost z minuty godziny, płatki, odśnieżarka o pełnej godzinie
 const sw=el('g',{class:'deco only-zima snow'});front.appendChild(sw);
 SN={W,H,groundY,k,mobile,layer:E('path',{class:'snowlayer'},sw),edge:E('path',{class:'snowedge'},sw),flakes:[],plow:makePlow(sw),spray:[]};
 for(let i=0;i<(mobile?34:72);i++)SN.flakes.push(E('circle',{class:'flake',r:((.7+hsh(i+.31)*1.5)*k).toFixed(2)},sw));
 for(let i=0;i<14;i++)SN.spray.push(E('circle',{class:'flake',r:(1+hsh(i+.77)*1.4)*k},sw));""")

s=s.replace("let rabbit=null,deer=null,CR=null,",r"""let SN=null;
const PLOW_V=70;                                       // px/s (skalowane)
function plowTimes(){const {W,k}=SN,v=PLOW_V*k,ts=HOUR-(W+260*k)/v-3;return {v,ts}}
const snowMax=()=>SN.H*(SN.mobile?.045:.06);
const snowShape=x=>1+.16*Math.sin(x*.021+1)+.09*Math.sin(x*.067+2)+.05*Math.sin(x*.19);
function snowDepth(x,within){const {v,ts}=plowTimes(),bx=-140*SN.k+v*(within-ts);          // bx = pozycja lemiesza
 const tp=ts+(x+140*SN.k)/v,acc=(within>=ts&&x<bx)?within-tp:within;               // za pługiem śnieg rośnie od nowa
 return snowMax()*Math.min(1,Math.max(0,acc)/(HOUR-RAKE_D))*snowShape(x)}
function makePlow(par){const g=E('g',{class:'plow',style:'display:none'},par);
 E('path',{class:'ff',fill:'#e9e6df',d:'M30,-2 Q36,-6 40,-2 Z'},g);                                    // śnieg przed lemieszem
 g.mound=g.lastChild;
 E('path',{class:'ff',fill:'#e08a2c',d:'M-30,-6 L-30,-17 L-6,-17 L-6,-27 Q-6,-30 -3,-30 L12,-30 Q15,-30 16,-27 L20,-17 L25,-16 L25,-6 Z'},g);
 E('path',{class:'ff',fill:'#cfe3ee',d:'M-3,-27.4 L11,-27.4 L14.6,-18 L-3,-18 Z'},g);E('path',{class:'thin',d:'M5,-27.4 V-18 M-24,-12 H-10 M-24,-9 H-10'},g);
 E('rect',{class:'ff',fill:'#3a3a3a',x:-29,y:-21,width:20,height:4},g);
 g.beacon=E('rect',{class:'ff',fill:'#ffb020',x:3,y:-33.4,width:5,height:3.4,rx:1},g);g.glow=E('circle',{cx:5.5,cy:-32,r:9,fill:'url(#fglow)'},g);
 E('path',{class:'fi',d:'M25,-10 L31,-10'},g);
 E('path',{class:'ff',fill:'#ffd23f',d:'M29,-1 L33,-16 L37,-15 L34,1 Z'},g);E('path',{class:'thin',d:'M31,-6 L35,-5 M32,-11 L36,-10'},g);
 g.w=[];[[-20,0],[14,0]].forEach(([x,y])=>{const w=E('g',{transform:`translate(${x} ${y-5})`},g);E('circle',{class:'ff',fill:'#2d2a26',cx:0,cy:0,r:5.6},w);E('circle',{class:'ff',fill:'#9a948c',cx:0,cy:0,r:2.2},w);E('path',{class:'thin',d:'M-2,0 H2'},w);g.w.push(w)});
 return g}
function snowTick(){if(!SN||document.body.dataset.season!=='zima')return;
 const {W,H,groundY,k}=SN,[hr,within]=hourPos(),t=wall();
 let d=`M-10,${groundY+2} L-10,${(groundY-snowDepth(-10,within)).toFixed(1)}`,e='M-10,'+(groundY-snowDepth(-10,within)).toFixed(1);
 for(let x=-4;x<=W+12;x+=6){const y=(groundY-snowDepth(x,within)).toFixed(1);d+=` L${x},${y}`;e+=` L${x},${y}`}
 SN.layer.setAttribute('d',d+` L${W+12},${groundY+2} Z`);SN.edge.setAttribute('d',e);
 SN.flakes.forEach((f,i)=>{const v=(14+hsh(i+.5)*12)*k,span=H*1.15,y=((t*v+hsh(i+.9)*span)%span)-H*.08,x=hsh(i+.1)*(W+40)-20+Math.sin(t*.7+i)*9*k;
  f.setAttribute('cx',x.toFixed(1));f.setAttribute('cy',y.toFixed(1));f.style.opacity=y>groundY-snowDepth(x,within)?0:.9});
 const {v,ts}=plowTimes(),P=SN.plow,bx=-140*k+v*(within-ts),on=within>=ts&&bx<W+170*k;
 P.style.display=on?'':'none';if(!on){SN.spray.forEach(c=>c.style.opacity=0);return}
 const s=k*1.25,x=bx-37*s,dep=snowDepth(bx+8*k,within);
 P.setAttribute('transform',`translate(${x.toFixed(1)} ${(groundY+1).toFixed(1)}) scale(${s.toFixed(2)})`);
 const m=Math.min(14,1+dep/s*1.4);P.mound.setAttribute('d',`M30,0 Q${36+m*.5},${-m*1.1} ${40+m},0 Z`);
 const blink=(t*2.2)%1<.5;P.beacon.setAttribute('fill',blink?'#ffb020':'#a8641c');P.glow.style.opacity=blink?1:.15;
 P.w.forEach(w=>w.lastChild.setAttribute('transform',`rotate(${((bx/(5.6*s))*57)%360})`));
 SN.spray.forEach((c,i)=>{const q=((t*1.7+i/14)%1),ang=-1.2+hsh(i+.2)*.7,sp=(40+hsh(i+.4)*50)*k;
  c.setAttribute('cx',(bx+4*k+Math.cos(ang)*sp*q).toFixed(1));c.setAttribute('cy',(groundY-10*k+Math.sin(ang)*sp*q+90*k*q*q).toFixed(1));
  c.style.opacity=dep>1.5*k?(1-q).toFixed(2):0})}
let rabbit=null,deer=null,CR=null,""",1)
open('header2_js.txt','w').write(s)

m=open('make_compact.py').read()
a="""  if(t<simT-1e-3){if(!full){upd(t);return}resetLeaves()}
  if(full||t-simT<120){while(simT<t-1e-6)stepLeaves(Math.min(.05,t-simT),true);
   falling.forEach(f=>f.node.setAttribute('transform',`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`));rakeStep(0,false)}}"""
assert a in m
m=m.replace(a,"""  syncLeaves(full?1e9:6000)}
 snowTick();""")
m=m.replace(" if(document.body.dataset.season==='jesien'&&G&&heights){\n  syncLeaves(full?1e9:6000)}"," syncLeaves(full?1e9:6000);")
# style śniegu
m=m.replace("/* napisy widoczne od początku */",""".snowlayer{fill:#fbfcfd} .snowedge{fill:none;stroke:#b9c6d3;stroke-width:1}
.flake{fill:#fff;stroke:#c9d4de;stroke-width:.3}
/* napisy widoczne od początku */""",1)
# panel: zegar godziny + skok do końca godziny
m=m.replace("""<output id="tlv">0.0 s</output></div>""","""<output id="tlv">0.0 s</output></div><div class="scrub" style="padding-top:0"><button id="toEnd">⏩ 4 min przed pełną godziną</button><span>Zegar sceny: <output id="clk"></output> (liście i śnieg liczone od pełnej godziny)</span></div>""")
m=m.replace("(function follow(){","""document.getElementById('toEnd').onclick=()=>{const [,w]=hourPos();let d=HOUR-240-w;if(d<0)d+=HOUR;seek(now()+d,true)};
const clk=document.getElementById('clk');setInterval(()=>{const w=wall(),dt=new Date(w*1000);clk.value=dt.toLocaleTimeString('pl-PL')},250);
(function follow(){""")
open('make_compact.py','w').write(m)
print('ok')
