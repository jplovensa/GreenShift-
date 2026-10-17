"""Check the replacement client film at the GitHub Pages production path."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE='http://localhost:4174/GreenShift-/'
# GitHub Pages supports byte ranges; the minimal local dev server does not.
def pages_media(route):
 data=(ROOT/'assets/studio-process-film.mp4').read_bytes();r=route.request.headers.get('range')
 headers={'Accept-Ranges':'bytes','Content-Type':'video/mp4'}
 if r:
  a,b=r.removeprefix('bytes=').split('-');start=int(a or 0);end=min(int(b) if b else len(data)-1,len(data)-1);headers['Content-Range']=f'bytes {start}-{end}/{len(data)}';body=data[start:end+1];status=206
 else:body=data;status=200
 headers['Content-Length']=str(len(body));route.fulfill(status=status,headers=headers,body=body)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox']);errors=[];bad=[]
 for w,h in [(1440,1000),(390,844)]:
  p=b.new_page(viewport={'width':w,'height':h});p.route('**/studio-process-film.mp4',pages_media);p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
  p.goto(BASE,wait_until='domcontentloaded');p.locator('.intro-skip').click();v=p.locator('[data-client-slide="film"] video');v.scroll_into_view_if_needed();p.wait_for_function('document.querySelector("[data-client-slide=film] video").readyState>=2')
  info=v.evaluate('(v)=>({src:v.currentSrc,w:v.videoWidth,h:v.videoHeight,d:v.duration,fit:getComputedStyle(v).objectFit})');assert 'studio-process-film.mp4' in info['src'];assert (info['w'],info['h'])==(1280,720);assert 17.9<=info['d']<=18.2,info;assert info['fit']=='contain'
  v.evaluate('(v)=>v.play()');p.wait_for_timeout(400);assert v.evaluate('(v)=>!v.paused&&v.currentTime>0')
  for t in [1,4.5,8.5,12,16]:
   v.evaluate('(v,t)=>{v.pause();v.currentTime=t}',t);p.wait_for_function('(t)=>Math.abs(document.querySelector("[data-client-slide=film] video").currentTime-t)<.1&&!document.querySelector("[data-client-slide=film] video").seeking',arg=t)
   if w==1440:v.screenshot(path=str(ROOT/f'verification/studio-process-{int(t)}.png'))
  v.evaluate('(v)=>{v.currentTime=8.5;v.play()}');p.wait_for_timeout(200);p.locator('[data-client-select="walkthrough"]').click();assert v.evaluate('(v)=>v.paused');p.locator('[data-client-select="film"]').click();assert v.is_visible()
  v.scroll_into_view_if_needed();v.evaluate('(v)=>{v.pause();v.currentTime=8.5}');p.wait_for_timeout(250);p.screenshot(path=str(ROOT/f'verification/studio-process-page-{w}.png'));assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');print(f'{w}px: metadata, playback, chapter seeks, uncropped frame and slide pause passed.',flush=True);p.close()
 p=b.new_page(reduced_motion='reduce');p.goto(BASE,wait_until='domcontentloaded');p.wait_for_selector('.studio-intro',state='detached');v=p.locator('[data-client-slide="film"] video');v.scroll_into_view_if_needed();p.wait_for_timeout(500);assert v.evaluate('(v)=>v.paused');assert not errors,errors;assert not bad,bad;print('Reduced motion retains manual video playback. No browser errors or missing assets.',flush=True);b.close()
