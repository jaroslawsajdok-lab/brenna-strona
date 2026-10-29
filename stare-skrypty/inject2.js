(()=>{document.querySelectorAll('#pvwrap').forEach(e=>e.remove());const sty=document.createElement('style');sty.textContent="/* ===== przegl\u0105darka spaceru 360\u00b0 ===== */\n.pv{position:relative;overflow:hidden;user-select:none;-webkit-user-select:none;background:#d9d4c7;outline:none}\n.pv-view{position:absolute;inset:0;overflow:hidden;cursor:grab;touch-action:none}\n.pv-view:active{cursor:grabbing}\n.pv-cam{position:absolute;left:50%;top:50%;width:0;height:0;transform-style:preserve-3d}\n.pv-stage,.pv-cube{position:absolute;transform-style:preserve-3d}\n.pv-cube{transition:opacity .6s ease}\n.pv-face{position:absolute;left:-512px;top:-512px;width:1024px;height:1024px;backface-visibility:hidden;transform-style:preserve-3d}\n.pv-face img{position:absolute;display:block;max-width:none;pointer-events:none}\n.pv-hot{position:absolute;inset:0;pointer-events:none;perspective:600px}\n.pv-spot{position:absolute;left:0;top:0;width:58px;height:58px;padding:0;border:0;background:none;cursor:pointer;pointer-events:auto}\n.pv-spot svg{width:100%;height:100%;overflow:visible}\n.pv-spot circle{fill:rgba(247,245,239,.78);stroke:#1d1d1b;stroke-width:1.6}\n.pv-spot path{fill:none;stroke:#2f5d45;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}\n.pv-spot:hover circle,.pv-spot:focus-visible circle{fill:#2f5d45}\n.pv-spot:hover path,.pv-spot:focus-visible path{stroke:#fff}\n.pv-ui{position:absolute;inset:0;pointer-events:none}\n.pv-ui button{pointer-events:auto;cursor:pointer;font:inherit;color:#1d1d1b}\n.pv-ui svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}\n.pv-b{position:absolute;top:50%;width:46px;height:46px;margin-top:-23px;border-radius:50%;border:1.6px solid #1d1d1b;background:rgba(247,245,239,.92);display:grid;place-items:center;padding:0}\n.pv-prev{left:5%}.pv-next{right:5%}\n.pv-b:hover,.pv-s:hover{background:#2f5d45;color:#fff;border-color:#2f5d45}\n.pv-bar{pointer-events:auto;position:absolute;left:50%;bottom:7%;transform:translateX(-50%);display:flex;align-items:center;gap:2px;padding:4px;border:1.6px solid #1d1d1b;border-radius:40px;background:rgba(247,245,239,.94)}\n.pv-s{width:38px;height:38px;border-radius:50%;border:0;background:transparent;display:grid;place-items:center;padding:0}\n.pv-s svg{width:19px;height:19px}\n.pv-n{min-width:52px;text-align:center;font-size:13px;font-weight:700;font-variant-numeric:tabular-nums;color:#1d1d1b}\n.pv-ui button:focus-visible,.pv-spot:focus-visible{outline:2px solid #2f5d45;outline-offset:2px}\n/* pe\u0142ny ekran: okno staje si\u0119 prostok\u0105tem na ca\u0142y ekran, sterowanie wi\u0119ksze */\n.pv-full{width:100vw!important;height:100vh!important;border-radius:0!important;background:#1d1d1b}\n.pv-full .rose-in,.pv-full.rose-in{inset:0!important;border-radius:0!important}\n.pv-full .tracery,.pv-full figcaption{display:none!important}\n.pv-full .pv-bar{bottom:28px;transform:translateX(-50%) scale(1.2)}\n.pv-full .pv-b{width:56px;height:56px;margin-top:-28px}\n.pv-full .pv-prev{left:24px}.pv-full .pv-next{right:24px}\n\n.pv-busy .pv-n{opacity:.45}\n.pv-busy .pv-view::after{content:\"\";position:absolute;left:50%;top:50%;width:34px;height:34px;margin:-17px;border:2px solid rgba(247,245,239,.9);border-top-color:transparent;border-radius:50%;animation:pvspin .8s linear infinite}\n@keyframes pvspin{to{transform:rotate(360deg)}}\n#pvwrap{position:fixed;left:30px;top:30px;width:520px;height:520px;z-index:99999;border-radius:50%;overflow:hidden}";document.head.appendChild(sty);const host=document.createElement('div');host.id='pvwrap';document.body.appendChild(host);
// =====================================================================
// Przeglądarka spaceru 360° (CSS 3D, sześcian 3DVista) – własne sterowanie
// Nie wymaga WebGL ani nagłówków CORS: kafelki to zwykłe <img>.
// =====================================================================
const PANO_BASE='https://luteranie-wirtualne-muzea.pl/wirtualnyspacer/brenna/media/';
const PANO_VER='?v=1789060995726';
// [id, [[cel, kierunek, kierunek powrotny, wysokość strzałki], ...]] – kolejność jak w wycieczce
const PANOS=[
['8A3A634C_848B_252C_41C4_04A259C7237F',[['891A7F6C',172,0,15],['891A419B',-51,37,23],['891A1A07',-98,71,-64],['891A0B03',57,-93,-57],['891AB3F1',-6,148,-46],['891C0F2F',-28,117,-33]]],
['891A7F6C_848B_5DEC_41A5_9A556F7B6CD2',[['8919FB89',174,-2,15],['8A3A634C',0,172,19]]],
['8919FB89_848B_6514_41E0_813F523A4C82',[['891A7F6C',-2,174,4]]],
['891A17C8_848B_6D13_41D9_97F771125812',[['891A419B',-1,-90,7]]],
['891A419B_848B_2534_41D6_0571E38A8FA4',[['891A17C8',-90,-1,15],['8A3A634C',37,-51,14]]],
['891A1A07_848B_271C_41C8_2A2548A1E867',[['891A0B03',60,-90,-7],['891AB3F1',-2,180,-3],['8A3A634C',71,-98,53],['891C0F2F',-30,98,-6]]],
['891A0B03_848B_E515_41DF_D10B4FE69AFB',[['891A1A07',-90,60,-10],['8A3A634C',-93,57,52],['891AB3F1',-21,130,-5]]],
['891AB3F1_848B_E4F4_41D6_C82B1900794B',[['891A1A07',180,-2,-12],['891A0B03',130,-21,-12],['8A3A634C',148,-6,38],['891ADC76',-3,-179,-7]]],
['891ADC76_848B_E3FF_41DC_89B9FFE48EC0',[['891CFC22',145,38,-1],['891AB3F1',-179,-3,-1],['891B952F',1,173,-13]]],
['891B952F_848B_2D6D_41B1_A65B31943C6B',[['891B5951',-150,159,22],['891ADC76',173,1,-11],['891BF706',-88,20,-15],['891B9E0A',75,-45,-19]]],
['891B9E0A_848B_3F17_41C5_EB3B55C2DF76',[['891B952F',-45,75,-22],['891BEFF1',-76,0,18]]],
['891BF706_848B_2D1C_41D2_0205E751F28B',[['891C9347',78,0,8],['891B952F',20,-88,-15]]],
['891BEFF1_848B_5CF5_41D5_10B629B18628',[['891B5951',-88,-84,-8],['891C9347',-173,49,-6],['891CFC22',123,-139,-35],['891B952F',-7,0,-21]]],
['891B5951_848B_6535_41D6_0B9297C02777',[['891B952F',159,-150,-26],['891BEFF1',-84,-88,-16]]],
['891C9347_848B_651D_419E_B71DB87A78B7',[['891B5951',-27,0,-18],['891B952F',18,0,-24],['891BEFF1',49,-173,-30]]],
['891CFC22_848B_6317_41C2_72028573452C',[['891B3478',152,-167,-35],['891ADC76',38,145,-21],['891BEFF1',-139,123,-3]]],
['891B3478_848B_23F3_41C5_57A63921FD8A',[['891CFC22',-167,152,-8],['891C8D0F',-23,25,-18],['891CB567',86,109,-13]]],
['891C8D0F_848B_3D2D_41D6_23F72584C060',[['891B3478',25,-23,-16]]],
['891CB567_848B_2D1C_41C7_6E67F3B4C674',[['891C7DDB',-60,99,-18],['891B3478',109,86,-29]]],
['891C7DDB_848C_DD35_41DA_79AF683F5250',[['891CB567',99,-60,-19]]],
['891C6641_848C_EF14_41C8_746752D3B00E',[['891C0F2F',43,30,-8],['8A3A634C',70,0,57]]],
['891C0F2F_848C_FD6C_41D4_2B5677CB0F18',[['891A1A07',98,-30,-6],['8A3A634C',117,-28,32],['891C6641',30,43,-2]]]];
// poziomy kafelków 3DVista: [nr poziomu, bok ściany w px, kafelków w rzędzie]
const PANO_LEVELS=[[3,512,1],[2,1024,2],[1,1536,3],[0,3072,6]];
const FACE_T={f:'rotateY(0deg)',r:'rotateY(-90deg)',b:'rotateY(180deg)',l:'rotateY(90deg)',u:'rotateX(-90deg)',d:'rotateX(90deg)'};

function mountPano(host,opt={}){
 const S=1024;                                  // rozmiar sześcianu w układzie CSS
 const st={i:0,yaw:opt.yaw??-1.6,pitch:opt.pitch??-14,hfov:96,auto:true,drag:null,vy:0,vp:0,hold:0,lvl:-1,raf:0,last:0,vis:true};
 host.classList.add('pv');host.innerHTML='';
 const view=E('div','pv-view'),cam=E('div','pv-cam'),stage=E('div','pv-stage');
 view.appendChild(cam);cam.appendChild(stage);host.appendChild(view);
 const hot=E('div','pv-hot');host.appendChild(hot);
 // sterowanie
 const ui=E('div','pv-ui');ui.innerHTML=`
  <button class="pv-b pv-prev" aria-label="Poprzedni punkt"><svg viewBox="0 0 24 24"><path d="M15 4 7 12l8 8"/></svg></button>
  <button class="pv-b pv-next" aria-label="Następny punkt"><svg viewBox="0 0 24 24"><path d="m9 4 8 8-8 8"/></svg></button>
  <div class="pv-bar" role="toolbar" aria-label="Sterowanie widokiem">
   <button class="pv-s" data-act="left" aria-label="Obróć w lewo"><svg viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v4h-4" transform="scale(-1 1) translate(-24 0)"/></svg></button>
   <button class="pv-s" data-act="out" aria-label="Oddal"><svg viewBox="0 0 24 24"><path d="M5 12h14"/></svg></button>
   <span class="pv-n" aria-live="polite"></span>
   <button class="pv-s" data-act="in" aria-label="Przybliż"><svg viewBox="0 0 24 24"><path d="M5 12h14M12 5v14"/></svg></button>
   <button class="pv-s" data-act="right" aria-label="Obróć w prawo"><svg viewBox="0 0 24 24"><path d="M20 12a8 8 0 1 1-2.3-5.6M20 4v4h-4"/></svg></button>
   <button class="pv-s pv-fs" data-act="fs" aria-label="Pełny ekran"><svg viewBox="0 0 24 24"><path d="M4 9V4h5M15 4h5v5M20 15v5h-5M9 20H4v-5"/></svg></button>
  </div>`;
 host.appendChild(ui);
 function E(t,c){const e=document.createElement(t);e.className=c;return e}

 // ----- budowa sześcianu dla bieżącego punktu -----
 // Każdy nowy sześcian jest odrobinę mniejszy od widocznego (r), więc leży bliżej kamery i zakrywa stary
 // bez migotania. Ze środka sześcianu mniejszy wygląda identycznie.
 let gen=0;
 function build(level,r){
  const id=PANOS[st.i][0],L=PANO_LEVELS[level];const cube=E('div','pv-cube');cube.dataset.r=r;
  const n=L[2],t=S/n;
  for(const f of ['f','r','b','l','u','d']){const face=E('div','pv-face');face.dataset.f=f;place(face,f,r);
   for(let rr=0;rr<n;rr++)for(let c=0;c<n;c++){const im=new Image();im.decoding='async';im.draggable=false;im.alt='';
    im.style.cssText=`left:${c*t}px;top:${rr*t}px;width:${t+.6}px;height:${t+.6}px`;im.src=`${PANO_BASE}panorama_${id}_0/${f}/${L[0]}/${rr}_${c}.webp${PANO_VER}`;face.appendChild(im)}
   cube.appendChild(face)}
  return cube}
 function place(face,f,r){face.style.transform=`${FACE_T[f]} translateZ(${-(r-.5)}px) scale(${r/512})`}
 const nextR=()=>Math.min(512,...[...stage.children].map(c=>+c.dataset.r))-3;
 function whenLoaded(cube,ms){const ims=[...cube.querySelectorAll('img')];return Promise.race([
  Promise.all(ims.map(im=>im.complete?0:new Promise(r=>{im.onload=im.onerror=r}))),new Promise(r=>setTimeout(r,ms))])}
 // po zakończonym przejściu zostaje jeden sześcian – wracamy do pełnego rozmiaru (bez zmiany obrazu)
 function settle(keep,my){setTimeout(()=>{if(my!==gen)return;[...stage.children].forEach(c=>{if(c!==keep)c.remove()});
  keep.dataset.r=512;keep.querySelectorAll('.pv-face').forEach(f=>place(f,f.dataset.f,512))},650)}
 function show(i,yaw){
  st.i=(i+PANOS.length)%PANOS.length;st.lvl=-1;const my=++gen;
  ui.querySelector('.pv-n').textContent=`${st.i+1} / ${PANOS.length}`;host.classList.add('pv-busy');
  const c=build(0,nextR());c.style.opacity=0;stage.appendChild(c);
  return whenLoaded(c,4000).then(()=>{if(my!==gen){c.remove();return}
   if(yaw!=null)st.yaw=yaw;hotspots();host.classList.remove('pv-busy');
   c.style.opacity=1;settle(c,my);upgrade();if(!st.ready){st.ready=true;opt.onReady&&opt.onReady()}})}
 // ostrzejsze kafelki, gdy okno jest duże (pełny ekran) – tylko dla aktualnego punktu
 function upgrade(){if(host.classList.contains('pv-busy'))return;const w=view.clientWidth,need=w/Math.tan(st.hfov*Math.PI/360)*(devicePixelRatio||1)*.9;
  let lv=0;while(lv<PANO_LEVELS.length-2&&PANO_LEVELS[lv][1]<need)lv++;
  if(lv<=st.lvl)return;st.lvl=lv;if(lv===0)return;const my=gen;
  const c=build(lv,nextR());c.style.opacity=0;stage.appendChild(c);
  whenLoaded(c,15000).then(()=>{if(my!==gen||!c.parentNode){c.remove();return}c.style.opacity=1;settle(c,my)})}
 // strzałki na podłodze prowadzące do sąsiednich punktów
 function hotspots(){hot.innerHTML='';PANOS[st.i][1].forEach(([to,yaw,back,pit])=>{const j=PANOS.findIndex(p=>p[0].startsWith(to));if(j<0)return;
  const b=E('button','pv-spot');b.setAttribute('aria-label',`Przejdź do punktu ${j+1}`);b.dataset.yaw=yaw;b.dataset.pit=pit;
  b.innerHTML='<svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="17"/><path d="M12 24l8-8 8 8"/></svg>';
  b.onclick=e=>{e.stopPropagation();stopAuto();st.pitch=-8;show(j,back+180)};hot.appendChild(b)})}

 // ----- rysowanie klatki -----
 function render(){const w=view.clientWidth,h=view.clientHeight;const persp=(w/2)/Math.tan(st.hfov*Math.PI/360);
  view.style.perspective=persp+'px';
  cam.style.transform=`translateZ(${persp}px) rotateX(${st.pitch}deg) rotateY(${st.yaw}deg)`;
  const R=Math.PI/180,cp=st.pitch*R;
  hot.querySelectorAll('.pv-spot').forEach(b=>{const Y=(+b.dataset.yaw-st.yaw)*R,P=(+b.dataset.pit)*R;   // kierunek strzałki względem kamery
   const x0=Math.cos(P)*Math.sin(Y),y0=Math.sin(P),z0=Math.cos(P)*Math.cos(Y),y1=y0*Math.cos(cp)-z0*Math.sin(cp),z1=y0*Math.sin(cp)+z0*Math.cos(cp);
   const vis=z1>.15;b.style.display=vis?'':'none';if(!vis)return;
   const x=w/2+persp*x0/z1,y=h/2-persp*y1/z1;
   b.style.transform=`translate(${x.toFixed(1)}px,${y.toFixed(1)}px) translate(-50%,-50%)`})}
 function loop(ts){const dt=st.last?Math.min(.05,(ts-st.last)/1000):0;st.last=ts;
  if(st.auto&&!st.drag)st.yaw+=dt*4;
  if(st.hold)st.yaw+=st.hold*dt*45;
  if(!st.drag&&(Math.abs(st.vy)>.01||Math.abs(st.vp)>.01)){st.yaw+=st.vy;st.pitch+=st.vp;st.vy*=.9;st.vp*=.9}
  st.pitch=Math.max(-85,Math.min(85,st.pitch));if(st.vis)render();st.raf=requestAnimationFrame(loop)}
 function stopAuto(){st.auto=false}

 // ----- obsługa myszy, dotyku, klawiatury -----
 view.addEventListener('pointerdown',e=>{stopAuto();view.setPointerCapture(e.pointerId);st.drag={x:e.clientX,y:e.clientY,yaw:st.yaw,p:st.pitch,t:performance.now()};st.vy=st.vp=0});
 view.addEventListener('pointermove',e=>{if(!st.drag)return;const k=st.hfov/view.clientWidth;
  const ny=st.drag.yaw-(e.clientX-st.drag.x)*k,np=st.drag.p+(e.clientY-st.drag.y)*k;st.vy=(ny-st.yaw)*.5;st.vp=(np-st.pitch)*.5;st.yaw=ny;st.pitch=np});
 const up=()=>{st.drag=null};view.addEventListener('pointerup',up);view.addEventListener('pointercancel',up);
 view.addEventListener('wheel',e=>{e.preventDefault();stopAuto();zoom(e.deltaY>0?6:-6)},{passive:false});
 host.tabIndex=0;host.addEventListener('keydown',e=>{const k={ArrowLeft:[-8,0],ArrowRight:[8,0],ArrowUp:[0,-6],ArrowDown:[0,6]}[e.key];
  if(k){e.preventDefault();stopAuto();st.yaw+=k[0];st.pitch-=k[1]}else if(e.key==='+'||e.key==='=')zoom(-8);else if(e.key==='-')zoom(8)});
 function zoom(d){st.hfov=Math.max(40,Math.min(115,st.hfov+d));upgrade()}
 const holdBtn=(b,v)=>{const on=e=>{e.preventDefault();stopAuto();st.hold=v},off=()=>st.hold=0;
  b.addEventListener('pointerdown',on);['pointerup','pointerleave','pointercancel'].forEach(t=>b.addEventListener(t,off));
  b.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();stopAuto();st.yaw+=v*15}})};
 holdBtn(ui.querySelector('[data-act=left]'),-1);holdBtn(ui.querySelector('[data-act=right]'),1);
 ui.querySelector('[data-act=in]').onclick=()=>{stopAuto();zoom(-12)};ui.querySelector('[data-act=out]').onclick=()=>{stopAuto();zoom(12)};
 ui.querySelector('.pv-prev').onclick=()=>{stopAuto();show(st.i-1)};ui.querySelector('.pv-next').onclick=()=>{stopAuto();show(st.i+1)};
 const fsTarget=opt.fullscreenTarget||host;
 ui.querySelector('[data-act=fs]').onclick=()=>{const d=document;if(d.fullscreenElement)d.exitFullscreen();else (fsTarget.requestFullscreen||fsTarget.webkitRequestFullscreen).call(fsTarget)};
 document.addEventListener('fullscreenchange',()=>{const on=document.fullscreenElement===fsTarget;fsTarget.classList.toggle('pv-full',on);st.lvl=Math.min(st.lvl,0);setTimeout(upgrade,250)});
 new ResizeObserver(()=>upgrade()).observe(view);
 // gdy okno zniknie z ekranu, przeglądarka przestaje rysować (oszczędność baterii)
 new IntersectionObserver(es=>{st.vis=es[0].isIntersecting||!!document.fullscreenElement}).observe(host);
 show(opt.start||0,opt.yaw);st.raf=requestAnimationFrame(loop);
 return {show,state:st}}

window.PV=mountPano(host,{start:9,yaw:0,pitch:-6});return 'ok'})()