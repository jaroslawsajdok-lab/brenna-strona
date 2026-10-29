import re
h=open('naglowek-kompakt.html',encoding='utf-8').read()
content=open('page_content.html',encoding='utf-8').read()
css=open('page_style.css',encoding='utf-8').read()

# tytuł i fonty
h=h.replace('<title>Brenna-Górki – nagłówek kompaktowy</title>','<title>Parafia Ewangelicko-Augsburska Brenna-Górki</title>',1)
h=h.replace('family=PT+Sans:wght@400;700','family=PT+Sans:wght@400;700&family=PT+Sans+Narrow:wght@700',1)

# treść strony zamiast opisu prototypu
h,n=re.subn(r'<p class="below">.*?</p>',lambda m:content,h,count=1,flags=re.S);assert n==1

# panele podglądu animacji -> zwijany panel w rogu
i=h.index('<div class="bar" role="group"');j=h.index('<script>',i)
ctrl=h[i:j]
h=h[:i]+'<details class="preview"><summary>Podgląd animacji: pora roku, święta, czas</summary>'+ctrl+'</details>\n<div class="editbar" role="status">Tryb edycji: kliknij tekst, aby go zmienić. <button type="button" id="editdone">Zakończ</button></div>\n'+h[j:]

# style strony
h=h.replace('<header id="hero">','<a class="skip" href="#tresc">Przejdź do treści</a><header id="hero"><h1 class="sr">Parafia Ewangelicko-Augsburska Brenna-Górki</h1>',1)
h=h.replace('</style></head>',css+'\n'+open('post_editor.css',encoding='utf-8').read()+'\n'+open('services_editor.css',encoding='utf-8').read()+'\n'+open('bottom.css',encoding='utf-8').read()+'\n'+open('calm.css',encoding='utf-8').read()+'\n</style></head>',1)

# skrypty strony
JS0=r'''
// ===== okno-rozeta: ornament kreślony w SVG =====
(function(){const s=document.querySelector('.tracery');if(!s)return;const NS='http://www.w3.org/2000/svg',mk=(t,a)=>{const e=document.createElementNS(NS,t);for(const k in a)e.setAttribute(k,a[k]);s.appendChild(e);return e};
 s.insertAdjacentHTML('afterbegin','<defs><pattern id="hatchg" width="2.4" height="20" patternUnits="userSpaceOnUse"><rect width=".7" height="20" fill="#24493a"/></pattern></defs>');mk('path',{class:'ring','fill-rule':'evenodd',d:'M-99,0a99,99 0 1,0 198,0a99,99 0 1,0 -198,0Z M-86,0a86,86 0 1,0 172,0a86,86 0 1,0 -172,0Z'});
 mk('circle',{class:'ln2',r:99});mk('circle',{class:'ln2',r:86});mk('circle',{class:'ln2',r:92.5,'stroke-dasharray':'1.5 2.5',opacity:.6});
 for(let i=0;i<24;i++){const a=i*Math.PI/12;mk('line',{class:'ln2',x1:Math.cos(a)*86,y1:Math.sin(a)*86,x2:Math.cos(a)*99,y2:Math.sin(a)*99})}
 for(let i=0;i<24;i++){const a=(i+.5)*Math.PI/12;mk('circle',{class:'foil',cx:Math.cos(a)*92.5,cy:Math.sin(a)*92.5,r:3.2})}
 // linia odniesienia do opisu, jak na rysunku
 mk('path',{class:'lead',d:'M-46,87.5 L-46,104'});mk('circle',{class:'ln2',cx:-46,cy:87.5,r:1.4,fill:'#1d1d1b'})})();
PANOJS
document.querySelector('.mapframe button')?.addEventListener('click',e=>{const f=e.target.parentElement;f.innerHTML=`<iframe src="${f.dataset.src}" title="Mapa dojazdu do kancelarii parafialnej" loading="lazy"></iframe>`});

// ===== pasek łączący: przykleja się i rozrasta po przewinięciu pod animację =====
(function(){const j=document.getElementById('joint');if(!j)return;const hero=document.getElementById('hero');
 document.getElementById('hero').id='hero';document.body.id=document.body.id||'top';
 new IntersectionObserver(es=>{j.classList.toggle('stuck',!es[0].isIntersecting)},{rootMargin:'-20px 0px 0px 0px'}).observe(hero);
 const btn=j.querySelector('.jmenu');btn.onclick=()=>{const o=j.classList.toggle('open');btn.setAttribute('aria-expanded',o)};
 j.querySelectorAll('.jnav a').forEach(a=>a.addEventListener('click',()=>{j.classList.remove('open');btn.setAttribute('aria-expanded',false)}));
 // podświetlenie aktualnego działu
 const links=[...j.querySelectorAll('.jnav a')],secs=links.map(a=>document.querySelector(a.getAttribute('href')));
 new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting){links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))}})},{rootMargin:'-45% 0px -50% 0px'}).observe&&secs.forEach(s=>s&&new IntersectionObserver(es=>{es.forEach(e=>{if(e.isIntersecting)links.forEach(a=>a.classList.toggle('on',a.getAttribute('href')==='#'+e.target.id))})},{rootMargin:'-45% 0px -50% 0px'}).observe(s))})();

// opóźnienia pojawiania się pozycji menu w pasku
document.querySelectorAll('.jnav a').forEach((a,i)=>{a.style.transitionDelay=(.35+i*.07)+'s';a.style.animationDelay=(.35+i*.07)+'s'});
// ===== oszczędzanie: to, czego nie widać, nie jest liczone ani rysowane =====
(function(){const hero=document.getElementById('hero');if(!hero)return;
 new IntersectionObserver(es=>{const v=es[0].isIntersecting;window.HERO_VIS=v;hero.classList.toggle('offscreen',!v)},{rootMargin:'40px'}).observe(hero)})();

// ===== podgląd „jak na telefonie”: strona otwiera się w ramce telefonu 390×844 =====
(function(){if(window.self!==window.top){document.documentElement.classList.add('in-phone');return}
 const b=document.createElement('button');b.className='phonebtn';b.type='button';b.textContent='Podgląd na telefonie';document.body.appendChild(b);
 let ov=null;
 b.onclick=()=>{if(ov){ov.remove();ov=null;b.textContent='Podgląd na telefonie';return}
  ov=document.createElement('div');ov.className='phoneov';
  ov.innerHTML=`<div class="phwrap"><div class="phone"><div class="notch"></div><iframe title="Strona na telefonie" src="${location.href.split('#')[0]}"></iframe></div></div>
   <div class="phonebar"><label>Model <select><option value="390x844">iPhone 13–15 (390×844)</option><option value="360x780">Android (360×780)</option><option value="375x667">iPhone SE (375×667)</option><option value="412x915">Duży Android (412×915)</option></select></label>
   <button type="button" class="phclose">Zamknij</button></div>`;
  document.body.appendChild(ov);document.documentElement.style.overflow='hidden';b.textContent='Zamknij podgląd';
  const ph=ov.querySelector('.phone'),wr=ov.querySelector('.phwrap'),sel=ov.querySelector('select');b.style.display='none';
  const fit=()=>{const [w,h]=sel.value.split('x').map(Number);ph.style.width=w+'px';ph.style.height=h+'px';
   const s=Math.min(1,(innerHeight-90)/(h+28),(innerWidth-40)/(w+28));ph.style.transform=`scale(${s})`;wr.style.width=(w+28)*s+'px';wr.style.height=(h+28)*s+'px'};
  sel.onchange=fit;fit();addEventListener('resize',fit);
  const close=()=>{ov.remove();ov=null;document.documentElement.style.overflow='';b.textContent='Podgląd na telefonie';b.style.display=''};
  ov.querySelector('.phclose').onclick=close;ov.addEventListener('click',e=>{if(e.target===ov)close()});
  addEventListener('keydown',function k(e){if(e.key==='Escape'&&ov){close();removeEventListener('keydown',k)}})};})();
'''
JS=JS0.replace('PANOJS',open('tour.js',encoding='utf-8').read()+'\n'+open('post_editor.js',encoding='utf-8').read()+'\n'+open('services_editor.js',encoding='utf-8').read()+'\n'+open('login.js',encoding='utf-8').read())
h=h.replace('</script>\n</body>',JS+'\n</script>\n</body>',1)
import base64
for k,f in [('DOOR_LEFT','door/left.webp'),('DOOR_RIGHT','door/right.webp'),('DOOR_RING','door/ring.webp')]:
    h=h.replace(k,'data:image/webp;base64,'+base64.b64encode(open(f,'rb').read()).decode(),1)
open('brenna-strona.html','w',encoding='utf-8').write(h)
print('ok',len(h)//1024,'KB')
