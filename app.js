// The introduction is optional enhancement: the static homepage always exists.
(() => {
  const app = document.getElementById('app');
  if (!app) return;
  const reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const intro = document.createElement('section');
  intro.className = 'studio-intro';
  intro.setAttribute('role', 'dialog');
  intro.setAttribute('aria-modal', 'true');
  intro.setAttribute('aria-label', 'GreenShift introduction — from 540 to 45 days, part of Fjäll Group');
  intro.innerHTML = `<video class="intro-video" muted loop playsinline preload="metadata" poster="./assets/hero-poster.jpg" aria-hidden="true"><source src="./assets/hero-studio.mp4" type="video/mp4"></video><div class="intro-shade"></div><button class="intro-skip" type="button">Skip intro <i class="ph ph-arrow-right" aria-hidden="true"></i></button><div class="intro-count" aria-hidden="true"><p class="eyebrow">Build your home. Without the wait.</p><span class="intro-number">${reduced ? '45' : '540'}</span><span class="intro-days">DAYS</span><p class="intro-range">540 days <span>→</span> 45 days</p></div><div class="intro-brand"><div class="intro-brand-sheet"><img class="intro-greenshift" src="./assets/logo.png" alt="GreenShift"><p class="eyebrow">Part of</p><img class="intro-fjall" src="./assets/fjall-group.png" alt="Fjäll Group"><p class="intro-promise">45 days. Without the wait.</p></div></div>`;
  let closed = false, frame = 0;
  const timers = [];
  const previousFocus = document.activeElement;
  const previousInert = app.inert;
  const media = intro.querySelector('video');
  const skip = intro.querySelector('button');
  function finish() {
    if (closed) return;
    closed = true;
    timers.forEach(clearTimeout);
    cancelAnimationFrame(frame);
    media.pause();
    intro.remove();
    app.inert = previousInert;
    document.body.classList.remove('intro-open');
    document.removeEventListener('keydown', onKey);
    document.removeEventListener('visibilitychange', onVisibility);
    if (document.activeElement === document.body && previousFocus && previousFocus !== document.body) previousFocus.focus({preventScroll:true});
  }
  function onKey(event) {
    if (event.key === 'Escape') { event.preventDefault(); finish(); }
    else if (event.key === 'Tab') { event.preventDefault(); skip.focus(); }
  }
  function onVisibility() { if (document.hidden) finish(); }
  // Independent upper bound: failed video, missing logo, or interrupted animation
  // must never trap visitors behind a loader.
  timers.push(setTimeout(finish, 6200));
  skip.addEventListener('click', finish);
  document.addEventListener('keydown', onKey);
  document.addEventListener('visibilitychange', onVisibility);
  document.body.appendChild(intro);
  app.inert = true;
  document.body.classList.add('intro-open');
  skip.focus({preventScroll:true});
  function reveal() {
    intro.querySelector('.intro-number').textContent = '45';
    intro.classList.add('is-brand');
    timers.push(setTimeout(() => {
      intro.classList.add('is-leaving');
      timers.push(setTimeout(finish, reduced ? 0 : 500));
    }, reduced ? 700 : 1500));
  }
  if (reduced) {
    intro.classList.add('is-reduced');
    reveal();
    return;
  }
  media.play().catch(() => {}); // Poster remains visible if playback is unavailable.
  const start = performance.now();
  function tick(now) {
    if (closed) return;
    const progress = Math.min(1, (now - start) / 2600);
    const eased = 1 - Math.pow(1 - progress, 3);
    intro.querySelector('.intro-number').textContent = String(Math.round(540 - 495 * eased));
    if (progress < 1) frame = requestAnimationFrame(tick);
    else timers.push(setTimeout(reveal, 350));
  }
  frame = requestAnimationFrame(tick);
})();

(() => {
const content = JSON.parse(document.getElementById("studio-data").textContent);
const icon=(name)=>`<i class="ph ph-${name}" aria-hidden="true"></i>`;
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('open',open);menu.innerHTML=icon(open?'x':'list');});
nav.addEventListener('click',e=>{if(e.target.closest('a')){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');menu.innerHTML=icon('list');}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){nav.classList.remove('open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label','Open navigation');menu.innerHTML=icon('list');}});
const v=document.querySelector('video'),toggle=document.querySelector('.video-toggle');
const updateVideo=()=>{toggle.innerHTML=icon(v.paused?'play':'pause');toggle.setAttribute('aria-label',v.paused?'Play hero video':'Pause hero video');};
toggle.addEventListener('click',async()=>{if(v.paused){try{await v.play();}catch{toggle.setAttribute('aria-label','Video playback unavailable');}}else v.pause();updateVideo();});
v.addEventListener('play',updateVideo);v.addEventListener('pause',updateVideo);
const motion=window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : {matches:true};
if(!motion.matches)v.play().catch(updateVideo);
const motionChanged=()=>{if(motion.matches)v.pause();};
if(motion.addEventListener)motion.addEventListener('change',motionChanged);else if(motion.addListener)motion.addListener(motionChanged);
const dialog=document.querySelector('dialog');
document.querySelectorAll('[data-tier]').forEach(button=>button.addEventListener('click',()=>{const t=content.tiers[button.dataset.tier];document.querySelector('#tier-content').innerHTML=`<span class="eyebrow">${t.label}</span><h2 id="tier-title">${t.title}</h2><p class="lead">${t.description}</p><div class="specs"><h3>STRUCTURAL SPECIFICS</h3><p>${t.structural}</p><h3>PROJECT RANGE</h3><p>${t.projectRange}</p><h3>TARGET MARKET</h3><p>${t.targetMarket}</p></div><button class="button" id="tier-inquiry">Initiate Project ${icon('arrow-right')}</button>`;dialog.showModal();document.body.classList.add('dialog-open');document.querySelector('#tier-inquiry').addEventListener('click',()=>{document.querySelector('[name="interest"]').value=t.title;dialog.close();document.querySelector('#contact').scrollIntoView({behavior:motion.matches?'instant':'smooth'});document.querySelector('[name="name"]').focus({preventScroll:true});});}));
document.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();});dialog.addEventListener('close',()=>document.body.classList.remove('dialog-open'));
const form=document.querySelector('form'),review=document.querySelector('#inquiry-review');
form.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(form);const message=`GreenShift project inquiry\n\nFull name: ${d.get('name')}\nEmail: ${d.get('email')}\nCompany: ${d.get('company')||'—'}\nInterest: ${d.get('interest')}\n\n${d.get('message')}`;review.querySelector('pre').textContent=message;review.querySelector('a').href='https://wa.me/6287786010290?text='+encodeURIComponent(message);review.hidden=false;review.scrollIntoView({behavior:motion.matches?'instant':'smooth',block:'center'});});
form.addEventListener('input',()=>{review.hidden=true;review.querySelector('a').removeAttribute('href');});document.querySelector('#edit-inquiry').addEventListener('click',()=>{review.hidden=true;document.querySelector('[name="message"]').focus();});

})();
