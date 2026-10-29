// =====================================================================
// Plan kościoła: schemat z punktami spaceru 360°, podgląd miejsca, spacer na pełnym ekranie
// Kolejność = PANOS (numery 1–22 w wycieczce 3DVista). Nazwy nadane na podstawie zdjęć – robocze.
// =====================================================================
const PLACES=[
 ['Kościół z góry','Z lotu ptaka',420,80],['Droga i łąki','Z lotu ptaka',460,80],['Wieś w dolinie','Z lotu ptaka',500,80],
 ['Dolina Brennicy','Z lotu ptaka',540,80],['Dach kościoła','Z lotu ptaka',580,80],
 ['Alejka do kościoła','Wokół kościoła',270,452],['Przed kościołem','Wokół kościoła',70,330],
 ['Wejście','Kościół',270,388],
 ['Nawa','Sala nabożeństw',270,226],['Ołtarz','Sala nabożeństw',270,104],['Przy ołtarzu','Sala nabożeństw',210,104],['Obok ołtarza','Sala nabożeństw',330,104],
 ['Widok z empory','Empora z organami',210,342],['Ławki na emporze','Empora z organami',270,342],['Przy organach','Empora z organami',330,342],
 ['Schody na dół','Dolna kondygnacja',440,236],['Korytarz','Dolna kondygnacja',500,236],['Sala katechetyczna','Dolna kondygnacja',560,236],
 ['Sala parafialna','Dolna kondygnacja',470,300],['Sala parafialna, drugi koniec','Dolna kondygnacja',530,300],
 ['Przy kościele','Wokół kościoła',70,210],['Teren za kościołem','Wokół kościoła',70,270]];
const placeName=i=>PLACES[i][1]==='Kościół'?PLACES[i][0]:`${PLACES[i][0]} · ${PLACES[i][1]}`;
const placeFace=i=>`${PANO_BASE}panorama_${PANOS[i][0]}_0/f/3/0_0.webp${PANO_VER}`;

(function(){const sec=document.getElementById('kosciol');if(!sec)return;
 const NS='http://www.w3.org/2000/svg',pts=sec.querySelector('.cp-pts'),list=sec.querySelector('.church-list'),
  img=sec.querySelector('.church-pv img'),nm=sec.querySelector('.cp-n'),gr=sec.querySelector('.cp-g'),go=sec.querySelector('.church-go');
 let cur=9;
 function preview(i){cur=i;img.src=placeFace(i);img.alt=`${PLACES[i][0]} – kościół w Brennej`;nm.textContent=PLACES[i][0];gr.textContent=PLACES[i][1];
  pts.querySelectorAll('.pt').forEach(g=>g.classList.toggle('on',+g.dataset.i===i))}
 // punkty na schemacie (myszą i klawiaturą); na telefonie zamiast nich lista
 PLACES.forEach(([n,g,x,y],i)=>{const e=document.createElementNS(NS,'g');e.setAttribute('class','pt');e.dataset.i=i;
  e.setAttribute('transform',`translate(${x} ${y})`);e.setAttribute('tabindex','0');e.setAttribute('role','button');
  e.setAttribute('aria-label',`${n}, ${g.toLowerCase()} – otwórz widok 360°`);
  e.innerHTML=`<title>${n}</title><circle class="hit" r="20"/><circle class="dot" r="9"/>`;
  e.addEventListener('mouseenter',()=>preview(i));e.addEventListener('focus',()=>preview(i));
  e.addEventListener('click',()=>open(i));e.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){ev.preventDefault();open(i)}});
  pts.appendChild(e)});
 const groups=[...new Set(PLACES.map(p=>p[1]))];
 list.innerHTML=groups.map(g=>`<li><span>${g==='Kościół'?'Wejście':g}</span><div>${PLACES.map((p,i)=>p[1]===g?`<button type="button" data-i="${i}">${p[0]}</button>`:'').join('')}</div></li>`).join('');
 list.addEventListener('click',e=>{const b=e.target.closest('button');if(b)open(+b.dataset.i)});
 for(let i=0;i<PLACES.length;i++)new Image().src=placeFace(i);   // podgląd bez czekania
 preview(cur);

 // spacer w oknie na cały ekran: nazwa miejsca, „Zamknij”, bez samoczynnego obracania
 const dlg=document.createElement('dialog');dlg.className='tour';dlg.setAttribute('aria-label','Spacer po kościele w Brennej');
 dlg.innerHTML='<div class="tour-h"><p><b class="tour-n"></b><span class="tour-g"></span></p><button type="button" class="tour-x">Zamknij</button></div><div class="tour-v"></div>';
 document.body.appendChild(dlg);
 const tn=dlg.querySelector('.tour-n'),tg=dlg.querySelector('.tour-g');let pano=null;
 function open(i){preview(i);
  if(!dlg.open){dlg.showModal();document.documentElement.style.overflow='hidden'}
  if(!pano)pano=mountPano(dlg.querySelector('.tour-v'),{start:i,yaw:0,pitch:-4,auto:false,name:i=>PLACES[i][0],
   onShow:i=>{tn.textContent=PLACES[i][0];tg.textContent=PLACES[i][1];preview(i)}});
  else{pano.state.pitch=-4;pano.show(i,0)}
  dlg.querySelector('.tour-v').focus()}
 dlg.querySelector('.tour-x').onclick=()=>dlg.close();
 dlg.addEventListener('close',()=>{document.documentElement.style.overflow='';go.focus({preventScroll:true})});
 go.addEventListener('click',e=>{e.preventDefault();open(cur)});
 sec.querySelector('.church-pv').addEventListener('click',()=>open(cur))})();
