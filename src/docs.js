// =====================================================================
// Dokumenty: w prototypie osobna „podstrona” w tym samym pliku – adres #dokumenty chowa resztę
// treści i pokazuje sam dział pod nagłówkiem. W WordPressie to zwykła podstrona /dokumenty/.
// W trybie edycji przy każdej grupie „+ Dodaj plik” (prototyp: plik widać do odświeżenia strony;
// w WordPressie od razu trafia do biblioteki mediów).
// =====================================================================
(function(){const sec=document.getElementById('dokumenty');if(!sec)return;
 function route(){const h=location.hash;if(h==='#edycja')return;
  const on=h==='#dokumenty';const was=document.body.classList.contains('on-docs');
  document.body.classList.toggle('on-docs',on);
  if(on){scrollTo(0,0)}
  else if(was){const t=h&&h.length>1&&document.querySelector(h);requestAnimationFrame(()=>t?t.scrollIntoView():scrollTo(0,0))}}
 addEventListener('hashchange',route);route();
 // wejście prosto z adresu …#dokumenty: przeglądarka przewija do kotwicy po wczytaniu – wracamy na górę jak na nowej stronie
 addEventListener('load',()=>{if(document.body.classList.contains('on-docs'))setTimeout(()=>scrollTo(0,0),0)});

 const size=b=>b<1048576?Math.max(1,Math.round(b/1024))+' KB':(b/1048576).toFixed(1).replace('.',',')+' MB';
 sec.querySelectorAll('.docs-g').forEach(g=>{
  const b=document.createElement('button');b.type='button';b.className='doc-add';b.textContent='+ Dodaj plik';
  const f=document.createElement('input');f.type='file';f.accept='.pdf,.doc,.docx,.odt';f.hidden=true;
  b.onclick=()=>f.click();
  f.onchange=()=>{const file=f.files[0];if(!file)return;
   const li=document.createElement('li');li.className='doc';
   const a=document.createElement('a');a.className='doc-n';a.href=URL.createObjectURL(file);a.target='_blank';a.rel='noopener';
   a.textContent=file.name.replace(/\.[^.]+$/,'').replace(/[_-]+/g,' ');
   const m=document.createElement('span');m.className='doc-m';m.textContent=`${file.name.split('.').pop().toUpperCase()}, ${size(file.size)}`;
   li.append(a,m);g.querySelector('ul').appendChild(li);f.value='';
   // WordPress: plik do biblioteki mediów, na liście zostaje jego stały adres (zapis listy robi wp.js)
   const WP=window.PARAFIA;if(WP){m.textContent='wysyłanie…';
    WP.upload(file).then(r=>{a.href=r.url;m.textContent=`${file.name.split('.').pop().toUpperCase()}, ${size(file.size)}`})
     .catch(e=>{m.textContent='nie wysłano: '+e.message;m.classList.add('todo')})}};
  g.append(b,f)})})();
