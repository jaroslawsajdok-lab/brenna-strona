s=open('header2_js.txt').read()
i=s.index(" // KRÓLIK:"); j=s.index("\n}\nlet scrubbed=false")
new=r""" // ZAJĄC: raz na ok. 35 s przebiega przez stronę; mniej więcej co drugi raz przysiada po drodze i się rozgląda
 {const P=35,v=Math.max(150,W/6.5),n=Math.floor(t/P),stops=n===0||hsh(n+1.7)<.55,
   sx=.22+hsh(n+2.3)*.56,sd=stops?1.6+hsh(n+4.1)*1.6:0,run=(W+120)/v,dur=run+sd,
   off=n===0?9:4+hsh(n)*Math.max(0,P-dur-6),u=t-n*P-off;
  if(u<0||u>dur){rabbit.style.display='none'}else{
   const dir=n===0||hsh(n+.5)<.6?1:-1,s=k*1.5,hop=.4;
   const ts=sx*run;                                    // chwila, w której zając dobiega do miejsca przystanku
   let d,sit=false,w=0;
   if(u<ts||!stops)d=v*u;else if(u<ts+sd){d=v*ts;sit=true;w=u-ts}else d=v*(u-sd);
   const x=dir>0?-60+d:W+60-d;
   rabbit.style.display='';
   if(sit){                                           // siedzi: skulony, uszy w górę, krótkie strzygnięcie i obrót głowy
    show(rabbit.pA,false);show(rabbit.pB,true);
    const look=(w>.4&&w<sd-.5)?Math.sin(Math.min(1,(w-.4)/.25)*Math.PI/2)*Math.min(1,(sd-.5-w)/.25):0;
    rabbit.setAttribute('transform',`translate(${x.toFixed(1)} ${groundY.toFixed(1)}) scale(${dir*s} ${s}) rotate(${(-6*look).toFixed(1)})`)}
   else{const uu=u<ts||!stops?u:u-sd,ph=(uu%hop)/hop,air=Math.sin(Math.PI*ph);
    show(rabbit.pA,air>.35);show(rabbit.pB,air<=.35);
    rabbit.setAttribute('transform',`translate(${x.toFixed(1)} ${(groundY-air*9*k).toFixed(1)}) scale(${dir*s} ${s}) rotate(${((ph-.5)*-14).toFixed(1)})`)}}}
 // SARENKA: raz na ok. 55 s wbiega, staje w pół drogi, nasłuchuje i ucieka długimi susami
 {const P=55,n=Math.floor(t/P),off=n===0?20:6+hsh(n+3)*30,u=t-n*P-off,dir=n%2===0?1:-1;
  const x0=dir>0?-70:W+70,xs=dir>0?W*.3:W*.7,v=Math.max(140,W/8.5),T1=Math.abs(xs-x0)/v*1.35,T2=3.6,T3=Math.abs(xs-x0)/(v*1.6)*1.15;
  if(u<0||u>T1+T2+T3){deer.style.display='none'}else{
   deer.style.display='';const s=k*1.2;let x,face=dir,pose='S',bob=0,head=0,ear=0,tilt=0;
   // krok galopu liczony w czasie: faza lotu (nogi wyciągnięte) i lądowania (nogi pod sobą)
   const gait=(tt,stride,leap)=>{const ph=(tt%stride)/stride,airF=.58;
    if(ph<airF){const a=ph/airF;pose='A';bob=Math.sin(Math.PI*a)*leap;tilt=(a-.5)*-12}else{pose='B';bob=0;tilt=4}};
   if(u<T1){const q=u/T1,e=1-(1-q)*(1-q);x=x0+(xs-x0)*e;const sp=2*(1-q);
    if(sp>.45)gait(u,.5,4.5*Math.min(1,sp));else{pose='S'}}
   else if(u<T1+T2){x=xs;const w=u-T1;head=w>.5&&w<2.7?-24*Math.min(1,(w-.5)/.35,(2.7-w)/.35):0;ear=(w>1.6&&w<1.8)||(w>2.9&&w<3.05)?-18:0}
   else{const q=(u-T1-T2)/T3,e=Math.pow(q,1.25);x=xs+(x0-xs)*e;face=-dir;gait(u-T1-T2,.56,8)}
   show(deer.pS,pose==='S');show(deer.pA,pose==='A');show(deer.pB,pose==='B');
   deer.head.setAttribute('transform',`rotate(${head})`);deer.ears.setAttribute('transform',`rotate(${ear})`);
   deer.setAttribute('transform',`translate(${x.toFixed(1)} ${(groundY-bob*k).toFixed(1)}) scale(${face*s} ${s}) rotate(${tilt.toFixed(1)})`)}}"""
s=s[:i]+new+s[j:]
open('header2_js.txt','w').write(s)
print('ok')
