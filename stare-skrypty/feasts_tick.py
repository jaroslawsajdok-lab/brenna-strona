s=open('feasts_js.txt').read()
i=s.index("// ---------- ruch scen (wywoływany co klatkę) ----------");j=s.index("// ---------- podgląd: wybór daty ----------")
new=r"""// ---------- ruch scen (wywoływany co klatkę) ----------
const bowC=p=>p<.25?Math.sin(p/.25*Math.PI/2):p<.55?1:p<.75?Math.cos((p-.55)/.2*Math.PI/2):0;   // pokłon: w dół, chwila, w górę, przerwa
function feastTick(){if(!FEAST||!LY)return;const t=now(),T=tau(),{W,H,groundY,k,sceneW,mobile,th}=LY,door=W/2-sceneW*.12;
 const sP=Math.min(1.3,th/50*1.2)*(mobile?.6:1);
 // Królowie: karawana idzie grzbietem od wschodu i znika za zboczem
 if(FX.magi){const P=80,u=((T%P)+P)%P,v=22*k,s=k*1.05,xd=(W+sceneW)/2+10,rb=x=>ridgeY(x+W*.37,W,H,LY.topBack,.06);
  FX.magi.figs.forEach((f,i)=>{const dd=v*u-i*15*s;if(T<0||dd<0){f.style.display='none';return}f.style.display='';
   const x=W+30-dd;let y=x>xd?rb(x):rb(xd)+(xd-x)*.6;const bob=Math.abs(Math.sin(dd/5))*1.3;
   if(f.lA){const st=Math.floor(dd/6)%2;f.lA.style.display=st?'none':'';f.lB.style.display=st?'':'none'}
   f.setAttribute('transform',`translate(${x.toFixed(1)} ${(y-bob).toFixed(1)}) scale(${(-s).toFixed(2)} ${s.toFixed(2)}) rotate(${(Math.sin(dd/5)*2).toFixed(1)})`)})}
 // stajenka: Maryja kołysze się nad żłobkiem, zwierzęta, owce, anioł; 6.01 wszyscy się kłaniają
 if(FX.nat){const N=FX.nat;
  N.mary.setAttribute('transform',`rotate(${(Math.sin(t*1.1)*3.5).toFixed(2)} -18 0)`);
  N.halo.setAttribute('r',(7+Math.sin(t*1.4)*1.4).toFixed(2));N.warm.style.opacity=(.85+Math.sin(t*1.9)*.15).toFixed(2);
  const bw=N.epi?bowC(((t*.16)%1+1)%1):0;
  N.ox.setAttribute('transform',N.epi?`rotate(${(bw*18).toFixed(1)} -24 -28)`:`translate(0 ${(Math.abs(Math.sin(t*1.8))*.9).toFixed(2)})`);
  N.don.setAttribute('transform',N.epi?`rotate(${(-bw*18).toFixed(1)} 24 -28)`:'');N.ear.setAttribute('transform',(t%5.3)<.3?'rotate(-18 25 -33)':'');
  N.sheep.forEach(([sp,hd,i])=>{const wx=+sp.dataset.x+Math.sin(t*.13+i*2.1)*3,b2=N.epi?bowC(((t*.16+.1*i)%1+1)%1):0;
   sp.setAttribute('transform',`translate(${wx.toFixed(1)} ${sp.dataset.y}) rotate(${(b2*10).toFixed(1)})`);
   hd.setAttribute('transform',`translate(0 ${(N.epi?b2*2.6:Math.max(0,Math.sin(t*.7+i*1.7))*2.2).toFixed(2)})`)});
  N.bow.forEach(([g,x,ph,deg])=>{const b=N.epi?bowC(((t*.16+ph*.1)%1+1)%1):0;g.setAttribute('transform',`translate(${x} 0) rotate(${(b*deg).toFixed(1)})`)});
  const A=N.angel,ua=((T%38)+38)%38,op=T<0?0:ua<3?ua/3:ua<16?1:ua<19?(19-ua)/3:0;A.style.opacity=op.toFixed(2);
  A.setAttribute('transform',`translate(${(Math.sin(t*.5)*6).toFixed(1)} ${(-74+Math.sin(t*1.3)*2).toFixed(1)})`);
  const fl=(.35+.65*Math.abs(Math.sin(t*4))).toFixed(2);N.wl.setAttribute('transform',`scale(1 ${fl})`);N.wr.setAttribute('transform',`scale(1 ${fl})`)}
 // Niedziela Palmowa
 if(FX.palm){const Pm=FX.palm,P=80,n=Math.floor(T/P),u=T-n*P,v=15*k,xs=W+30,xr=xs-v*u,rd=Pm.rider;
  if(T<0){rd.style.display='none';Pm.crowd.forEach(p=>{p.style.display='none';p.leaf&&(p.leaf.style.display='none')})}
  else{rd.style.display='';const op=xr>door?1:Math.max(0,1-(door-xr)/(30*k));rd.style.opacity=op.toFixed(2);
   const st=Math.floor(v*u/5)%2;rd.lA.style.display=st?'none':'';rd.lB.style.display=st?'':'none';
   put(rd,xr,groundY-Math.abs(Math.sin(v*u/5*Math.PI))*.8,-1,sP);
   Pm.crowd.forEach((p,i)=>{if(mobile&&i>1){p.style.display='none';return}p.style.display='';const face=xr>p.xf?1:-1;
    put(p,p.xf,groundY,face,sP);p.fr.setAttribute('transform',`translate(6 -24) rotate(${(Math.sin(t*4+i*1.3)*25).toFixed(0)})`);
    if(!p.leaf){p.leaf=E('g',{class:'nodraw'},Pm.laid);frondSmall(p.leaf,13)}
    const tt=(xs-(p.xf+28*sP))/v,xl=p.xf-14*sP;                       // rzut gałązki przed osiołka
    if(u<tt){p.leaf.style.display='none'}else{p.leaf.style.display='';const q=Math.min(1,(u-tt)/.9),x=p.xf+(xl-p.xf)*q,y=groundY-24*sP*(1-q)-Math.sin(q*Math.PI)*14*sP;
     p.leaf.setAttribute('transform',`translate(${x.toFixed(1)} ${(y-1).toFixed(1)}) scale(${sP.toFixed(2)}) rotate(${(-80*q+(1-q)*20).toFixed(0)})`)}})}}
 // Wielkanoc: kobiety idą do grobu, zaglądają, zdumione biegną z radością z powrotem
 if(FX.easter){const Eo=FX.easter,P=60,n=Math.floor(T/P),u=T-n*P,tombX=Eo.px-24*Eo.sc,vw=26*k,vr=72*k;
  Eo.women.forEach((w,i)=>{const r=u-i*1.3,xt=tombX-i*9*sP,Tw=(xt-door)/vw;w.armsUp.style.display='none';w.armsDown.style.display='';
   if(T<0||r<0){w.style.display='none';return}w.style.display='';w.style.opacity=1;
   if(r<Tw){const x=door+vw*r;w.style.opacity=Math.min(1,r).toFixed(2);put(w,x,groundY,1,sP);walkLegs(w,r*vw/sP)}
   else if(r<Tw+3){put(w,xt,groundY,1,sP,Math.min(1,(r-Tw)/.6)*14);walkLegs(w,0)}
   else if(r<Tw+4.4){const j=Math.abs(Math.sin((r-Tw-3)*Math.PI*2.2));put(w,xt,groundY-j*5*sP,1,sP);w.armsUp.style.display='';w.armsDown.style.display='none'}
   else{const x=xt-vr*(r-Tw-4.4);if(x<door-20*k){w.style.display='none';return}
    const j=Math.abs(Math.sin((r-Tw-4.4)*Math.PI*2.6));put(w,x,groundY-j*6*sP,-1,sP);w.armsUp.style.display='';w.armsDown.style.display='none';walkLegs(w,(r-Tw)*vr/sP);
    w.style.opacity=Math.min(1,Math.max(0,(x-door+20*k)/(20*k))).toFixed(2)}});
  if(FX.angelE)FX.angelE.setAttribute('transform',`translate(25 ${(-22+Math.sin(t*1.2)*.8).toFixed(2)})`)}
 // Zielone Świątki: gołębica nadlatuje, ogniste języki spływają nad głowy, ludzie się radują
 if(FX.pent){const Pn=FX.pent,P=46,n=Math.floor(T/P),u=T-n*P,hx=Mobile=>0,hoverX=mobile?W*.66:Pn.px,hoverY=H*.2;
  Pn.people.forEach((p,i)=>{if(T<0){p.style.display='none';return}p.style.display='';put(p,Pn.px+p.xo*Pn.sc,groundY,i<2?1:-1,sP)});
  let dx,dy,vis=true;
  if(T<0||u>38)vis=false;else if(u<12){const q=1-Math.pow(1-u/12,2);dx=-30+(hoverX+30)*q;dy=hoverY-30+30*q}
  else if(u<30){const w=u-12;dx=hoverX+Math.sin(w*.8)*14;dy=hoverY+Math.sin(w*1.6)*5}
  else{const q=(u-30)/8;dx=hoverX+(W+40-hoverX)*q*q;dy=hoverY-H*.15*q}
  const D=FX.dove;D.style.display=vis?'':'none';
  if(vis){D.setAttribute('transform',`translate(${dx.toFixed(1)} ${dy.toFixed(1)}) scale(${(-1)*k*1.7} ${k*1.7})`);
   D.w1.setAttribute('transform',`scale(1 ${(.35+.65*Math.abs(Math.sin(t*7))).toFixed(2)})`);D.w2.setAttribute('transform',`scale(1 ${(.3+.7*Math.abs(Math.sin(t*7+.4))).toFixed(2)})`)}
  Pn.flames.forEach((fl,i)=>{const p=Pn.people[i],hxp=Pn.px+p.xo*Pn.sc,hy=groundY-31*sP,t0=13+i*.45,t1=t0+2.6;
   if(T<0||u<t0||u>44){fl.style.display='none';p.armsUp.style.display='none';p.armsDown.style.display='';return}fl.style.display='';
   let x,y;if(u<t1){const q=(u-t0)/(t1-t0),e=q*q*(3-2*q);x=hoverX+(hxp-hoverX)*e;y=hoverY+8+(hy-hoverY-8)*e}else{x=hxp;y=hy}
   const fz=(1+Math.sin(t*9+i)*.12)*sP*1.25;fl.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) scale(${fz.toFixed(2)} ${(fz*(1+Math.sin(t*7+i*2)*.15)).toFixed(2)})`);
   fl.style.opacity=u>41?((44-u)/3).toFixed(2):1;
   const joy=u>=t1&&u<t1+5;p.armsUp.style.display=joy?'':'none';p.armsDown.style.display=joy?'none':''})}
 if(FX.ref)refTick(T)}

"""
s=s[:i]+new+s[j:]
# Reformacja: przed narysowaniem sceny nikogo nie ma
a="function refTick(t){const R=FX.ref;if(!R)return;"
assert a in s
s=s.replace(a,"function refTick(t){const R=FX.ref;if(!R)return;if(t<0){R.lp.style.display='none';R.P.forEach(p=>p.style.display='none');R.paper.style.display='none';return}")
open('feasts_js.txt','w').write(s)
print('ok')
