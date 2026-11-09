(function(){if(/podglad/.test(location.search+location.hash))document.documentElement.classList.add('dev')})();
// ===== stopka: las i logo =====
(function(){const t=document.querySelector('.ftrees');if(t){let s=7;const R=()=>(s=(s*9301+49297)%233280)/233280;let x=-10,g='';
 while(x<1610){const h=24+R()*34,w=h*.42,y=64;
  g+=`<path d="M${x.toFixed(1)},${y-h} L${(x+w*.55).toFixed(1)},${(y-h*.55).toFixed(1)} L${(x+w*.3).toFixed(1)},${(y-h*.55).toFixed(1)} L${(x+w*.75).toFixed(1)},${(y-h*.18).toFixed(1)} L${(x+w*.12).toFixed(1)},${(y-h*.18).toFixed(1)} L${(x+w*.12).toFixed(1)},${y} L${(x-w*.12).toFixed(1)},${y} L${(x-w*.12).toFixed(1)},${(y-h*.18).toFixed(1)} L${(x-w*.75).toFixed(1)},${(y-h*.18).toFixed(1)} L${(x-w*.3).toFixed(1)},${(y-h*.55).toFixed(1)} L${(x-w*.55).toFixed(1)},${(y-h*.55).toFixed(1)} Z"/>`;
  x+=w*.9+R()*(R()<.25?70:18)}
 t.innerHTML=`<svg viewBox="0 0 1600 64" preserveAspectRatio="xMidYMax slice"><g fill="#2f5d45" stroke="#1d1d1b" stroke-width="1.3" stroke-linejoin="round">${g}</g></svg>`}
 const l=document.querySelector('.flogo'),j=document.querySelector('.jmark svg');if(l&&j)l.appendChild(j.cloneNode(true))})();

// ===== logowanie i tryb edycji =====
// Prototyp: login „proboszcz”, hasło „brenna”. W WordPressie (window.PARAFIA) okno wysyła dane do wtyczki,
// która loguje przez wp_signon() („Zapamiętaj mnie” = rok), a o prawie do edycji decyduje serwer (PARAFIA.canEdit).
(function(){
 const ROSE='<svg viewBox="-30 -30 60 60" aria-hidden="true"><circle r="27"/><path d="M0,-9 C-3,-15 -12,-17 -12,-10 C-12,-4 -4,1 0,6 C4,1 12,-4 12,-10 C12,-17 3,-15 0,-9 Z M0,-7 V3 M-4,-3 H4 M-4,-13 C-10,-27 10,-27 4,-13 M10,-6 C24,-9 22,10 9,4 M7,9 C14,22 -2,26 -1,13 M-7,9 C-14,22 2,26 1,13 M-10,-6 C-24,-9 -22,10 -9,4"/></svg>';
 const D=document.createElement('dialog');D.className='login';D.setAttribute('aria-labelledby','lg-h');
 D.innerHTML=`<form method="dialog" novalidate><button type="button" class="lx" aria-label="Zamknij"><svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg></button>
  <h2 id="lg-h">${ROSE}Edycja strony</h2><p>Dostęp tylko dla osób prowadzących stronę parafii.</p>
  <label>Login<input type="text" name="u" autocomplete="username" autocapitalize="off" spellcheck="false"></label>
  <label>Hasło<input type="password" name="p" autocomplete="current-password"></label>
  <label class="rem"><input type="checkbox" name="r" checked> Zapamiętaj mnie na tym komputerze</label>
  <p class="err" role="alert"></p>
  <div class="lbtns"><button type="button" class="no">Anuluj</button><button type="submit" class="go">Zaloguj</button></div></form>`;
 document.body.appendChild(D);
 const pill=document.createElement('button');pill.type='button';pill.className='editpill';pill.innerHTML='<svg class="ico" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16v4zM14 6l4 4"/></svg> Edytuj stronę';document.body.appendChild(pill);
 const bar=document.querySelector('.editbar');
 const st={get:k=>{try{return localStorage.getItem(k)||sessionStorage.getItem(k)}catch(e){return null}},
  set:(k,v,keep)=>{try{(keep?localStorage:sessionStorage).setItem(k,v)}catch(e){}},del:k=>{try{localStorage.removeItem(k);sessionStorage.removeItem(k)}catch(e){}}};
 const sel='[data-edit] :is(p,h3,dd,dt,li,td,summary,span,small,time,strong,b),[data-edit]:is(p,li)';
 const edit=on=>{if(on&&!document.body.classList.contains('admin'))return;document.body.classList.toggle('editing',on);
  document.querySelectorAll(sel).forEach(el=>{if(el.closest('.screw,.ctl,.nextbar'))return;if(on)el.setAttribute('contenteditable','true');else el.removeAttribute('contenteditable')})};
 const admin=on=>{document.body.classList.toggle('admin',on);if(!on)edit(false)};
 const WP=window.PARAFIA;
 if(WP?WP.canEdit:st.get('brenna-admin')==='1')admin(true);
 let fails=0,lockUntil=0;
 const open=()=>{if(document.body.classList.contains('admin')){edit(true);return}D.querySelector('.err').textContent='';D.showModal();D.querySelector('[name=u]').focus()};
 document.querySelector('.seal')?.addEventListener('click',open);
 if(location.hash==='#edycja'){history.replaceState(null,'',location.pathname+location.search);setTimeout(open,300)}
 addEventListener('hashchange',()=>{if(location.hash==='#edycja'){history.replaceState(null,'',location.pathname+location.search);open()}});
 D.querySelector('.lx').onclick=D.querySelector('.no').onclick=()=>D.close();
 D.querySelector('form').addEventListener('submit',e=>{e.preventDefault();const err=D.querySelector('.err'),u=D.querySelector('[name=u]').value.trim().toLowerCase(),p=D.querySelector('[name=p]').value;
  if(Date.now()<lockUntil){err.textContent=`Zbyt wiele prób. Spróbuj ponownie za ${Math.ceil((lockUntil-Date.now())/1000)} s.`;return}
  if(WP){const b=D.querySelector('.go');b.disabled=true;err.textContent='';
   WP.call('login',{body:{u,p,r:D.querySelector('[name=r]').checked}}).then(()=>{location.hash='edycja';location.reload()})
    .catch(x=>{b.disabled=false;D.classList.remove('shake');void D.offsetWidth;D.classList.add('shake');err.textContent=x.message});return}
  if(u==='proboszcz'&&p==='brenna'){fails=0;st.set('brenna-admin','1',D.querySelector('[name=r]').checked);D.querySelector('[name=p]').value='';D.close();admin(true);edit(true);return}
  fails++;D.classList.remove('shake');void D.offsetWidth;D.classList.add('shake');D.querySelector('[name=p]').select();
  if(fails>=5){lockUntil=Date.now()+30000;fails=0;err.textContent='Zbyt wiele prób. Spróbuj ponownie za 30 s.'}else err.textContent='Nieprawidłowy login lub hasło.'});
 pill.onclick=()=>edit(true);
 if(bar){bar.innerHTML='Tryb edycji: kliknij tekst, aby go zmienić. <span class="savestat" role="status"></span><button type="button" id="editdone">Zakończ</button><button type="button" class="out">Wyloguj</button>';
  bar.querySelector('#editdone').onclick=()=>{edit(false);WP&&WP.flush&&WP.flush()};
  bar.querySelector('.out').onclick=async()=>{if(WP){await (WP.flush&&WP.flush());await WP.call('logout').catch(()=>{});location.reload();return}st.del('brenna-admin');admin(false)}}
})();
// ===== mapa: przełącznik Brenna / Górki =====
(function(){const box=document.querySelector('.mapbox');if(!box)return;const f=box.querySelector('.gmap'),l=box.querySelector('.maplink'),tabs=[...box.querySelectorAll('[role=tab]')];
 tabs.forEach(t=>t.addEventListener('click',()=>{tabs.forEach(x=>x.setAttribute('aria-selected',x===t));
  f.src='https://maps.google.com/maps?q='+encodeURIComponent(t.dataset.q)+'&z=15&output=embed';f.title='Mapa: kościół w '+(t.textContent==='Brenna'?'Brennej':'Górkach');
  l.href='https://www.google.com/maps/dir/?api=1&destination='+t.dataset.dir}))})();
