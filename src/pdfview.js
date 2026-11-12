// =====================================================================
// Podgląd PDF na stronie: dokumenty (standardy, RODO, ogłoszenia) otwierają się w oknie, a nie pobierają –
// także na telefonach z Androidem i w przeglądarkach ustawionych na „pobieraj PDF-y”.
// Biblioteka PDF.js (Mozilla, Apache 2.0) leży w motywie: {{THEME}}/vendor/pdfjs/. W prototypie z dysku
// (file://) albo gdy coś się nie uda – zwykłe otwarcie pliku w nowej karcie.
// =====================================================================
(function(){
 const LIB='{{THEME}}/vendor/pdfjs/';
 if(LIB.includes('{{')||location.protocol==='file:')return;          // prototyp: zostaje zwykły link
 let lib=null;
 const load=()=>lib||(lib=new Promise((ok,no)=>{const s=document.createElement('script');s.src=LIB+'pdf.min.js';
  s.onload=()=>{window.pdfjsLib.GlobalWorkerOptions.workerSrc=LIB+'pdf.worker.min.js';ok(window.pdfjsLib)};s.onerror=no;document.head.appendChild(s)}));
 const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;
  const href=a.getAttribute('href');if(!/\.pdf(\?|#|$)/i.test(href)||document.body.classList.contains('editing'))return;
  e.preventDefault();open(a.href,a.textContent.trim()||'Dokument')});
 async function open(url,title){
  const V=document.createElement('div');V.className='pdfv';V.setAttribute('role','dialog');V.setAttribute('aria-label',title);
  V.innerHTML=`<div class="pdfv-h"><p><b>${esc(title)}</b><span class="pdfv-n">Wczytywanie…</span></p><a class="pdfv-d" href="${esc(url)}" download>Pobierz</a><button type="button" class="pdfv-x">Zamknij</button></div><div class="pdfv-b"></div>`;
  const close=()=>{V.remove();removeEventListener('keydown',key);document.documentElement.style.overflow=''},key=e=>{if(e.key==='Escape')close()};
  V.querySelector('.pdfv-x').onclick=close;addEventListener('keydown',key);document.body.appendChild(V);document.documentElement.style.overflow='hidden';V.querySelector('.pdfv-x').focus();
  try{const pdfjs=await load(),doc=await pdfjs.getDocument(url).promise,box=V.querySelector('.pdfv-b');
   V.querySelector('.pdfv-n').textContent=doc.numPages+(doc.numPages===1?' strona':doc.numPages<5?' strony':' stron');
   const w=Math.min(box.clientWidth-24,900),dpr=Math.min(2,devicePixelRatio||1);
   for(let i=1;i<=doc.numPages&&V.isConnected;i++){const pg=await doc.getPage(i),vp0=pg.getViewport({scale:1}),scale=w/vp0.width,vp=pg.getViewport({scale:scale*dpr});
    const c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;c.style.width=w+'px';c.setAttribute('aria-label',`Strona ${i}`);box.appendChild(c);
    await pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise}}
  catch(err){close();window.open(url,'_blank','noopener')}}            // nie wyszło – zwykłe otwarcie pliku
})();
