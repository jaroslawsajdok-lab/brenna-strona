// ===== aktualności: lista wpisów, przeglądarka zdjęć i okno edycji wpisu =====
// W prototypie wpisy żyją w pamięci strony. W WordPressie ten sam obiekt {title,date,html,main,gallery}
// trafi przez REST API do bazy, a zdjęcia do biblioteki mediów.
(function(){
const sec=document.getElementById('aktualnosci');if(!sec)return;
const MON=['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia'];
const fmtD=iso=>{const [y,m,d]=iso.split('-').map(Number);return d+' '+MON[m-1]+' '+y};
const todayISO=()=>{const d=new Date(),z=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+z(d.getMonth()+1)+'-'+z(d.getDate())};
const esc=s=>String(s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const clone=o=>JSON.parse(JSON.stringify(o));
let uid=0;

// --- wpisy obecne w HTML zamieniamy na dane ---
const more=sec.querySelector('.more');
let posts=[...sec.querySelectorAll('article.post')].map(a=>{const im=a.querySelector('.ph img');
 const p={id:++uid,title:a.querySelector('h3').textContent.trim(),date:a.querySelector('time').getAttribute('datetime'),
  html:[...a.querySelectorAll('p')].map(x=>'<p>'+x.innerHTML+'</p>').join(''),main:im?{src:im.getAttribute('src'),fx:50,fy:50}:null,gallery:[]};
 a.remove();return p});
// WordPress: wpisy z bazy (każdy ma wp – numer wpisu; zdjęcia mają id w bibliotece mediów)
const WP=window.PARAFIA;
if(WP&&Array.isArray(WP.posts))posts=WP.posts.map(x=>({...x,id:++uid}));
const lead=sec.querySelector('.lead');
const addBtn=document.createElement('button');addBtn.type='button';addBtn.className='addpost';addBtn.innerHTML='<span aria-hidden="true">+</span> Dodaj aktualność';
(lead||sec.querySelector('h2')).after(addBtn);
const SHOW=4;

function cardHTML(p,prev){
 const all=(p.main?[p.main]:[]).concat(p.gallery),g=p.gallery,vis=g.slice(0,4),rest=g.length-vis.length;
 const ph=p.main?`<${prev?'div':'button type="button"'} class="ph" data-i="0" ${prev?'':`aria-label="Zobacz zdjęcia (${all.length}): ${esc(p.title)}"`}><img src="${p.main.src}" alt="" style="object-position:${p.main.fx}% ${p.main.fy}%"></${prev?'div':'button'}>`:'<div class="ph" aria-hidden="true"></div>';
 const gal=vis.length?`<ul class="pgal">${vis.map((x,i)=>`<li><${prev?'span':'button type="button"'} class="pgb" data-i="${i+(p.main?1:0)}" ${prev?'':`aria-label="Zdjęcie ${i+(p.main?2:1)} z ${all.length}"`}><img src="${x.src}" alt="">${i===vis.length-1&&rest>0?`<span class="n">+${rest}</span>`:''}</${prev?'span':'button'}></li>`).join('')}</ul>`:'';
 return `<article class="post" data-id="${p.id}">${ph}<time datetime="${p.date}">${fmtD(p.date)}</time><h3>${esc(p.title)||'<span style="color:#8a8c85">Tytuł wpisu</span>'}</h3><div class="ptext">${p.html||'<p style="color:#8a8c85">Treść wpisu…</p>'}</div>${prev?'':'<button type="button" class="pmore" aria-expanded="false">Czytaj dalej</button>'}${gal}${prev?'':'<button type="button" class="pedit"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4"/></svg> Edytuj wpis</button>'}</article>`}
function render(flashId){
 sec.querySelectorAll('article.post').forEach(a=>a.remove());
 posts.sort((a,b)=>b.date.localeCompare(a.date)||b.id-a.id);
 more.insertAdjacentHTML('beforebegin',posts.slice(0,SHOW).map(p=>cardHTML(p)).join(''));
 sec.querySelectorAll('article.post').forEach(a=>{const t=a.querySelector('.ptext');if(t.scrollHeight>t.clientHeight+4)a.classList.add('long')});
 if(flashId){const a=sec.querySelector(`.post[data-id="${flashId}"]`);if(a){a.classList.add('flash');a.scrollIntoView({block:'center',behavior:'smooth'})}}}
render();

// --- kliknięcia na liście ---
sec.addEventListener('click',e=>{const a=e.target.closest('article.post');if(!a||a.closest('.ped'))return;const p=posts.find(x=>x.id==a.dataset.id);if(!p)return;
 const pic=e.target.closest('[data-i]');if(pic){lightbox(p,+pic.dataset.i,pic);return}
 if(e.target.closest('.pmore')){const o=a.classList.toggle('open');e.target.textContent=o?'Zwiń':'Czytaj dalej';e.target.setAttribute('aria-expanded',o);return}
 if(e.target.closest('.pedit'))openEditor(p)});
addBtn.addEventListener('click',()=>openEditor(null));

// --- przeglądarka zdjęć ---
function lightbox(p,i,back){const all=(p.main?[p.main]:[]).concat(p.gallery);if(!all.length)return;
 const L=document.createElement('div');L.className='lbx';L.setAttribute('role','dialog');L.setAttribute('aria-modal','true');L.setAttribute('aria-label','Zdjęcia: '+p.title);
 L.innerHTML=`<img alt=""><div class="lb-cap"></div><button type="button" class="lb-x" aria-label="Zamknij"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>${all.length>1?'<button type="button" class="lb-p" aria-label="Poprzednie"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" class="lb-n" aria-label="Następne"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>':''}`;
 const img=L.querySelector('img'),cap=L.querySelector('.lb-cap');
 const show=()=>{i=(i+all.length)%all.length;img.src=all[i].src;cap.textContent=`${p.title} · ${i+1} / ${all.length}`};
 const close=()=>{L.remove();removeEventListener('keydown',key);document.documentElement.style.overflow='';back&&back.focus()};
 const key=e=>{if(e.key==='Escape')close();else if(e.key==='ArrowRight'){i++;show()}else if(e.key==='ArrowLeft'){i--;show()}};
 L.addEventListener('click',e=>{if(e.target.closest('.lb-x')||e.target===L)close();else if(e.target.closest('.lb-p')){i--;show()}else if(e.target.closest('.lb-n')){i++;show()}});
 let x0=null;L.addEventListener('touchstart',e=>{x0=e.touches[0].clientX},{passive:true});L.addEventListener('touchend',e=>{if(x0==null)return;const d=e.changedTouches[0].clientX-x0;if(Math.abs(d)>50){i+=d<0?1:-1;show()}x0=null});
 addEventListener('keydown',key);document.body.appendChild(L);document.documentElement.style.overflow='hidden';show();L.querySelector('.lb-x').focus()}

// --- zdjęcia z telefonu bywają ogromne: zmniejszamy przed dodaniem ---
let busyN=0;const busy=d=>{busyN+=d;const b=D.querySelector('.ped-ok');if(b){b.disabled=busyN>0;msg.textContent=busyN>0?'Chwileczkę, przygotowuję zdjęcia…':''}};
async function shrink(file,max=1800){busy(1);
 try{const bmp=await createImageBitmap(file,{imageOrientation:'from-image'});const s=Math.min(1,max/Math.max(bmp.width,bmp.height));
  const c=document.createElement('canvas');c.width=Math.round(bmp.width*s);c.height=Math.round(bmp.height*s);c.getContext('2d').drawImage(bmp,0,0,c.width,c.height);
  const b=await new Promise(r=>c.toBlob(r,'image/jpeg',.86));return URL.createObjectURL(b)}
 catch(e){return URL.createObjectURL(file)}
 finally{busy(-1)}}
const imgs=list=>[...list].filter(f=>/^image\//.test(f.type));

// --- okno edycji ---
const D=document.createElement('dialog');D.className='ped';D.setAttribute('aria-labelledby','ped-h');
D.innerHTML=`<form class="ped-in" novalidate>
 <header class="ped-top"><h2 id="ped-h">Nowa aktualność</h2><button type="button" class="ped-x" aria-label="Zamknij okno"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button></header>
 <div class="ped-body">
  <div class="ped-form">
   <div class="ped-row">
    <label class="ped-f ped-title"><span>Tytuł</span><input type="text" name="title" maxlength="140" placeholder="np. Koncert w kościele w Brennej" autocomplete="off"></label>
    <label class="ped-f"><span>Data</span><input type="date" name="date"></label>
   </div>
   <div class="ped-f"><span class="ped-l" id="ped-ml">Zdjęcie główne</span>
    <div class="ped-main" tabindex="0" role="button" aria-labelledby="ped-ml"></div>
    <p class="ped-hint ped-mhint">To zdjęcie widać na liście aktualności. Możesz je też przeciągnąć z pulpitu.</p>
   </div>
   <div class="ped-f"><span class="ped-l" id="ped-tl">Treść</span>
    <div class="ped-tools" role="toolbar" aria-label="Formatowanie">
     <button type="button" data-c="bold" aria-label="Pogrubienie" title="Pogrubienie"><b>B</b></button>
     <button type="button" data-c="italic" aria-label="Kursywa" title="Kursywa"><i>I</i></button>
     <button type="button" data-c="insertUnorderedList">• Lista</button>
     <button type="button" data-c="link">Link</button>
    </div>
    <div class="ped-linkbar" hidden><input type="url" placeholder="https://adres-strony.pl" aria-label="Adres linku"><button type="button" class="ped-btn ped-lok">Wstaw link</button><button type="button" class="ped-btn ped-lno">Anuluj</button></div>
    <div class="ped-text" contenteditable="true" role="textbox" aria-multiline="true" aria-labelledby="ped-tl" data-ph="Napisz, co się wydarzy albo co się wydarzyło. Tekst wklejony z Worda lub maila zostanie oczyszczony z formatowania."></div>
   </div>
   <div class="ped-f"><span class="ped-l">Galeria <small>– dodatkowe zdjęcia, nieobowiązkowe</small></span>
    <ul class="ped-gal"></ul>
    <p class="ped-hint">Kolejność zmienisz strzałkami albo przeciągając. Gwiazdka ustawia zdjęcie jako główne.</p>
   </div>
  </div>
  <aside class="ped-prev" aria-label="Podgląd"><span class="ped-l">Tak wpis będzie wyglądał</span><div class="ped-card"></div><p class="ped-sum"></p></aside>
 </div>
 <footer class="ped-foot"><button type="button" class="ped-del">Usuń wpis</button><span class="ped-msg" role="status" aria-live="polite"></span><button type="button" class="ped-cancel">Anuluj</button><button type="submit" class="ped-ok">Opublikuj</button></footer>
 <div class="ped-confirm" hidden><div role="alertdialog" aria-modal="true" aria-labelledby="ped-cq"><p id="ped-cq"></p><div class="cbtns"><button type="button" class="ped-cancel c-no"></button><button type="button" class="ped-ok c-yes"></button></div></div></div>
</form>
<input type="file" accept="image/*" class="f-main" hidden><input type="file" accept="image/*" multiple class="f-gal" hidden>`;
document.body.appendChild(D);
const $=s=>D.querySelector(s),fT=$('[name=title]'),fD=$('[name=date]'),mainZ=$('.ped-main'),txt=$('.ped-text'),galU=$('.ped-gal'),msg=$('.ped-msg'),card=$('.ped-card'),sum=$('.ped-sum');
let cur=null,orig='',editing=null,dragI=null;
const snap=()=>JSON.stringify({t:fT.value,d:fD.value,h:txt.innerHTML,m:cur.main,g:cur.gallery});

function openEditor(p){editing=p;cur=p?clone(p):{id:0,title:'',date:todayISO(),html:'',main:null,gallery:[]};
 $('#ped-h').textContent=p?'Edycja aktualności':'Nowa aktualność';$('.ped-ok').textContent=p?'Zapisz zmiany':'Opublikuj';$('.ped-del').hidden=!p;
 fT.value=cur.title;fD.value=cur.date;txt.innerHTML=cur.html;msg.textContent='';$('.ped-title').classList.remove('bad');$('.ped-linkbar').hidden=true;$('.ped-confirm').hidden=true;
 drawMain();drawGal();preview();orig=snap();D.showModal();document.documentElement.style.overflow='hidden';setTimeout(()=>fT.focus(),30)}
function shut(){D.close();document.documentElement.style.overflow=''}
function ask(q,yes,no,cb,danger){const C=$('.ped-confirm');C.hidden=false;$('#ped-cq').textContent=q;const y=$('.c-yes'),n=$('.c-no');y.textContent=yes;n.textContent=no;y.classList.toggle('danger',!!danger);
 y.onclick=()=>{C.hidden=true;cb()};n.onclick=()=>{C.hidden=true};n.focus()}
const tryClose=()=>{if(snap()!==orig)ask('Zamknąć bez zapisywania zmian?','Zamknij','Wróć do edycji',shut,true);else shut()};
D.addEventListener('cancel',e=>{e.preventDefault();if(!$('.ped-confirm').hidden){$('.ped-confirm').hidden=true;return}tryClose()});
$('.ped-x').onclick=tryClose;$('.ped-foot .ped-cancel').onclick=tryClose;
$('.ped-del').onclick=()=>ask('Usunąć ten wpis ze strony?','Usuń wpis','Nie usuwaj',()=>{const gone=editing;posts=posts.filter(x=>x.id!==gone.id);shut();render();toast('Wpis usunięty');
 if(WP&&gone.wp)WP.call('posts/'+gone.wp,{method:'DELETE'}).catch(e=>toast('Nie usunięto z bazy: '+e.message))},true);

// zdjęcie główne
const ICON='<svg viewBox="0 0 54 54" aria-hidden="true"><rect x="5" y="11" width="44" height="33" rx="3"/><circle cx="19" cy="22" r="4.5"/><path d="M5 38 L19 28 L28 35 L37 26 L49 36"/></svg>';
function drawMain(busy){const m=cur.main;mainZ.classList.toggle('has',!!m);
 $('.ped-mhint').textContent=m?'Kliknij na zdjęciu miejsce, które ma być zawsze widoczne w kadrze miniatury.':'To zdjęcie widać na liście aktualności. Możesz je też przeciągnąć z pulpitu.';
 mainZ.setAttribute('aria-label',m?'Zdjęcie główne – kliknij, aby ustawić środek kadru':'Dodaj zdjęcie główne');
 mainZ.innerHTML=(m?`<img src="${m.src}" alt=""><span class="ped-dot" style="left:${m.fx}%;top:${m.fy}%"></span><div class="ped-mbar"><button type="button" class="m-ch">Zmień zdjęcie</button><button type="button" class="m-rm">Usuń</button></div>`
  :`<div class="ped-empty">${ICON}<b>Dodaj zdjęcie główne</b>Kliknij tutaj, aby wybrać zdjęcie z komputera lub telefonu</div>`)+(busy?'<div class="ped-busy">Przygotowuję zdjęcie…</div>':'');
 if(m){const im=mainZ.querySelector('img'),dot=mainZ.querySelector('.ped-dot');const place=()=>{const r=fitRect(im);dot.style.left=(r.x+r.w*m.fx/100)+'px';dot.style.top=(r.y+r.h*m.fy/100)+'px'};im.complete?place():im.onload=place}}
function fitRect(im){const W=im.clientWidth,H=im.clientHeight,iw=im.naturalWidth||1,ih=im.naturalHeight||1,s=Math.min(W/iw,H/ih);return{x:(W-iw*s)/2,y:(H-ih*s)/2,w:iw*s,h:ih*s}}
mainZ.addEventListener('click',e=>{if(e.target.closest('.m-ch')){$('.f-main').click();return}
 if(e.target.closest('.m-rm')){cur.main=cur.gallery.shift()||null;drawMain();drawGal();preview();return}
 if(!cur.main){$('.f-main').click();return}
 const im=mainZ.querySelector('img'),r=fitRect(im),b=im.getBoundingClientRect();
 cur.main.fx=Math.round(Math.max(0,Math.min(100,(e.clientX-b.left-r.x)/r.w*100)));cur.main.fy=Math.round(Math.max(0,Math.min(100,(e.clientY-b.top-r.y)/r.h*100)));drawMain();preview()});
mainZ.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target===mainZ){e.preventDefault();$('.f-main').click()}});
async function setMain(f){if(!f)return;drawMain(true);const src=await shrink(f);cur.main={src,fx:50,fy:50};drawMain();preview()}
$('.f-main').onchange=e=>{const f=imgs(e.target.files)[0];e.target.value='';if(f){if(cur.main)cur.main=null;setMain(f)}};
['dragover','dragenter'].forEach(ev=>mainZ.addEventListener(ev,e=>{if(e.dataTransfer.types.includes('Files')){e.preventDefault();mainZ.classList.add('over')}}));
['dragleave','drop'].forEach(ev=>mainZ.addEventListener(ev,()=>mainZ.classList.remove('over')));
mainZ.addEventListener('drop',e=>{const fs=imgs(e.dataTransfer.files);if(!fs.length)return;e.preventDefault();cur.main=null;setMain(fs[0]);if(fs.length>1)addGal(fs.slice(1))});

// galeria
function drawGal(){const g=cur.gallery,n=g.length;
 galU.innerHTML=g.map((x,i)=>`<li draggable="true" data-i="${i}"><img src="${x.src}" alt=""><span class="g-no">${i+1}</span><div class="g-bar">
  <button type="button" class="g-l" aria-label="Przesuń wcześniej" ${i?'':'disabled style="visibility:hidden"'}><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button><button type="button" class="g-st" aria-label="Ustaw jako zdjęcie główne" title="Ustaw jako zdjęcie główne"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1L3.2 9.5l6.1-.9z"/></svg></button><button type="button" class="g-rm" aria-label="Usuń zdjęcie" title="Usuń zdjęcie"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button><button type="button" class="g-r" aria-label="Przesuń dalej" ${i<n-1?'':'disabled style="visibility:hidden"'}><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button></div></li>`).join('')
  +`<li class="add" tabindex="0" role="button" aria-label="Dodaj zdjęcia do galerii"><div><span aria-hidden="true">+</span>Dodaj zdjęcia</div></li>`}
galU.addEventListener('click',e=>{if(e.target.closest('li.add')){$('.f-gal').click();return}
 const li=e.target.closest('li[data-i]');if(!li)return;const i=+li.dataset.i,g=cur.gallery;
 if(e.target.closest('.g-rm'))g.splice(i,1);
 else if(e.target.closest('.g-l')&&i>0)[g[i-1],g[i]]=[g[i],g[i-1]];
 else if(e.target.closest('.g-r')&&i<g.length-1)[g[i+1],g[i]]=[g[i],g[i+1]];
 else if(e.target.closest('.g-st')){const x=g.splice(i,1)[0];if(cur.main)g.unshift(cur.main);cur.main={src:x.src,fx:50,fy:50};drawMain()}
 else return;
 drawGal();preview();const again=galU.querySelector(`li[data-i="${Math.min(i,cur.gallery.length-1)}"] .g-st`);again&&again.focus()});
galU.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('li.add')){e.preventDefault();$('.f-gal').click()}});
async function addGal(fs){const add=galU.querySelector('li.add');add.innerHTML='<div>Przygotowuję zdjęcia…</div>';
 for(const f of fs)cur.gallery.push({src:await shrink(f,1600)});if(!cur.main&&cur.gallery.length){const x=cur.gallery.shift();cur.main={src:x.src,fx:50,fy:50};drawMain()}drawGal();preview()}
$('.f-gal').onchange=e=>{const fs=imgs(e.target.files);e.target.value='';if(fs.length)addGal(fs)};
galU.addEventListener('dragstart',e=>{const li=e.target.closest('li[data-i]');if(!li)return;dragI=+li.dataset.i;li.classList.add('drag');e.dataTransfer.effectAllowed='move';e.dataTransfer.setData('text/plain','x')});
galU.addEventListener('dragend',()=>{dragI=null;galU.querySelectorAll('.drag,.tgt,.over').forEach(x=>x.classList.remove('drag','tgt','over'))});
galU.addEventListener('dragover',e=>{const li=e.target.closest('li');if(!li)return;
 if(dragI==null){if(e.dataTransfer.types.includes('Files')){e.preventDefault();galU.querySelector('li.add').classList.add('over')}return}
 e.preventDefault();galU.querySelectorAll('.tgt').forEach(x=>x.classList.remove('tgt'));li.classList.add('tgt')});
galU.addEventListener('drop',e=>{e.preventDefault();galU.querySelector('li.add')?.classList.remove('over');
 if(dragI==null){const fs=imgs(e.dataTransfer.files);if(fs.length)addGal(fs);return}
 const li=e.target.closest('li'),g=cur.gallery,x=g.splice(dragI,1)[0];let to=li&&li.dataset.i!=null?+li.dataset.i:g.length+1;if(to>dragI)to--;g.splice(to,0,x);dragI=null;drawGal();preview()});

// treść: prosty edytor, wklejanie bez obcego formatowania
let range=null;
$('.ped-tools').addEventListener('mousedown',e=>{if(e.target.closest('button'))e.preventDefault()});
$('.ped-tools').addEventListener('click',e=>{const b=e.target.closest('button');if(!b)return;txt.focus();
 if(b.dataset.c==='link'){const s=getSelection();range=s.rangeCount?s.getRangeAt(0).cloneRange():null;const lb=$('.ped-linkbar');lb.hidden=false;lb.querySelector('input').value='';lb.querySelector('input').focus();return}
 document.execCommand(b.dataset.c,false,null);tools();preview()});
const doLink=()=>{let u=$('.ped-linkbar input').value.trim();$('.ped-linkbar').hidden=true;txt.focus();if(!u)return;if(!/^(https?:|mailto:|tel:)/i.test(u))u='https://'+u;
 const s=getSelection();if(range){s.removeAllRanges();s.addRange(range)}
 if(s.isCollapsed)document.execCommand('insertHTML',false,`<a href="${esc(u)}">${esc(u.replace(/^https?:\/\//,''))}</a>`);else document.execCommand('createLink',false,u);preview()};
$('.ped-lok').onclick=doLink;$('.ped-lno').onclick=()=>{$('.ped-linkbar').hidden=true;txt.focus()};
$('.ped-linkbar input').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();doLink()}});
txt.addEventListener('paste',e=>{e.preventDefault();const t=(e.clipboardData||window.clipboardData).getData('text/plain');
 const html=t.replace(/\r/g,'').split(/\n{2,}/).map(par=>'<p>'+esc(par).replace(/\n/g,'<br>')+'</p>').join('');document.execCommand('insertHTML',false,html);preview()});
txt.addEventListener('input',()=>{if(txt.innerHTML==='<br>')txt.innerHTML='';preview()});
const tools=()=>D.querySelectorAll('.ped-tools [data-c]').forEach(b=>{if(b.dataset.c!=='link')try{b.setAttribute('aria-pressed',document.queryCommandState(b.dataset.c))}catch(e){}});
document.addEventListener('selectionchange',()=>{if(D.open&&D.contains(document.activeElement))tools()});
function clean(html){const box=document.createElement('div');box.innerHTML=html;const OK={P:1,B:1,STRONG:1,I:1,EM:1,UL:1,OL:1,LI:1,A:1,BR:1};
 const walk=n=>{[...n.childNodes].forEach(c=>{if(c.nodeType===3)return;if(c.nodeType!==1){c.remove();return}walk(c);
  if(c.tagName==='DIV'){const p=document.createElement('p');p.innerHTML=c.innerHTML;c.replaceWith(p);return}
  if(!OK[c.tagName]){c.replaceWith(...c.childNodes);return}
  [...c.attributes].forEach(a=>{if(!(c.tagName==='A'&&a.name==='href'))c.removeAttribute(a.name)});
  if(c.tagName==='A'&&!/^(https?:|mailto:|tel:)/i.test(c.getAttribute('href')||''))c.replaceWith(...c.childNodes)})};
 walk(box);[...box.childNodes].forEach(c=>{if(c.nodeType===3&&c.textContent.trim()){const p=document.createElement('p');c.replaceWith(p);p.appendChild(c)}});
 return box.innerHTML.replace(/<p>(\s|<br>)*<\/p>/g,'').trim()}

// podgląd na żywo
fT.addEventListener('input',()=>{$('.ped-title').classList.remove('bad');msg.textContent='';preview()});fD.addEventListener('input',preview);
function preview(){const p={...cur,title:fT.value.trim(),date:fD.value||todayISO(),html:clean(txt.innerHTML)};card.innerHTML=cardHTML(p,true);
 const n=(p.main?1:0)+p.gallery.length;sum.textContent=n?`Zdjęć we wpisie: ${n}. Po kliknięciu w miniaturę otworzą się w powiększeniu.`:'Wpis bez zdjęć też się opublikuje, ale ze zdjęciem wygląda lepiej.'}

// zapis
$('.ped-in').addEventListener('submit',e=>{e.preventDefault();const title=fT.value.trim();
 if(!title){$('.ped-title').classList.add('bad');msg.textContent='Wpisz tytuł wpisu.';fT.focus();return}
 const p={...cur,title,date:fD.value||todayISO(),html:clean(txt.innerHTML)};
 if(editing){Object.assign(editing,p)}else{p.id=++uid;posts.push(p)}
 const saved=editing||p;shut();render(p.id||editing.id);
 if(!WP){toast(editing?'Zmiany zapisane':'Wpis opublikowany');return}
 toast('Zapisywanie wpisu…');persist(saved).then(()=>toast(editing?'Zmiany zapisane':'Wpis opublikowany')).catch(e=>toast('Nie zapisano: '+e.message))});
// WordPress: nowe zdjęcia (adresy blob:) do biblioteki mediów, potem wpis do bazy
async function persist(p){
 const up=async im=>{if(!im||!/^blob:/.test(im.src))return im;const b=await (await fetch(im.src)).blob();const m=await WP.upload(b,'zdjecie.jpg');return {...im,src:m.url,mid:m.id}};
 p.main=await up(p.main);p.gallery=await Promise.all((p.gallery||[]).map(up));
 const r=await WP.call('posts',{body:{wp:p.wp||0,title:p.title,date:p.date,html:p.html,
  main:p.main?{id:p.main.mid||0,src:p.main.src,fx:p.main.fx,fy:p.main.fy}:null,gallery:(p.gallery||[]).map(g=>g.mid||0).filter(Boolean)}});
 p.wp=r.wp;render()}
function toast(t){const el=document.createElement('div');el.className='ped-toast';el.setAttribute('role','status');el.textContent=t;document.body.appendChild(el);setTimeout(()=>el.remove(),3100)}
})();
