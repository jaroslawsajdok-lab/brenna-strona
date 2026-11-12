// ===== tabela nabożeństw: miesiące, edycja wierszy (dodaj, usuń, przesuń, święto) =====
// Każdy wiersz ma pełną datę w data-date (RRRR-MM-DD). Proboszcz wpisuje „8.11” – rok dobiera się do oglądanego miesiąca.
// Nad tabelą przełącznik miesięcy: goście widzą miesiące z nabożeństwami, w trybie edycji można iść do 24 miesięcy naprzód.
(function(){const tb=document.querySelector('#nabozenstwa .titleblock');if(!tb)return;const body=tb.tBodies[0];
 const DN=['niedziela','poniedziałek','wtorek','środa','czwartek','piątek','sobota'];
 const MN=['Styczeń','Luty','Marzec','Kwiecień','Maj','Czerwiec','Lipiec','Sierpień','Wrzesień','Październik','Listopad','Grudzień'];
 const day0=()=>{const t=new Date();t.setHours(0,0,0,0);return t};
 const iso=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
 const mkey=d=>d.getFullYear()*12+d.getMonth();                  // numer miesiąca do porównań
 const kdate=k=>new Date(Math.floor(k/12),k%12,1);
 let view=mkey(day0());                                           // oglądany miesiąc
 // data wiersza: z data-date, a gdy jej brak (wpisane ręcznie „8.11”) – rok najbliższy oglądanemu miesiącowi
 const dateOf=tr=>{const iz=tr.dataset.date&&tr.dataset.date.match(/^(\d{4})-(\d{2})-(\d{2})$/);if(iz)return new Date(+iz[1],+iz[2]-1,+iz[3]);
  const m=tr.cells[0].textContent.match(/(\d{1,2})\s*\.\s*(\d{1,2})/);if(!m)return null;
  const ref=new Date(Math.floor(view/12),view%12,15);let best=null;
  for(const y of [ref.getFullYear()-1,ref.getFullYear(),ref.getFullYear()+1]){const d=new Date(y,+m[2]-1,+m[1]);if(!best||Math.abs(d-ref)<Math.abs(best-ref))best=d}
  tr.dataset.date=iso(best);return best};
 const dateCell=d=>`<b>${d.getDate()}.${String(d.getMonth()+1).padStart(2,'0')}</b> ${DN[d.getDay()]}`;
 const NONE=v=>/^(|-|–|—|brak|nie ma|nie|x|0)$/i.test(v.trim());
 const editing=()=>document.body.classList.contains('editing');
 const CTL='<td class="ctl"><button type="button" class="up" aria-label="Przesuń wyżej" title="Wyżej"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button><button type="button" class="dn" aria-label="Przesuń niżej" title="Niżej"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg></button><button type="button" class="st" aria-label="Oznacz jako święto" title="Święto (wyróżnienie)"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg></button><button type="button" class="rm" aria-label="Usuń wiersz" title="Usuń wiersz"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></td>';
 tb.tHead.rows[0].insertAdjacentHTML('beforeend','<th class="ctl" scope="col"><span class="sr">Edycja wiersza</span></th>');
 [...body.rows].forEach(tr=>{tr.insertAdjacentHTML('beforeend',CTL);tr.classList.remove('next');[2,3].forEach(i=>tr.cells[i].classList.remove('tbc'))});
 // tabela razem z przełącznikiem miesięcy w jednym bloku (obok zostaje „W tygodniu”)
 const wrap=document.createElement('div');wrap.className='tbwrap';tb.before(wrap);
 const CH=d=>`<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="${d}"/></svg>`;
 const nav=document.createElement('div');nav.className='mnav';
 nav.innerHTML=`<button type="button" class="mbtn mprev">${CH('M15 5l-7 7 7 7')}<span></span></button><h3 class="mname" aria-live="polite"></h3><button type="button" class="mbtn mnext"><span></span>${CH('M9 5l7 7-7 7')}</button>`;
 const empty=document.createElement('p');empty.className='mempty';
 wrap.append(nav,tb,empty);
 const tools=document.createElement('div');tools.className='rowtools';
 tools.innerHTML='<button type="button" class="addrow addone"><span aria-hidden="true">+</span> Dodaj nabożeństwo</button><button type="button" class="addrow addsun"><span aria-hidden="true">+</span> Dodaj wszystkie niedziele miesiąca</button><p>Kolejne miesiące wybierasz strzałkami nad tabelą. Datę wpisz jak 8.11 – dzień tygodnia uzupełni się sam, a wiersze ułożą się według dat. Minione nabożeństwa znikają ze strony automatycznie. ★ wyróżnia święto. Jeśli w Brennej albo w Górkach nie ma nabożeństwa, zostaw komórkę pustą.</p>';
 wrap.append(tools);
 const prev=nav.querySelector('.mprev'),next=nav.querySelector('.mnext');
 // miesiące dostępne: dla gości – bieżący i te z przyszłymi nabożeństwami; w edycji – od bieżącego do 24 miesięcy naprzód
 function months(){const now=mkey(day0());if(editing())return Array.from({length:25},(_,i)=>now+i);
  const s=new Set([now]);[...body.rows].forEach(tr=>{if(tr._d&&!tr.classList.contains('past'))s.add(mkey(tr._d))});return [...s].sort((a,b)=>a-b)}
 function show(){const ms=months();if(!ms.includes(view))view=ms.reduce((b,k)=>Math.abs(k-view)<Math.abs(b-view)?k:b,ms[0]);
  const i=ms.indexOf(view),d=kdate(view);
  nav.querySelector('.mname').textContent=`${MN[d.getMonth()]} ${d.getFullYear()}`;
  const set=(b,k)=>{b.style.visibility=k==null?'hidden':'';if(k!=null){const kd=kdate(k);b.querySelector('span').textContent=MN[kd.getMonth()]+(kd.getFullYear()!==d.getFullYear()?' '+kd.getFullYear():'');b.setAttribute('aria-label',(b===prev?'Poprzedni miesiąc: ':'Następny miesiąc: ')+MN[kd.getMonth()]+' '+kd.getFullYear())}};
  set(prev,i>0?ms[i-1]:null);set(next,i<ms.length-1?ms[i+1]:null);
  let n=0;[...body.rows].forEach(tr=>{const off=!!tr._d&&mkey(tr._d)!==view;tr.classList.toggle('off',off);if(!off&&(editing()||!tr.classList.contains('past')))n++});
  empty.hidden=n>0;empty.textContent=editing()?'W tym miesiącu nie ma jeszcze nabożeństw – dodaj je przyciskami poniżej.':'Nabożeństwa na ten miesiąc zostaną wkrótce podane.'}
 prev.onclick=()=>{const ms=months(),i=ms.indexOf(view);if(i>0){view=ms[i-1];show()}};
 next.onclick=()=>{const ms=months(),i=ms.indexOf(view);if(i<ms.length-1){view=ms[i+1];show()}};
 // porządek: pełna data, dzień tygodnia, sortowanie, „najbliższe”, minione, filtr miesiąca
 function tidy(sort){const rows=[...body.rows],t=day0();
  rows.forEach(tr=>{const d=dateOf(tr);tr._d=d;if(d){tr.dataset.date=iso(d);if(sort)tr.cells[0].innerHTML=dateCell(d)}});
  if(sort)rows.filter(r=>r._d).sort((a,b)=>a._d-b._d).forEach(r=>body.appendChild(r));
  let nx=false;[...body.rows].forEach(tr=>{const past=tr._d&&tr._d<t;tr.classList.toggle('past',!!past);const n=!past&&!nx&&!!tr._d;if(n)nx=true;tr.classList.toggle('next',n)});
  [...body.rows].forEach(tr=>{[2,3].forEach(i=>{const c=tr.cells[i],v=c.textContent.trim(),none=NONE(v);
   if(none&&c.innerHTML!==''&&document.activeElement!==c)c.textContent='';c.classList.toggle('none',none);c.classList.toggle('tbc',!none&&v.length>6);c.dataset.ph='brak'})});
  show();if(editing())ce()}
 function ce(){[...body.rows].forEach(tr=>[...tr.cells].forEach(td=>{if(td.classList.contains('ctl'))td.removeAttribute('contenteditable');else if(editing())td.setAttribute('contenteditable','true')}))}
 new MutationObserver(()=>{ce();show();if(!editing())[...body.rows].forEach(tr=>[...tr.cells].forEach(td=>td.removeAttribute('contenteditable')))}).observe(document.body,{attributes:true,attributeFilter:['class']});
 // zmieniona data w pierwszej kolumnie: rok od nowa (według oglądanego miesiąca), widok przechodzi do miesiąca wiersza
 body.addEventListener('focusout',e=>{const td=e.target.closest('td');if(!td)return;
  setTimeout(()=>{if(td.cellIndex===0){const tr=td.parentNode;delete tr.dataset.date;const d=dateOf(tr);if(d)view=mkey(d)}tidy(td.cellIndex===0)},0)});
 body.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.closest('td[contenteditable]')){e.preventDefault();e.target.blur()}});
 body.addEventListener('click',e=>{const b=e.target.closest('.ctl button');if(!b)return;const tr=b.closest('tr');
  if(b.classList.contains('rm')){tr.classList.add('gone');setTimeout(()=>{tr.remove();tidy(false)},220);return}
  if(b.classList.contains('st')){tr.classList.toggle('feast');b.setAttribute('aria-pressed',tr.classList.contains('feast'));return}
  if(b.classList.contains('up')&&tr.previousElementSibling)body.insertBefore(tr,tr.previousElementSibling);
  if(b.classList.contains('dn')&&tr.nextElementSibling)body.insertBefore(tr.nextElementSibling,tr);
  tidy(false);b.focus()});
 // zwykłe godziny: z ostatniego wiersza, który nie jest świętem
 const regular=()=>{const r=[...body.rows].reverse().find(r=>!r.classList.contains('feast')&&/\d/.test(r.cells[2].textContent));return r?[r.cells[2].textContent.trim(),r.cells[3].textContent.trim()]:['8:30','10:15']};
 const addRow=d=>{const [b,g]=regular(),tr=document.createElement('tr');tr.dataset.date=iso(d);
  tr.innerHTML=`<td>${dateCell(d)}</td><td></td><td>${b}</td><td>${g}</td>`+CTL;body.appendChild(tr);tr.classList.add('fresh');tr.cells[1].dataset.ph='nazwa niedzieli lub święta';return tr};
 const sundays=k=>{const out=[],d=kdate(k);while(d.getDay()!==0)d.setDate(d.getDate()+1);while(mkey(d)===k){if(d>=day0())out.push(new Date(d));d.setDate(d.getDate()+7)}return out};
 const has=d=>[...body.rows].some(r=>r.dataset.date===iso(d));
 // „+ Dodaj nabożeństwo”: najbliższa wolna niedziela w oglądanym miesiącu (gdy brak – pierwsza niedziela następnego)
 tools.querySelector('.addone').onclick=()=>{let d=sundays(view).find(x=>!has(x));
  if(!d){d=kdate(view+1);while(d.getDay()!==0||d<day0())d.setDate(d.getDate()+1)}
  view=mkey(d);const tr=addRow(d);tidy(true);ce();tr.cells[1].focus()};
 // „+ Dodaj wszystkie niedziele miesiąca”: brakujące niedziele oglądanego miesiąca ze zwykłymi godzinami
 tools.querySelector('.addsun').onclick=()=>{const ds=sundays(view).filter(x=>!has(x));
  if(!ds.length){empty.hidden=false;empty.textContent='Wszystkie niedziele tego miesiąca są już w tabeli.';return}
  const trs=ds.map(addRow);tidy(true);ce();trs[0].cells[1].focus()};
 tidy(true);
 // na start: miesiąc najbliższego nabożeństwa
 const nx=body.querySelector('tr.next');if(nx&&nx._d){view=mkey(nx._d);show()}})();
// ===== pasek „najbliższe nabożeństwo” pod menu (liczony z tabeli) =====
(function(){const tb=document.querySelector('#nabozenstwa .titleblock'),main=document.getElementById('tresc');if(!tb||!main)return;
 const MON=['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia'];
 const bar=document.createElement('a');bar.className='nextbar';bar.href='#nabozenstwa';main.prepend(bar);
 const when=d=>{const t=new Date();t.setHours(0,0,0,0);const n=Math.round((d-t)/864e5);return n===0?'dziś':n===1?'jutro':n===2?'pojutrze':n<7?'za '+n+' dni':n<14?'za tydzień':'za '+Math.round(n/7)+' tyg.'};
 function upd(){const tr=tb.tBodies[0].querySelector('tr.next');if(!tr||!tr._d){bar.hidden=true;return}bar.hidden=false;
  const d=tr._d,day=(tr.cells[0].textContent.match(/[a-ząćęłńóśźż]+$/i)||[''])[0],name=tr.cells[1].textContent.trim(),B=tr.cells[2].textContent.trim(),G=tr.cells[3].textContent.trim(),NO=v=>/^(|-|–|—|brak|nie ma|nie|x|0)$/i.test(v),places=[['Brenna',B,'w Brennej'],['Górki',G,'w Górkach']].filter(x=>!NO(x[1]));
  bar.classList.toggle('feast',tr.classList.contains('feast'));bar.classList.toggle('today',when(d)==='dziś');
  const only=places.length===1?`tylko ${places[0][2]}`:'';
  bar.setAttribute('aria-label',`Najbliższe nabożeństwo: ${day} ${d.getDate()} ${MON[d.getMonth()]}, ${name}. ${places.map(x=>x[0]+' '+x[1]).join(', ')}${only?' ('+only+')':''}. Zobacz wszystkie nabożeństwa.`);
  const w=when(d),pl=places.length===2&&places[0][1]===places[1][1]?[['Brenna i Górki',places[0][1]]]:places;
  bar.innerHTML=`<span class="nb wrap" aria-hidden="true"><span class="nb-box"><span class="nb-k">Najbliższe nabożeństwo</span><span class="nb-d"><b>${day} ${d.getDate()} ${MON[d.getMonth()]}</b><i>${w}</i></span><span class="nb-n">${name}</span><span class="nb-p">${pl.map(([n,v])=>`<span>${n} <b>${v}</b></span>`).join('')}${only?`<span class="nb-o">${only}</span>`:''}</span></span></span>`}

 new MutationObserver(upd).observe(tb.tBodies[0],{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:['class']});upd()})();

