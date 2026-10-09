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
const reduced = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : {matches:true};
const icon = name => `<i class="ph ph-${name}" aria-hidden="true"></i>`;
const header = document.getElementById('site-header');
const toggle = document.getElementById('menu-toggle');
const menu = document.getElementById('mobile-menu');
const main = document.querySelector('main');
const footer = document.querySelector('footer');
function setMenu(open) {
  menu.hidden = !open;
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  toggle.innerHTML = icon(open ? 'x' : 'list');
  header.classList.toggle('is-menu-open', open);
  document.body.classList.toggle('menu-open', open);
  main.inert = open;
  footer.inert = open;
}
toggle.addEventListener('click',()=>setMenu(menu.hidden));
menu.addEventListener('click',event=>{if(event.target.closest('a'))setMenu(false);});
header.querySelector('a').addEventListener('click',()=>setMenu(false));
function updateHeader(){header.classList.toggle('is-scrolled',window.scrollY>80);}
window.addEventListener('scroll', updateHeader, {passive:true});updateHeader();
window.addEventListener('resize',()=>{if(window.innerWidth>768)setMenu(false);});
document.addEventListener('keydown',event=>{
 if(event.key==='Escape' && !menu.hidden){setMenu(false);toggle.focus();}
 if(event.key==='Tab' && !menu.hidden){const focusables=[toggle,...menu.querySelectorAll('a')];const idx=focusables.indexOf(document.activeElement);event.preventDefault();focusables[(idx+(event.shiftKey?-1:1)+focusables.length)%focusables.length].focus();}
});
const videos=[...document.querySelectorAll('main video')];
const videoObserver = 'IntersectionObserver' in window ? new IntersectionObserver(entries=>{for(const entry of entries){const video=entry.target;if(entry.isIntersecting && !reduced.matches)video.play().catch(()=>{});else video.pause();}},{threshold:.15}) : null;
for(const video of videos){video.muted=true;if(videoObserver)videoObserver.observe(video);}
const heroVideo=document.querySelector('#hero video');
if(heroVideo){
 const button=document.createElement('button');button.className='video-toggle';button.type='button';button.setAttribute('aria-label','Play hero video');button.innerHTML=icon('play');document.getElementById('hero').appendChild(button);
 const sync=()=>{button.innerHTML=icon(heroVideo.paused?'play':'pause');button.setAttribute('aria-label',heroVideo.paused?'Play hero video':'Pause hero video');};heroVideo.addEventListener('play',sync);heroVideo.addEventListener('pause',sync);
 button.addEventListener('click',()=>{if(heroVideo.paused)heroVideo.play().catch(()=>{});else heroVideo.pause();});
}
const onReduced=()=>{if(reduced.matches){videos.forEach(v=>v.pause());document.querySelectorAll('dialog video').forEach(v=>v.pause());}};
if(reduced.addEventListener)reduced.addEventListener('change',onReduced);else if(reduced.addListener)reduced.addListener(onReduced);
const keys=['Mid-Range','Luxury','Avant-Garde','Adaptive Reuse'];
const dialog=document.getElementById('tier-dialog');
let origin=null;
function closeDialog(){dialog.close();}
function openTier(card){
 const idx=keys.indexOf(card.dataset.tier);if(idx<0)return;
 origin=card;
 dialog.replaceChildren(document.getElementById('tier-template-'+idx).content.cloneNode(true));
 dialog.querySelector('.close-tier').addEventListener('click',closeDialog);
 dialog.querySelector('.tier-inquiry').addEventListener('click',()=>{document.querySelector('[name=interest]').value=dialog.querySelector('#tier-title').textContent;closeDialog();document.getElementById('contact').scrollIntoView({behavior:reduced.matches?'instant':'smooth'});document.querySelector('[name=name]').focus({preventScroll:true});});
 dialog.showModal();document.body.classList.add('dialog-open');
 const video=dialog.querySelector('video');if(video){video.muted=true;if(!reduced.matches)video.play().catch(()=>{});}
}
for(const card of document.querySelectorAll('[data-tier]')){card.addEventListener('click',()=>openTier(card));card.addEventListener('keydown',event=>{if(event.key==='Enter'||event.key===' '){event.preventDefault();openTier(card);}});}
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const box=dialog.getBoundingClientRect();if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)closeDialog();});
dialog.addEventListener('close',()=>{dialog.querySelectorAll('video').forEach(v=>v.pause());document.body.classList.remove('dialog-open');if(origin)origin.focus({preventScroll:true});});
const form=document.getElementById('inquiry');
const review=document.getElementById('inquiry-review');
form.addEventListener('submit',event=>{
 event.preventDefault();if(!form.reportValidity())return;
 const data=new FormData(form);const text=`GreenShift project inquiry\n\nFull name: ${data.get('name')}\nEmail: ${data.get('email')}\nCompany: ${data.get('company')||'—'}\nInterest: ${data.get('interest')}\n\n${data.get('message')}`;
 review.querySelector('pre').textContent=text;review.querySelector('a').href='https://wa.me/6287786010290?text='+encodeURIComponent(text);review.hidden=false;review.scrollIntoView({behavior:reduced.matches?'instant':'smooth',block:'center'});
});
form.addEventListener('input',()=>{review.hidden=true;review.querySelector('a').removeAttribute('href');});document.getElementById('edit-inquiry').addEventListener('click',()=>{review.hidden=true;document.querySelector('[name=message]').focus();});
})();
