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
