// =====================================================================
// Drzwi do spaceru 360°: rysują się kreską, po kliknięciu odrysowują się (kolor schodzi, kreski
// się zwijają, w kole zostaje zdjęcie nawy), a w kole wczytuje się spacer. „Pełny ekran”
// powiększa samo koło (bez przeładowania spaceru); „Zamknij pełny ekran” albo Esc wraca do koła.
// W kole działa oryginalny odtwarzacz 3DVista z luteranie-wirtualne-muzea.pl; #media=9 – nawa.
// =====================================================================
(function(){const fig=document.querySelector('.rose');if(!fig)return;
 const TOUR='https://luteranie-wirtualne-muzea.pl/wirtualnyspacer/brenna/index.htm#media=9';
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const box=fig.querySelector('.rose-in'),visit=fig.querySelector('.visit');
 const fs=document.createElement('button');fs.type='button';fs.className='rose-fs';fs.textContent='Pełny ekran';fig.appendChild(fs);
 const x=document.createElement('button');x.type='button';x.className='rose-x';x.textContent='Zamknij pełny ekran';box.appendChild(x);
 let fr=null,started=false;
 const draw=()=>{fig.classList.remove('inked');void fig.offsetWidth;fig.classList.add('inked')};
 function open(){if(started)return;started=true;
  fr=document.createElement('iframe');fr.title='Spacer 360° po kościele w Brennej';fr.allow='fullscreen; gyroscope; accelerometer; xr-spatial-tracking';
  fr.addEventListener('load',()=>fig.classList.add('loaded'));fr.src=TOUR;box.appendChild(fr);   // wczytuje się, gdy drzwi się odrysowują
  // na ekranie dotykowym osłona przepuszcza przewijanie strony; pierwsze stuknięcie włącza obracanie
  const g=document.createElement('div');g.className='rose-guard';g.addEventListener('click',()=>g.remove());box.appendChild(g);
  fig.classList.add('undraw');setTimeout(()=>fig.classList.add('opened'),reduce?0:1700)}
 // pełny ekran: prawdziwy, gdy przeglądarka pozwala; inaczej (np. iPhone) koło rozciąga się na całe okno
 const isBig=()=>document.fullscreenElement===box||box.classList.contains('big');
 function big(on){
  if(on){if(box.requestFullscreen)box.requestFullscreen().catch(()=>setFake(true));else setFake(true)}
  else{if(document.fullscreenElement===box)document.exitFullscreen();setFake(false)}}
 function setFake(on){box.classList.toggle('big',on);document.documentElement.style.overflow=on?'hidden':'';sync()}
 function sync(){const on=isBig();fig.classList.toggle('full',on);if(!on)fs.focus({preventScroll:true})}
 document.addEventListener('fullscreenchange',sync);
 addEventListener('keydown',e=>{if(e.key==='Escape'&&box.classList.contains('big'))setFake(false)});
 fs.addEventListener('click',()=>big(true));x.addEventListener('click',()=>big(false));
 visit.addEventListener('click',open);fig.querySelector('.doors').addEventListener('click',open);
 // pierwsze rysowanie dopiero, gdy drzwi są dobrze widoczne
 fig.classList.add('sketch');new IntersectionObserver((es,ob)=>{if(es[0].isIntersecting){draw();ob.disconnect()}},{threshold:.6}).observe(fig)})();
