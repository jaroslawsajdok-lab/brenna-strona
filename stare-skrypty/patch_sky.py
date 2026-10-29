s=open('header2_js.txt').read()
i=s.index(" // słońce (lato)"); j=s.index(" // chmury")
s=s[:i]+r""" // słońce (lato) i księżyc (zima) – wędrują po niebie, pozycję liczy tick()
 const sr=20*k,mr=15*k;
 const sd=el('defs');
 [['sunhalo','#ffd27a',.55],['moonhalo','#fff2c9',.35]].forEach(([id,c,o])=>{const g=el('radialGradient',{id});
  g.appendChild(el('stop',{offset:0,'stop-color':c,'stop-opacity':o}));g.appendChild(el('stop',{offset:1,'stop-color':c,'stop-opacity':0}));sd.appendChild(g)});
 land.appendChild(sd);
 sunG=el('g',{class:'deco only-lato'});
 sunG.appendChild(el('circle',{r:sr*3.4,fill:'url(#sunhalo)'}));
 sunRays=el('g');
 for(let i=0;i<16;i++){const a=i*Math.PI/8,r1=sr*1.35,r2=sr*(i%2?1.7:1.95);
  sunRays.appendChild(el('line',{class:'ray',x1:Math.cos(a)*r1,y1:Math.sin(a)*r1,x2:Math.cos(a)*r2,y2:Math.sin(a)*r2}))}
 sunG.appendChild(sunRays);sunDisc=el('circle',{class:'sun',r:sr});sunG.appendChild(sunDisc);land.appendChild(sunG);
 moonG=el('g',{class:'deco only-zima'});
 moonG.appendChild(el('circle',{r:mr*3.2,fill:'url(#moonhalo)'}));
 moonG.appendChild(el('path',{class:'moon',d:`M${mr*.2},${-mr} A${mr},${mr} 0 1 0 ${mr*.2},${mr} A${mr*1.25},${mr*1.25} 0 0 1 ${mr*.2},${-mr} Z`}));
 land.appendChild(moonG);
 SKY={W,H,yH:H*.6,yT:H*(mobile?.17:.15),r:sr};
 skyTick(performance.now());

"""+s[j:]

s=s.replace("let first=true,chairs=[],liftPath=null,raf=0;","""let first=true,chairs=[],liftPath=null,raf=0;
// --- słońce, księżyc i kolory nieba ---
let SKY=null,sunG,sunRays,sunDisc,moonG,skyDirty=false,lastSkyPaint=0;
const DAY=150,NIGHT=180,VIS=.88;            // długość cyklu w sekundach; VIS = część cyklu nad horyzontem
const hx=h=>[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)),mix=(a,b,t)=>{const A=hx(a),B=hx(b);return 'rgb('+A.map((v,i)=>Math.round(v+(B[i]-v)*t)).join(',')+')'};
const SKYK=[[0,'#5b5a8f','#f4a46a'],[.06,'#7f8fc0','#f8c48e'],[.16,'#a9cde6','#eef0ea'],[.44,'#bfdcee','#eef3f0'],
 [.72,'#a9cde6','#f1e8d6'],[.81,'#7c6aa8','#f39a5c'],[.88,'#4b3f7c','#e8706a'],[.94,'#2d3160','#9a5c86'],[.97,'#2a2f58','#7d6a92'],[1,'#5b5a8f','#f4a46a']];
function skyAt(ph){let i=0;while(i<SKYK.length-2&&ph>SKYK[i+1][0])i++;const [a,t1,h1]=SKYK[i],[b,t2,h2]=SKYK[i+1],t=(ph-a)/(b-a);
 return [mix(t1,t2,t),mix(h1,h2,t)]}
function arc(p){const {W,yH,yT,r}=SKY;return [-r*3+(W+r*6)*p, yH-(yH-yT)*Math.sin(Math.PI*p)]}
function skyTick(ts){
 if(!SKY)return;const season=document.body.dataset.season,t=ts/1000,skyEl=document.getElementById('sky');
 if(season==='lato'){
  const ph=reduce?.36:(t/DAY)%1,p=ph/VIS,[x,y]=ph<VIS?arc(p):[-999,-999];
  sunG.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)})`);
  sunRays.setAttribute('transform',`rotate(${((t*4.5)%360).toFixed(1)})`);
  const hi=ph<VIS?Math.min(1,Math.sin(Math.PI*p)*2.4):0;            // nisko nad horyzontem = cieplejsze
  sunDisc.style.fill=mix('#ff9f4a','#f7dc85',hi);sunRays.style.stroke=mix('#e0682e','#d9a62e',hi);
  if(ts-lastSkyPaint>80||reduce){lastSkyPaint=ts;const [top,hor]=skyAt(ph);
   skyEl.style.background=`linear-gradient(to bottom,${top} 0%,${mix(top.replace(/rgb\\(|\\)/g,'').split(',').map(v=>(+v).toString(16).padStart(2,'0')).reduce((a,v)=>a+v,'#'),hor.replace(/rgb\\(|\\)/g,'').split(',').map(v=>(+v).toString(16).padStart(2,'0')).reduce((a,v)=>a+v,'#'),.5)} 24%,${hor} 44%,color-mix(in srgb,${hor} 45%,transparent) 62%,transparent 80%)`;
   skyDirty=true}
 }else if(skyDirty){skyEl.style.background='';skyDirty=false}
 if(season==='zima'){
  const ph=reduce?.42:((t+NIGHT*.02)/NIGHT)%1,p=ph/VIS,[x,y]=ph<VIS?arc(p):[-999,-999];
  moonG.setAttribute('transform',`translate(${x.toFixed(1)} ${y.toFixed(1)}) rotate(${(-25+50*p).toFixed(1)})`);
 }
}""")
s=s.replace("function tick(ts){\n","function tick(ts){\n skyTick(ts);\n",1)
open('header2_js.txt','w').write(s)
print('ok')
