// =====================================================================
// Podgląd dokumentów na stronie: PDF-y i pliki Worda (.docx) otwierają się w oknie, a nie pobierają –
// także na telefonach z Androidem i w przeglądarkach ustawionych na „pobieraj PDF-y”. Proboszcz nie musi
// przerabiać Worda na PDF.
// Biblioteki leżą w motywie: {{THEME}}/vendor/pdfjs/ (PDF.js, Mozilla, Apache 2.0) i {{THEME}}/vendor/mammoth/
// (mammoth – Word na zwykły tekst strony, BSD-2). Wczytują się dopiero przy pierwszym otwarciu dokumentu.
// Plik z innej strony (np. list z parafiajaworze.pl) przeglądarka może wczytać tylko przez wtyczkę (/pdf).
// W prototypie z dysku (file://) albo gdy coś się nie uda – zwykłe otwarcie pliku w nowej karcie.
// Starego formatu .doc ani .odt nie pokażemy – te zostają zwykłym linkiem.
// =====================================================================
(function(){
 const LIB='{{THEME}}/vendor/';
 if(LIB.includes('{{')||location.protocol==='file:')return;          // prototyp: zostaje zwykły link
 const libs={};
 const script=(src,ready)=>libs[src]||(libs[src]=new Promise((ok,no)=>{const s=document.createElement('script');s.src=LIB+src;
  s.onload=()=>ok(ready());s.onerror=no;document.head.appendChild(s)}));
 const pdfLib=()=>script('pdfjs/pdf.min.js',()=>{window.pdfjsLib.GlobalWorkerOptions.workerSrc=LIB+'pdfjs/pdf.worker.min.js';return window.pdfjsLib});
 const wordLib=()=>script('mammoth/mammoth.browser.min.js',()=>window.mammoth);
 const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 const kind=href=>{const m=String(href).split(/[?#]/)[0].match(/\.(pdf|docx)$/i);return m&&m[1].toLowerCase()};
 const many=(n,one,few,lots)=>n+' '+(n===1?one:(n%10>=2&&n%10<=4&&(n%100<10||n%100>=20))?few:lots);
 document.addEventListener('click',e=>{const a=e.target.closest('a[href]');if(!a||e.ctrlKey||e.metaKey||e.shiftKey)return;
  const k=kind(a.getAttribute('href'));if(!k||document.body.classList.contains('editing'))return;
  e.preventDefault();open(a.href,a.textContent.trim()||'Dokument',k)});
 async function open(url,title,k){
  const V=document.createElement('div');V.className='pdfv';V.setAttribute('role','dialog');V.setAttribute('aria-label',title);
  V.innerHTML=`<div class="pdfv-h"><p><b>${esc(title)}</b><span class="pdfv-n">Wczytywanie…</span></p><a class="pdfv-d" href="${esc(url)}" download>Pobierz</a><button type="button" class="pdfv-x">Zamknij</button></div><div class="pdfv-b"></div>`;
  const close=()=>{V.remove();removeEventListener('keydown',key);document.documentElement.style.overflow=''},key=e=>{if(e.key==='Escape')close()};
  V.querySelector('.pdfv-x').onclick=close;addEventListener('keydown',key);document.body.appendChild(V);document.documentElement.style.overflow='hidden';V.querySelector('.pdfv-x').focus();
  // plik z innej strony – przez wtyczkę; „Pobierz” zostaje z oryginalnym adresem
  const P=window.PARAFIA,src=(new URL(url,location.href).origin!==location.origin&&P&&P.api)?P.api+'pdf?u='+encodeURIComponent(url):url;
  const box=V.querySelector('.pdfv-b'),n=V.querySelector('.pdfv-n');
  try{
   if(k==='docx'){
    const [mammoth,buf]=await Promise.all([wordLib(),fetch(src,{credentials:'same-origin'}).then(r=>{if(!r.ok)throw new Error(r.status);return r.arrayBuffer()})]);
    const res=await mammoth.convertToHtml({arrayBuffer:buf}),doc=document.createElement('div');doc.className='docv';doc.innerHTML=res.value;
    // linki z dokumentu: tylko zwykłe adresy, otwierane w nowej karcie
    doc.querySelectorAll('a[href]').forEach(a=>{if(/^(https?:|mailto:|tel:)/i.test(a.getAttribute('href'))){a.target='_blank';a.rel='noopener'}else a.removeAttribute('href')});
    doc.querySelectorAll('img').forEach(i=>{if(!/^data:image\//.test(i.getAttribute('src')||''))i.remove();else i.alt=i.alt||''});
    box.appendChild(doc);n.textContent='dokument Word';return}
   const pdfjs=await pdfLib(),doc=await pdfjs.getDocument(src).promise;
   n.textContent=many(doc.numPages,'strona','strony','stron');
   const w=Math.min(box.clientWidth-24,900),dpr=Math.min(2,devicePixelRatio||1);
   for(let i=1;i<=doc.numPages&&V.isConnected;i++){const pg=await doc.getPage(i),vp0=pg.getViewport({scale:1}),scale=w/vp0.width,vp=pg.getViewport({scale:scale*dpr});
    const c=document.createElement('canvas');c.width=vp.width;c.height=vp.height;c.style.width=w+'px';c.setAttribute('aria-label',`Strona ${i}`);box.appendChild(c);
    await pg.render({canvasContext:c.getContext('2d'),viewport:vp}).promise}}
  catch(err){close();window.open(url,'_blank','noopener')}}            // nie wyszło – zwykłe otwarcie pliku
})();
