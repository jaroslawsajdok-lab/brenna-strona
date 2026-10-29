// =====================================================================
// Drzwi do spaceru 360°: rysują się kreską, po kliknięciu odrysowują się (kolor schodzi, kreski
// się zwijają, w kole zostaje zdjęcie nawy), potem spacer otwiera się na cały ekran.
// W oknie działa oryginalny odtwarzacz 3DVista z luteranie-wirtualne-muzea.pl;
// #media=N otwiera wycieczkę od N-tego punktu (9 – nawa). Po zamknięciu drzwi rysują się z powrotem.
// =====================================================================
(function(){const fig=document.querySelector('.rose');if(!fig)return;
 const TOUR='https://luteranie-wirtualne-muzea.pl/wirtualnyspacer/brenna/index.htm',START=9;
 const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
 const dlg=document.createElement('dialog');dlg.className='tour';dlg.setAttribute('aria-label','Spacer po kościele w Brennej');
 dlg.innerHTML='<div class="tour-h"><p><b>Kościół w Brennej</b><span>spacer 360°</span></p><button type="button" class="tour-x">Zamknij</button></div>'+
  '<div class="tour-v"><p class="tour-wait">Wczytywanie spaceru…</p><iframe title="Spacer 360° po kościele w Brennej" allow="fullscreen; gyroscope; accelerometer; xr-spatial-tracking" allowfullscreen></iframe></div>';
 document.body.appendChild(dlg);
 const fr=dlg.querySelector('iframe'),visit=fig.querySelector('.visit');let busy=false;
 fr.addEventListener('load',()=>dlg.classList.add('ready'));
 const draw=()=>{fig.classList.remove('inked');void fig.offsetWidth;fig.classList.add('inked')};
 function openTour(){if(!fr.src)fr.src=`${TOUR}#media=${START}`;
  dlg.showModal();document.documentElement.style.overflow='hidden';fr.focus()}
 function open(){if(busy)return;busy=true;
  if(!fr.src)fr.src=`${TOUR}#media=${START}`;          // spacer wczytuje się, gdy drzwi się odrysowują
  fig.classList.add('undraw');setTimeout(openTour,reduce?0:1700)}
 dlg.querySelector('.tour-x').onclick=()=>dlg.close();
 dlg.addEventListener('close',()=>{document.documentElement.style.overflow='';fig.classList.remove('undraw');draw();busy=false;
  visit.focus({preventScroll:true})});
 visit.addEventListener('click',open);fig.querySelector('.doors').addEventListener('click',open);
 // pierwsze rysowanie dopiero, gdy drzwi są dobrze widoczne
 fig.classList.add('sketch');new IntersectionObserver((es,ob)=>{if(es[0].isIntersecting){draw();ob.disconnect()}},{threshold:.6}).observe(fig)})();
