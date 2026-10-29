// ===== tabela nabożeństw: edycja wierszy (dodaj, usuń, przesuń, święto) =====
(function(){const tb=document.querySelector('#nabozenstwa .titleblock');if(!tb)return;const body=tb.tBodies[0];
 const DN=['niedziela','poniedziałek','wtorek','środa','czwartek','piątek','sobota'];
 const day0=()=>{const t=new Date();t.setHours(0,0,0,0);return t};
 const dateOf=tr=>{const m=tr.cells[0].textContent.match(/(\d{1,2})\s*\.\s*(\d{1,2})/);if(!m)return null;const t=day0();
  let d=new Date(t.getFullYear(),+m[2]-1,+m[1]);if(d-t<-200*864e5)d.setFullYear(d.getFullYear()+1);else if(d-t>165*864e5)d.setFullYear(d.getFullYear()-1);return d};
 const dateCell=d=>`<b>${d.getDate()}.${String(d.getMonth()+1).padStart(2,'0')}</b> ${DN[d.getDay()]}`;
 const NONE=v=>/^(|-|–|—|brak|nie ma|nie|x|0)$/i.test(v.trim());
 const editing=()=>document.body.classList.contains('editing');
 const CTL='<td class="ctl"><button type="button" class="up" aria-label="Przesuń wyżej" title="Wyżej"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg></button><button type="button" class="dn" aria-label="Przesuń niżej" title="Niżej"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 5v14M5 12l7 7 7-7"/></svg></button><button type="button" class="st" aria-label="Oznacz jako święto" title="Święto (wyróżnienie)"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg></button><button type="button" class="rm" aria-label="Usuń wiersz" title="Usuń wiersz"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></td>';
 tb.tHead.rows[0].insertAdjacentHTML('beforeend','<th class="ctl" scope="col"><span class="sr">Edycja wiersza</span></th>');
 [...body.rows].forEach(tr=>{tr.insertAdjacentHTML('beforeend',CTL);tr.classList.remove('next');[2,3].forEach(i=>tr.cells[i].classList.remove('tbc'))});
 const tools=document.createElement('div');tools.className='rowtools';
 tools.innerHTML='<button type="button" class="addrow"><span aria-hidden="true">+</span> Dodaj nabożeństwo</button><p>Datę wpisz jak 8.11 – dzień tygodnia uzupełni się sam, a wiersze ułożą się według dat. Minione nabożeństwa znikają ze strony automatycznie. ★ wyróżnia święto. Jeśli w Brennej albo w Górkach nie ma nabożeństwa, zostaw komórkę pustą.</p>';
 tb.after(tools);
 // porządek: dzień tygodnia, sortowanie, „najbliższe”, minione
 function tidy(sort){const rows=[...body.rows],t=day0();
  rows.forEach(tr=>{const d=dateOf(tr);tr._d=d;if(d&&sort)tr.cells[0].innerHTML=dateCell(d)});
  if(sort)rows.filter(r=>r._d).sort((a,b)=>a._d-b._d).forEach(r=>body.appendChild(r));
  let nx=false;[...body.rows].forEach(tr=>{const past=tr._d&&tr._d<t;tr.classList.toggle('past',!!past);const n=!past&&!nx&&!!tr._d;if(n)nx=true;tr.classList.toggle('next',n)});
  [...body.rows].forEach(tr=>{[2,3].forEach(i=>{const c=tr.cells[i],v=c.textContent.trim(),none=NONE(v);
   if(none&&c.innerHTML!==''&&document.activeElement!==c)c.textContent='';c.classList.toggle('none',none);c.classList.toggle('tbc',!none&&v.length>6);c.dataset.ph='brak'})});
  if(editing())ce()}
 function ce(){[...body.rows].forEach(tr=>[...tr.cells].forEach(td=>{if(td.classList.contains('ctl'))td.removeAttribute('contenteditable');else if(editing())td.setAttribute('contenteditable','true')}))}
 new MutationObserver(()=>{ce();if(!editing())[...body.rows].forEach(tr=>[...tr.cells].forEach(td=>td.removeAttribute('contenteditable')))}).observe(document.body,{attributes:true,attributeFilter:['class']});
 body.addEventListener('focusout',e=>{const td=e.target.closest('td');if(td)setTimeout(()=>tidy(td.cellIndex===0),0)});
 body.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.closest('td[contenteditable]')){e.preventDefault();e.target.blur()}});
 body.addEventListener('click',e=>{const b=e.target.closest('.ctl button');if(!b)return;const tr=b.closest('tr');
  if(b.classList.contains('rm')){tr.classList.add('gone');setTimeout(()=>{tr.remove();tidy(false)},220);return}
  if(b.classList.contains('st')){tr.classList.toggle('feast');b.setAttribute('aria-pressed',tr.classList.contains('feast'));return}
  if(b.classList.contains('up')&&tr.previousElementSibling)body.insertBefore(tr,tr.previousElementSibling);
  if(b.classList.contains('dn')&&tr.nextElementSibling)body.insertBefore(tr.nextElementSibling,tr);
  tidy(false);b.focus()});
 tools.querySelector('.addrow').onclick=()=>{const rows=[...body.rows],last=rows.filter(r=>dateOf(r)).pop(),reg=[...rows].reverse().find(r=>!r.classList.contains('feast')&&/\d/.test(r.cells[2].textContent));
  let d=last?new Date(dateOf(last)):day0();d.setDate(d.getDate()+1);while(d.getDay()!==0)d.setDate(d.getDate()+1);if(d<day0()){d=day0();while(d.getDay()!==0)d.setDate(d.getDate()+1)}
  const tr=document.createElement('tr');tr.innerHTML=`<td>${dateCell(d)}</td><td></td><td>${reg?reg.cells[2].textContent.trim():'8:30'}</td><td>${reg?reg.cells[3].textContent.trim():'10:15'}</td>`+CTL;
  body.appendChild(tr);tidy(true);tr.classList.add('fresh');ce();const n=tr.cells[1];n.focus();n.dataset.ph='nazwa niedzieli lub święta'};
 tidy(true)})();
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

// kalendarz: minione wydarzenia znikają, tak jak minione wiersze tabeli
(function(){const t=new Date();t.setHours(0,0,0,0);
 document.querySelectorAll('.days li').forEach(li=>{const d=li.querySelector('time')?.getAttribute('datetime');if(d&&new Date(d+'T00:00')<t)li.hidden=true})})();
