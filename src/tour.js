// =====================================================================
// Szkic kościoła: trzy punkty (z góry, obok, wewnątrz) otwierają spacer 360° na cały ekran.
// W oknie działa oryginalny odtwarzacz 3DVista z luteranie-wirtualne-muzea.pl;
// #media=N otwiera wycieczkę od N-tego punktu (1 – dron nad kościołem, 7 – przed kościołem, 9 – nawa).
// =====================================================================
(function(){const fig=document.querySelector('.sketch');if(!fig)return;
 const TOUR='https://luteranie-wirtualne-muzea.pl/wirtualnyspacer/brenna/index.htm';
 const dlg=document.createElement('dialog');dlg.className='tour';dlg.setAttribute('aria-label','Spacer po kościele w Brennej');
 dlg.innerHTML='<div class="tour-h"><p><b>Kościół w Brennej</b><span>spacer 360°</span></p><button type="button" class="tour-x">Zamknij</button></div>'+
  '<div class="tour-v"><p class="tour-wait">Wczytywanie spaceru…</p><iframe title="Spacer 360° po kościele w Brennej" allow="fullscreen; gyroscope; accelerometer; xr-spatial-tracking" allowfullscreen></iframe></div>';
 document.body.appendChild(dlg);
 const fr=dlg.querySelector('iframe');let from=null;
 fr.addEventListener('load',()=>dlg.classList.add('ready'));
 function open(m,btn){from=btn;const src=`${TOUR}#media=${m}`;
  if(fr.src!==src){dlg.classList.remove('ready');fr.src=src}
  dlg.showModal();document.documentElement.style.overflow='hidden';fr.focus()}
 dlg.querySelector('.tour-x').onclick=()=>dlg.close();
 dlg.addEventListener('close',()=>{document.documentElement.style.overflow='';from&&from.focus({preventScroll:true})});
 fig.querySelectorAll('.pin').forEach(b=>b.addEventListener('click',()=>open(+b.dataset.m,b)))})();
