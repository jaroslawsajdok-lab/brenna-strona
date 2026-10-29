// =====================================================================
// Szkic kościoła: trzy punkty (z góry, obok, wewnątrz) otwierają spacer 360° na cały ekran
// Nazwy miejsc w kolejności PANOS (numery 1–22 w wycieczce 3DVista), nadane na podstawie zdjęć – robocze.
// =====================================================================
const PLACES=[
 ['Kościół z góry','Z lotu ptaka'],['Droga i łąki','Z lotu ptaka'],['Wieś w dolinie','Z lotu ptaka'],
 ['Dolina Brennicy','Z lotu ptaka'],['Dach kościoła','Z lotu ptaka'],
 ['Alejka do kościoła','Wokół kościoła'],['Przed kościołem','Wokół kościoła'],['Wejście','Wokół kościoła'],
 ['Nawa','Wewnątrz'],['Ołtarz','Wewnątrz'],['Przy ołtarzu','Wewnątrz'],['Obok ołtarza','Wewnątrz'],
 ['Widok z empory','Empora z organami'],['Ławki na emporze','Empora z organami'],['Przy organach','Empora z organami'],
 ['Schody na dół','Dolna kondygnacja'],['Korytarz','Dolna kondygnacja'],['Sala katechetyczna','Dolna kondygnacja'],
 ['Sala parafialna','Dolna kondygnacja'],['Sala parafialna, drugi koniec','Dolna kondygnacja'],
 ['Przy kościele','Wokół kościoła'],['Teren za kościołem','Wokół kościoła']];

(function(){const fig=document.querySelector('.sketch');if(!fig)return;
 const dlg=document.createElement('dialog');dlg.className='tour';dlg.setAttribute('aria-label','Spacer po kościele w Brennej');
 dlg.innerHTML='<div class="tour-h"><p><b class="tour-n"></b><span class="tour-g"></span></p><button type="button" class="tour-x">Zamknij</button></div><div class="tour-v"></div>';
 document.body.appendChild(dlg);
 const tn=dlg.querySelector('.tour-n'),tg=dlg.querySelector('.tour-g');let pano=null,from=null;
 function open(i,btn){from=btn;
  if(!dlg.open){dlg.showModal();document.documentElement.style.overflow='hidden'}
  if(!pano)pano=mountPano(dlg.querySelector('.tour-v'),{start:i,yaw:0,pitch:-4,auto:false,name:i=>PLACES[i][0],
   onShow:i=>{tn.textContent=PLACES[i][0];tg.textContent=PLACES[i][1]}});
  else{pano.state.pitch=-4;pano.show(i,0)}
  dlg.querySelector('.tour-v').focus()}
 dlg.querySelector('.tour-x').onclick=()=>dlg.close();
 dlg.addEventListener('close',()=>{document.documentElement.style.overflow='';from&&from.focus({preventScroll:true})});
 fig.querySelectorAll('.pin').forEach(b=>b.addEventListener('click',()=>open(+b.dataset.i,b)))})();
