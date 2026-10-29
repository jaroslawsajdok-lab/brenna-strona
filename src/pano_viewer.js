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
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const st={i:0,yaw:opt.yaw??-1.6,pitch:opt.pitch??-14,hfov:96,auto:opt.auto!==false&&!reduce,drag:null,vy:0,vp:0,hold:0,lvl:-1,raf:0,last:0,vis:true};
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
 // Przejście: nowy sześcian wczytuje się w ukryciu, potem krótkie przyciemnienie i podmiana (bez nakładania się obrazów).
 let gen=0;
 function build(level){
  // Każdy kafelek dzielony jest na mniejsze płytki z osobną transformacją 3D. Duże ściany przecinające
  // płaszczyznę kamery przeglądarki rysują z błędami (dziury, „hieroglify”); małe płytki tego unikają.
  const id=PANOS[st.i][0],L=PANO_LEVELS[level];const cube=E('div','pv-cube');cube._imgs=[];
  const n=L[2],t=S/n,m=Math.max(1,Math.round(8/n)),w=t/m;
  for(const f of ['f','r','b','l','u','d'])for(let rr=0;rr<n;rr++)for(let c=0;c<n;c++){
   const url=`${PANO_BASE}panorama_${id}_0/${f}/${L[0]}/${rr}_${c}.webp${PANO_VER}`;
   const im=new Image();im.decoding='async';im.src=url;cube._imgs.push(im);
   for(let a=0;a<m;a++)for(let b=0;b<m;b++){const d=E('div','pv-tile');const fx=c*t+b*w,fy=rr*t+a*w;
    d.style.cssText=`width:${w+2}px;height:${w+2}px;background-image:url("${url}");background-size:${t+2*m}px ${t+2*m}px;background-position:${-b*w}px ${-a*w}px;`+
     `transform:${FACE_T[f]} translateZ(${-S/2+.5}px) translate(${fx-S/2}px,${fy-S/2}px)`;cube.appendChild(d)}}
  return cube}
 // czeka na kafelki (wczytane I zdekodowane, żeby nic nie migało); zwraca liczbę poprawnych
 function whenLoaded(cube,ms){const ims=cube._imgs;return Promise.race([
  Promise.all(ims.map(im=>new Promise(r=>{const ok=()=>(im.decode?im.decode().catch(()=>{}):Promise.resolve()).then(()=>r(im.naturalWidth?1:0));
   if(im.complete)ok();else{im.onload=ok;im.onerror=()=>r(0)}}))).then(a=>a.reduce((x,y)=>x+y,0)),
  new Promise(r=>setTimeout(()=>r(ims.filter(i=>i.naturalWidth).length),ms))])}
 const frames=n=>new Promise(r=>{const f=k=>k?requestAnimationFrame(()=>f(k-1)):r();f(n)});
 function swap(c){[...stage.children].forEach(o=>{if(o!==c)o.remove()});c.style.visibility=''}
 function fail(){host.classList.remove('pv-busy');veil.classList.remove('on');if(host.querySelector('.pv-err'))return;
  const m=E('div','pv-err');m.innerHTML='Nie udało się wczytać spaceru. <a href="https://luteranie-wirtualne-muzea.pl/wirtualnyspacer/brenna/index.htm" target="_blank" rel="noopener">Otwórz go w nowej karcie</a>';host.appendChild(m)}
 // zasłona: przy zmianie punktu obraz gaśnie do koloru tła, podmiana odbywa się pod zasłoną
 const veil=E('div','pv-veil');host.insertBefore(veil,hot);
 const veilOn=()=>new Promise(r=>{if(veil.classList.contains('on'))return r();veil.classList.add('on');setTimeout(r,260)});
 function show(i,yaw){
  st.i=(i+PANOS.length)%PANOS.length;st.lvl=-1;const my=++gen;const first=!st.ready;
  ui.querySelector('.pv-n').textContent=opt.name?opt.name(st.i):`${st.i+1} / ${PANOS.length}`;opt.onShow&&opt.onShow(st.i);host.classList.add('pv-busy');
  const c=build(0);c.style.visibility='hidden';stage.appendChild(c);
  return Promise.all([whenLoaded(c,6000),first?0:veilOn()]).then(async([ok])=>{if(my!==gen){c.remove();return}
   if(!ok&&!stage.querySelector('.pv-cube:not([style*=hidden])')){c.remove();fail();return}
   hot.style.visibility='hidden';swap(c);if(yaw!=null)st.yaw=yaw;hotspots();
   await frames(2);if(my!==gen)return;
   veil.classList.remove('on');hot.style.visibility='';host.classList.remove('pv-busy');
   upgrade();if(first){st.ready=true;opt.onReady&&opt.onReady()}})}
 // ostrzejsze kafelki, gdy okno jest duże (pełny ekran) – tylko dla aktualnego punktu
 function upgrade(){if(host.classList.contains('pv-busy'))return;const w=view.clientWidth,need=w/Math.tan(st.hfov*Math.PI/360)*(devicePixelRatio||1)*.9;
  let lv=0;while(lv<PANO_LEVELS.length-2&&PANO_LEVELS[lv][1]<need)lv++;
  if(lv<=st.lvl)return;st.lvl=lv;if(lv===0)return;const my=gen;
  const c=build(lv);c.style.visibility='hidden';stage.appendChild(c);
  whenLoaded(c,15000).then(ok=>{if(my!==gen||!c.parentNode||ok<c._imgs.length*.9){c.remove();return}swap(c)})}
 // strzałki na podłodze prowadzące do sąsiednich punktów
 function hotspots(){hot.innerHTML='';PANOS[st.i][1].forEach(([to,yaw,back,pit])=>{const j=PANOS.findIndex(p=>p[0].startsWith(to));if(j<0)return;
  const b=E('button','pv-spot');b.setAttribute('aria-label',opt.name?`Przejdź: ${opt.name(j)}`:`Przejdź do punktu ${j+1}`);b.dataset.yaw=yaw;b.dataset.pit=pit;
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
