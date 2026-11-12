// =====================================================================
// Łącznik z WordPressem (wtyczka „Parafia”). W prototypie window.PARAFIA nie istnieje i nic tu się nie dzieje.
// W WordPressie: (1) zanim ruszą edytory, wkleja zapisane treści bloków [data-key] i wiersze nabożeństw,
// (2) w trybie edycji sam zapisuje zmiany kilka sekund po ostatnim stuknięciu (bez przycisku „Zapisz”),
// (3) daje pozostałym modułom PARAFIA.call() – zapytanie do REST API z nonce i ponowieniem po wygaśnięciu.
// =====================================================================
(function(){const P=window.PARAFIA;if(!P)return;
 // --- zapytania do wtyczki ---
 P.call=async function(path,opt={}){
  const go=()=>fetch(P.api+path,{method:opt.method||'POST',credentials:'same-origin',
   headers:Object.assign(opt.form?{}:{'Content-Type':'application/json'},P.nonce?{'X-WP-Nonce':P.nonce}:{}),
   body:opt.form||(opt.body!==undefined?JSON.stringify(opt.body):undefined)});
  let r=await go();
  if(r.status===403&&P.ajax){                       // nonce wygasł (strona otwarta długo) – pobierz nowy i spróbuj raz jeszcze
   const n=await fetch(P.ajax+'?action=rest-nonce',{credentials:'same-origin'});if(n.ok){P.nonce=(await n.text()).trim();r=await go()}}
  const j=await r.json().catch(()=>({}));
  // niektóre serwery (wtyczki bezpieczeństwa) zamieniają kod błędu na 200 – błąd poznajemy też po treści odpowiedzi
  const bad=!r.ok||(j&&j.code&&j.data&&j.data.status>=400);
  if(bad)throw new Error(j.message||('Błąd '+r.status));return j};
 P.upload=async function(blobOrFile,name){const f=new FormData();f.append('file',blobOrFile,name||blobOrFile.name||'zdjecie.jpg');return P.call('media',{form:f})};

 // --- (1) zapisane treści wracają na stronę ---
 Object.entries(P.blocks||{}).forEach(([k,html])=>{const el=document.querySelector(`[data-key="${k}"]`);if(el)el.innerHTML=html});
 const tb=document.querySelector('[data-key="nabozenstwa"]');
 if(tb&&Array.isArray(P.services)&&P.services.length){const e=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const dm=d=>{const m=String(d).match(/^\d{4}-(\d{2})-(\d{2})$/);return m?(+m[2])+'.'+m[1]:d};   // pełna data RRRR-MM-DD albo dawne „8.11”
  tb.tBodies[0].innerHTML=P.services.map(r=>`<tr${r.f?' class="feast"':''}${/^\d{4}-/.test(r.d)?` data-date="${e(r.d)}"`:''}><td><b>${e(dm(r.d))}</b></td><td>${e(r.n)}</td><td>${e(r.b)}</td><td>${e(r.g)}</td></tr>`).join('')}
 if(!P.canEdit)return;

 // --- (2) zapis w trybie edycji ---
 const dirty=new Set();let timer=0,svcDirty=false;
 const stat=()=>document.querySelector('.editbar .savestat');
 const say=t=>{const s=stat();if(s)s.textContent=t};
 // kopia bloku bez elementów edytora (przyciski, pola wyboru plików, atrybuty edycji)
 const clean=el=>{const c=el.cloneNode(true);c.querySelectorAll('[contenteditable]').forEach(x=>x.removeAttribute('contenteditable'));
  c.querySelectorAll('.doc-add,input[type=file],.ctl,.rowtools,[data-ui]').forEach(x=>x.remove());
  c.querySelectorAll('[data-key]').forEach(x=>x.removeAttribute('data-key'));   // bloki zagnieżdżone (np. albumy w galerii) zapisują się razem z rodzicem
  return c.innerHTML.trim()};
 const rows=()=>[...tb.tBodies[0].rows].map(tr=>({d:tr.dataset.date||(tr.cells[0].textContent.match(/\d{1,2}\s*\.\s*\d{1,2}/)||[''])[0].replace(/\s/g,''),
  n:tr.cells[1].textContent.trim(),b:tr.cells[2].textContent.trim(),g:tr.cells[3].textContent.trim(),f:tr.classList.contains('feast')})).filter(r=>r.d||r.n);
 async function flush(){timer=0;const blocks={};dirty.forEach(k=>{const el=document.querySelector(`[data-key="${k}"]`);if(el)blocks[k]=clean(el)});dirty.clear();
  const svc=svcDirty;svcDirty=false;if(!Object.keys(blocks).length&&!svc)return;
  say('Zapisywanie…');
  try{if(Object.keys(blocks).length)await P.call('blocks',{body:{blocks}});if(svc&&tb)await P.call('services',{body:{rows:rows()}});say('Zapisano')}
  catch(e){Object.keys(blocks).forEach(k=>dirty.add(k));if(svc)svcDirty=true;say('Nie zapisano: '+e.message+' – spróbuję ponownie');schedule(5000)}}
 const schedule=(ms=1500)=>{clearTimeout(timer);timer=setTimeout(flush,ms)};
 const mark=el=>{let b=el&&el.closest&&el.closest('[data-key]');while(b&&b.parentElement&&b.parentElement.closest('[data-key]'))b=b.parentElement.closest('[data-key]');   // zapis do bloku najbardziej zewnętrznego
  if(!b||!document.body.classList.contains('editing'))return;
  if(b===tb)svcDirty=true;else dirty.add(b.dataset.key);schedule()};
 document.addEventListener('input',e=>mark(e.target));
 document.addEventListener('focusout',e=>mark(e.target));
 // zmiany w strukturze: wiersze nabożeństw (dodaj, usuń, przesuń, święto), dodane dokumenty
 document.querySelectorAll('[data-key]').forEach(b=>{try{new MutationObserver(ms=>{
  if(!document.body.classList.contains('editing'))return;
  if(ms.some(m=>m.type==='childList'||(m.type==='attributes'&&m.target.tagName==='TR')))mark(b)})
  .observe(b,b===tb?{childList:true,subtree:true,attributes:true,attributeFilter:['class']}:{childList:true,subtree:true})}
  catch(e){console.warn('Parafia: obserwacja bloku',b.dataset.key,e)}});
 addEventListener('beforeunload',e=>{if(timer||dirty.size||svcDirty){flush();e.preventDefault();e.returnValue=''}});
 P.flush=flush})();
