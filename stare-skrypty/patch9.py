s=open('header2_js.txt').read()
R=[
# --- liście pamiętają swój węzeł DOM (do grabienia) ---
(" leafPile.appendChild(leafEl(bb*BIN,groundY-L.h,L.rot,L.c,L.s*k))}"," L.node=leafEl(bb*BIN,groundY-L.h,L.rot,L.c,L.s*k);leafPile.appendChild(L.node)}"),
(" settled.forEach(l=>leafPile.appendChild(leafEl(l.fx*W,groundY-l.h,l.rot,l.c,l.s*k)));"," settled.forEach(l=>{l.node=leafEl(l.fx*W,groundY-l.h,l.rot,l.c,l.s*k);leafPile.appendChild(l.node)});"),
# --- koniec kroku liści: ksiądz z grabiami ---
("  if(!fast)f.node.setAttribute('transform',`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`)}\n}",
 "  if(!fast)f.node.setAttribute('transform',`translate(${f.x.toFixed(1)} ${f.y.toFixed(1)}) rotate(${f.rot.toFixed(0)})`)}\n rakeStep(dt,fast)\n}"),
("function resetLeaves(){lseed=12345;simT=0;","function resetLeaves(){PR.cycle=0;PR.active=false;lseed=12345;simT=0;"),
# --- warstwa liści: ksiądz ---
("leafFall=el('g');leafPile=el('g');lv.appendChild(leafPile);lv.appendChild(leafFall);front.appendChild(lv);",
 "leafFall=el('g');leafPile=el('g');lv.appendChild(leafPile);lv.appendChild(leafFall);front.appendChild(lv);\n priestG=makePriest(lv);rakeStep(0,false);"),
# --- turyści (lato) ---
(" front.appendChild(zoo);\n CR={W,groundY,k:k*1.05};critterTick();",
 " front.appendChild(zoo);\n const tour=el('g',{class:'deco only-lato tourists'});front.appendChild(tour);tourists=[['#c0503a','#2f5d7a'],['#2f6a55','#d9892e'],['#3f6a8c','#8a3a3a']].map(([c,pk],i)=>makeTourist(tour,c,pk,i));\n CR={W,groundY,k:k*1.05,H,topBack,sceneW,mobile};critterTick();"),
]
for a,b in R:
    assert s.count(a)==1,(s.count(a),a[:70]); s=s.replace(a,b)

# --- nowe funkcje: ksiądz i turyści ---
s=s.replace("let rabbit=null,deer=null,CR=null;",r"""let rabbit=null,deer=null,CR=null,tourists=[],priestG=null;
const PR={cycle:0,active:false,x:-40,acc:0,raking:false};
// JESIEŃ: co godzinę przychodzi ksiądz z grabiami i sprząta wszystkie liście
function makePriest(par){const p=person(par,'#1f1f1f',{hair:'#6a6a6a'});
 E('rect',{fill:'#fff',x:-1.3,y:-20.6,width:2.6,height:1.4},p);
 p.rake=E('g',{},p);E('path',{class:'fi',d:'M3.6,-15 L15,0'},p.rake);E('path',{class:'fi',d:'M12,0.4 L18.4,-1.6 M12.6,0.2 l-.6,1.8 M14.2,-.3 l-.6,1.8 M15.8,-.8 l-.6,1.8 M17.4,-1.3 l-.6,1.8'},p.rake);
 p.armsDown.setAttribute('d','M-3.2,-17 L4.6,-13.6 M3.2,-17 L7,-10.6');p.style.display='none';return p}
function rakeStep(dt,fast){if(!G||!heights)return;const {W,groundY,k}=G,cyc=Math.floor(simT/3600);
 if(cyc>=1&&PR.cycle!==cyc){PR.cycle=cyc;PR.active=true;PR.x=-40;PR.acc=0}
 if(!PR.active){if(priestG)priestG.style.display='none';return}
 const reach=PR.x+14*k,R=9*k,near=[];for(const L of settled)if(Math.abs(L.fx*W-reach)<R)near.push(L);
 if(near.length){PR.raking=true;PR.acc+=dt*24;
  while(PR.acc>=1&&near.length){PR.acc-=1;let bi=0;for(let q=1;q<near.length;q++)if(near[q].h>near[bi].h)bi=q;
   const L=near.splice(bi,1)[0];settled.splice(settled.indexOf(L),1);L.node&&L.node.remove();
   const b=Math.round(L.fx*W/BIN);heights[b]=Math.max(0,heights[b]-1.3*k*L.s);if(b>0)heights[b-1]=Math.max(0,heights[b-1]-.5*k);if(b<heights.length-1)heights[b+1]=Math.max(0,heights[b+1]-.5*k)}}
 else{PR.raking=false;PR.acc=0;PR.x+=dt*36*k;const b0=Math.max(0,Math.round((reach-R)/BIN)),b1=Math.min(heights.length-1,Math.round((reach+R)/BIN));for(let b=b0;b<=b1;b++)heights[b]=0}
 if(PR.x>W+40)PR.active=false;
 if(!fast&&priestG){priestG.style.display=PR.active?'':'none';const s=k*1.15;
  priestG.setAttribute('transform',`translate(${PR.x.toFixed(1)} ${groundY.toFixed(1)}) scale(${s} ${s})`);
  if(PR.raking){walkLegs(priestG,0);priestG.rake.setAttribute('transform',`rotate(${(Math.sin(simT*7)*14).toFixed(1)} 3.6 -15)`)}
  else{walkLegs(priestG,PR.x/s);priestG.rake.setAttribute('transform','')}}}
// LATO: turyści z wielkimi plecakami schodzą z gór do kościoła i go oglądają
function makeTourist(par,c,pk,i){const g=el('g',{class:'tourist'});par.appendChild(g);
 E('rect',{class:'ff',fill:'#c9b26a',x:-11,y:-30.4,width:8.6,height:3.4,rx:1.7},g);
 E('rect',{class:'ff',fill:pk,x:-10.2,y:-27.4,width:7,height:17,rx:2},g);E('path',{class:'thin',d:'M-10,-20 h6.6 M-8.8,-24 v-3'},g);
 const p=person(g,c,i===1?{hair:'#5a3a22'}:{});g.p=p;
 E('path',{class:'ff',fill:i===2?'#e2b43c':'#6b7a3a',d:'M-3.4,-24.6 Q-3,-27.4 0,-27.4 Q3,-27.4 3.4,-24.6 L5.6,-24.4 L5.4,-23.6 L-3.4,-23.8 Z'},g);
 E('path',{class:'thin',d:'M-3,-19 L-4,-12'},g);
 g.pole=E('path',{class:'fi',d:'M5,-11 L8.4,0'},g);
 if(i===0){g.cam=E('rect',{class:'ff',fill:'#333',x:2.6,y:-24.2,width:3.4,height:2.4,rx:.4,style:'display:none'},g);g.flash=E('circle',{cx:6.4,cy:-23.6,r:4,fill:'url(#whiteglow)',style:'display:none'},g)}
 g.style.display='none';return g}
function tourTick(t){if(!CR||!tourists.length)return;const {W,groundY,k,H,topBack,sceneW,mobile}=CR;
 const P=95,n=Math.floor(t/P),off=n===0?14:6+hsh(n+9)*25,u=t-n*P-off,rb=x=>ridgeY(x+W*.37,W,H,topBack,.06);
 const xa=W*(mobile?.86:.9),xb=W*(mobile?.76:.82),xc=mobile?W*.6:(W+sceneW)/2-sceneW*.16,sF=k*.5,sN=k*1.1,vA=14*k,vC=30*k,tA=(W+30-xa)/vA,tB=6;
 tourists.forEach((g,i)=>{const r=u-i*1.7,xs=xc+i*12*k,tC=(xb-xs)/vC,tD=9,tE=(xs+40)/vC,p=g.p;
  if(r<0||r>tA+tB+tC+tD+tE){g.style.display='none';return}g.style.display='';
  let x,y,s,lean=0,dist,stand=false;p.armsUp.style.display='none';p.armsDown.style.display='';if(g.cam){g.cam.style.display='none';g.flash.style.display='none'}
  if(r<tA){x=W+30-vA*r;y=rb(x);s=sF;dist=r*vA/sF}
  else if(r<tA+tB){const q=(r-tA)/tB,e=q*q*(3-2*q);x=xa+(xb-xa)*q;y=rb(xa)+(groundY-rb(xa))*e;s=sF+(sN-sF)*e;dist=(tA*vA/sF)+q*40}
  else if(r<tA+tB+tC){x=xb-vC*(r-tA-tB);y=groundY;s=sN;dist=x/s}
  else if(r<tA+tB+tC+tD){const w=r-tA-tB-tC;x=xs;y=groundY;s=sN;stand=true;lean=-Math.min(1,w/.8,(tD-w)/.8)*8;
   if(i===1&&w>2&&w<6){p.armsUp.setAttribute('d','M-3.2,-17 L-5,-10 M3.2,-17 L8,-23');p.armsUp.style.display='';p.armsDown.style.display='none'}
   if(g.cam&&w>3&&w<7){g.cam.style.display='';g.flash.style.display=(w>5&&w<5.25)?'':'none'}}
  else{x=xs-vC*(r-tA-tB-tC-tD);y=groundY;s=sN;dist=x/s}
  walkLegs(p,stand?0:dist);g.pole.setAttribute('transform',stand?'':`rotate(${(Math.sin(dist/3.2)*8).toFixed(1)} 5 -11)`);
  g.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${-s} ${s}) rotate(${lean.toFixed(1)})`)})}""",1)
s=s.replace("function critterTick(){\n if(!CR||!rabbit)return;","function critterTick(){\n tourTick(now());\n if(!CR||!rabbit)return;",1)
open('header2_js.txt','w').write(s)
print('ok')
