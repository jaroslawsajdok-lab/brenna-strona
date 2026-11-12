// =====================================================================
// Listy do uzupełniania w trybie edycji: spotkania w tygodniu, grupy, kalendarz wydarzeń (z datą),
// plik z ogłoszeniami parafialnymi, galeria (albumy ze zdjęciami + przeglądarka).
// Przyciski edycji mają atrybut data-ui (wp.js pomija je przy zapisie); przyciski „+ Dodaj…” stoją
// za blokiem, więc w ogóle nie trafiają do zapisu. W WordPressie pliki i zdjęcia idą do biblioteki mediów.
// =====================================================================
(function(){
 const WP=window.PARAFIA,editing=()=>document.body.classList.contains('editing');
 const X='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>';
 const MS=['sty','lut','mar','kwi','maj','cze','lip','sie','wrz','paź','lis','gru'];
 const MN=['styczeń','luty','marzec','kwiecień','maj','czerwiec','lipiec','sierpień','wrzesień','październik','listopad','grudzień'];
 const iso=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
 const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
 const size=b=>b<1048576?Math.max(1,Math.round(b/1024))+' KB':(b/1048576).toFixed(1).replace('.',',')+' MB';
 // nowe pola od razu do pisania (tryb edycji ustawia contenteditable tylko przy włączeniu)
 const writable=el=>{el.querySelectorAll('[data-ph]').forEach(x=>{if(editing())x.setAttribute('contenteditable','true')})};
 const addBtn=(label,after,fn)=>{const b=document.createElement('button');b.type='button';b.className='li-add';b.dataset.ui='';
  b.innerHTML='<span aria-hidden="true">+</span> '+label;b.onclick=fn;after.after(b);return b};
 const xBtn=(item,label,onRemove)=>{if(item.querySelector(':scope > .li-x'))return;const b=document.createElement('button');b.type='button';b.className='li-x';b.dataset.ui='';
  b.setAttribute('aria-label',label);b.title=label;b.innerHTML=X;b.onclick=e=>{e.preventDefault();e.stopPropagation();item.remove();onRemove&&onRemove()};item.appendChild(b)};
 const upload=async(file,name)=>WP?(await WP.upload(file,name)).url:URL.createObjectURL(file);

 // --- spotkania w tygodniu i grupy: dodaj / usuń pozycję ---
 function list(box,after,label,tpl,xlabel){if(!box)return;
  const deco=()=>[...box.children].forEach(it=>xBtn(it,xlabel));deco();
  addBtn(label,after,()=>{box.insertAdjacentHTML('beforeend',tpl);const it=box.lastElementChild;xBtn(it,xlabel);writable(it);it.querySelector('[data-ph]').focus()})}
 list(document.querySelector('.weekly dl'),document.querySelector('.weekly dl'),'Dodaj spotkanie',
  '<div><dt data-ph="Nazwa spotkania"></dt><dd data-ph="dzień, godzina, miejsce"></dd></div>','Usuń spotkanie');
 list(document.querySelector('.groups ul'),document.querySelector('.groups ul'),'Dodaj grupę',
  '<li><b data-ph="Nazwa grupy"></b> <span data-ph="kiedy się spotyka"></span></li>','Usuń grupę');

 // --- kalendarz wydarzeń: data z kalendarzyka, sortowanie, minione znikają ---
 const days=document.querySelector('.days');
 if(days){
  const t0=()=>{const t=new Date();t.setHours(0,0,0,0);return t};
  const dateOf=li=>{const v=li.querySelector('time')?.getAttribute('datetime');return v?new Date(v+'T00:00'):null};
  const setDate=(li,d)=>{const t=li.querySelector('time');t.setAttribute('datetime',iso(d));t.innerHTML=`<b>${d.getDate()}</b> ${MS[d.getMonth()]}`};
  const sort=()=>[...days.children].sort((a,b)=>(dateOf(a)||0)-(dateOf(b)||0)).forEach(li=>days.appendChild(li));
  const pastHide=()=>[...days.children].forEach(li=>{const d=dateOf(li);li.hidden=!editing()&&!!d&&d<t0();li.classList.toggle('was',!!d&&d<t0())});
  const deco=li=>{xBtn(li,'Usuń wydarzenie',pastHide);if(li.querySelector('.cal-date'))return;
   const inp=document.createElement('input');inp.type='date';inp.className='cal-date';inp.dataset.ui='';inp.setAttribute('aria-label','Data wydarzenia');
   inp.value=li.querySelector('time')?.getAttribute('datetime')||'';
   inp.onchange=()=>{if(!inp.value)return;setDate(li,new Date(inp.value+'T00:00'));sort();pastHide()};(li.querySelector(':scope > div')||li).prepend(inp)};
  [...days.children].forEach(deco);
  const empty=document.createElement('p');empty.className='cal-empty';days.after(empty);
  const upd=()=>{pastHide();const n=[...days.children].filter(li=>!li.hidden).length;empty.hidden=n>0;empty.textContent='Na razie brak zapowiedzianych wydarzeń.'};
  addBtn('Dodaj wydarzenie',empty,()=>{const d=t0();d.setDate(d.getDate()+7);
   days.insertAdjacentHTML('beforeend','<li><time></time><div><h3 data-ph="Nazwa wydarzenia"></h3><p data-ph="godzina, miejsce, kilka słów"></p></div></li>');
   const li=days.lastElementChild;setDate(li,d);deco(li);writable(li);sort();upd();li.querySelector('h3').focus()});
  new MutationObserver(upd).observe(document.body,{attributes:true,attributeFilter:['class']});upd();
  // ogłoszenia parafialne: jeden plik, podmieniany co tydzień
  const ann=document.querySelector('.ann');
  if(ann){const f=document.createElement('input');f.type='file';f.accept='.pdf,.doc,.docx,.odt';f.hidden=true;ann.after(f);
   const b=addBtn('Wgraj nowe ogłoszenia (plik)',f,()=>f.click());
   f.onchange=async()=>{const file=f.files[0];f.value='';if(!file)return;b.disabled=true;const old=b.innerHTML;b.textContent='Wysyłanie…';
    try{const url=await upload(file);const d=new Date(),ext=file.name.split('.').pop().toUpperCase();
     ann.innerHTML=`<h3>Ogłoszenia parafialne</h3><a class="doc-n" href="${esc(url)}" target="_blank" rel="noopener">Ogłoszenia parafialne</a><span class="doc-m">${ext}, ${size(file.size)} · dodane ${d.getDate()} ${MS[d.getMonth()]} ${d.getFullYear()}</span>`}
    catch(e){alert('Nie udało się wysłać pliku: '+e.message)}finally{b.disabled=false;b.innerHTML=old}}}}

 // --- galeria: albumy ze zdjęciami ---
 const albums=document.querySelector('.albums');
 if(albums){
  const photos=a=>{try{const p=JSON.parse(a.dataset.photos||'[]');if(p.length)return p}catch(e){}const i=a.querySelector('.ph img');return i?[i.getAttribute('src')]:[]};
  // zdjęcia z telefonu bywają ogromne: zmniejszamy przed wysłaniem
  const shrink=async(file,max=1800)=>{try{const bmp=await createImageBitmap(file,{imageOrientation:'from-image'});const s=Math.min(1,max/Math.max(bmp.width,bmp.height));
   const c=document.createElement('canvas');c.width=Math.round(bmp.width*s);c.height=Math.round(bmp.height*s);c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);
   return await new Promise(r=>c.toBlob(r,'image/jpeg',.86))}catch(e){return file}};
  const addPhotos=async(a,files,stat)=>{const list=photos(a).slice(),imgs=[...files].filter(f=>/^image\//.test(f.type));
   for(let i=0;i<imgs.length;i++){stat(`Wysyłanie zdjęć: ${i+1} z ${imgs.length}…`);const b=await shrink(imgs[i]);list.push(await upload(b,'galeria.jpg'))}
   a.dataset.photos=JSON.stringify(list);const ph=a.querySelector('.ph');if(list.length&&!ph.querySelector('img'))ph.innerHTML=`<img src="${esc(list[0])}" alt="" loading="lazy">`;
   const sm=a.querySelector('small');sm.textContent=sm.dataset.base||sm.textContent;stat('')};
  const pick=fn=>{const f=document.createElement('input');f.type='file';f.accept='image/*';f.multiple=true;f.onchange=()=>fn(f.files);f.click()};
  const deco=a=>{xBtn(a,'Usuń album');if(a.querySelector('.al-more'))return;const m=document.createElement('button');m.type='button';m.className='al-more';m.dataset.ui='';
   m.textContent='+ zdjęcia';m.onclick=e=>{e.preventDefault();e.stopPropagation();pick(fs=>{const sm=a.querySelector('small');sm.dataset.base=sm.textContent;
    addPhotos(a,fs,t=>{if(t)sm.textContent=t}).catch(er=>alert('Nie udało się wysłać zdjęć: '+er.message))})};a.appendChild(m)};
  [...albums.children].forEach(deco);
  addBtn('Dodaj album',albums,()=>pick(async fs=>{const d=new Date();
   albums.insertAdjacentHTML('afterbegin',`<a class="album" href="#"><div class="ph"></div><span data-ph="Nazwa albumu"></span><small>${MN[d.getMonth()]} ${d.getFullYear()}</small></a>`);
   const a=albums.firstElementChild,sm=a.querySelector('small');sm.dataset.base=sm.textContent;deco(a);writable(a);a.querySelector('span').focus();
   try{await addPhotos(a,fs,t=>{if(t)sm.textContent=t})}catch(er){alert('Nie udało się wysłać zdjęć: '+er.message)}}));
  // przeglądarka zdjęć albumu
  albums.addEventListener('click',e=>{const a=e.target.closest('.album');if(!a)return;e.preventDefault();if(editing()||e.target.closest('[data-ui]'))return;
   const p=photos(a);if(p.length)lightbox(p,a.querySelector('span')?.textContent||'')});
  function lightbox(list,title){let i=0;const L=document.createElement('div');L.className='glb';L.setAttribute('role','dialog');L.setAttribute('aria-label',title);
   L.innerHTML=`<div class="glb-h"><p><b>${esc(title)}</b><span class="glb-n"></span></p><button type="button" class="glb-x">Zamknij</button></div><img alt=""><button type="button" class="glb-b glb-p" aria-label="Poprzednie zdjęcie"><svg class="ico" viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" class="glb-b glb-nx" aria-label="Następne zdjęcie"><svg class="ico" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>`;
   const img=L.querySelector('img'),show=()=>{img.src=list[i];L.querySelector('.glb-n').textContent=list.length>1?`${i+1} z ${list.length}`:'';L.querySelectorAll('.glb-b').forEach(b=>b.hidden=list.length<2)};
   const go=n=>{i=(i+n+list.length)%list.length;show()},close=()=>{L.remove();removeEventListener('keydown',key);document.documentElement.style.overflow=''};
   const key=e=>{if(e.key==='Escape')close();else if(e.key==='ArrowLeft')go(-1);else if(e.key==='ArrowRight')go(1)};
   L.querySelector('.glb-x').onclick=close;L.querySelector('.glb-p').onclick=()=>go(-1);L.querySelector('.glb-nx').onclick=()=>go(1);
   let sx=0;img.addEventListener('touchstart',e=>sx=e.touches[0].clientX,{passive:true});img.addEventListener('touchend',e=>{const dx=e.changedTouches[0].clientX-sx;if(Math.abs(dx)>50)go(dx<0?1:-1)});
   addEventListener('keydown',key);document.body.appendChild(L);document.documentElement.style.overflow='hidden';show();L.querySelector('.glb-x').focus()}}
})();
