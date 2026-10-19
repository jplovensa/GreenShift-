"""Every direct client URL opens the current planner; advanced mode stays explicit."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
OUT=Path('/workspace/greenshift-entry-check');OUT.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_navigation_timeout(90000);errors=[];bad=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 for studio in ['renovation','facade']:
  url=BASE+'assets/'+studio+'-studio.html';p.goto(url);p.locator('#assembly-dialog').wait_for(state='visible');assert 'assembly=1' in p.url;assert p.locator('.ab-configuration-summary').is_visible();assert p.locator('.ab-navigation button').count()==5;p.screenshot(path=str(OUT/(studio+'-default.png')))
  p.locator('#ab-close').click();assert 'guided=1' in p.url;assert 'assembly=' not in p.url;assert not p.locator('#assembly-dialog').is_visible();p.reload();assert not p.locator('#assembly-dialog').is_visible();p.locator('#assembly-launch').click();assert p.locator('#assembly-dialog').is_visible();assert 'guided=' not in p.url
  p.goto(url+'?v=pass1&panel=eps');p.locator('#assembly-dialog').wait_for(state='visible');assert p.locator('#ab-eps-form').is_visible();assert p.locator('[data-workflow=eps]').get_attribute('aria-pressed')=='true'
  p.goto(url+'?space=1');assert not p.locator('#assembly-dialog').is_visible();print(studio+': bare/old-version links open current planner, advanced choice persists across reload, EPS deep link and measured space handoff passed.',flush=True)
 p.goto(BASE+'?lang=en');p.locator('.intro-skip').click();p.locator('.studio-launch-actions [data-panel=eps]').click();f=p.frame_locator('#experience-frame iframe');f.locator('#assembly-dialog').wait_for(state='visible');assert f.locator('#ab-eps-form').is_visible();assert f.locator('.ab-configuration-summary').is_visible();p.locator('#experience-close').click();p.locator('.studio-launch-actions [data-experience=renovation]:not([data-panel])').click();f.locator('#assembly-dialog').wait_for(state='visible');assert f.locator('#ab-program').is_visible();p.locator('#experience-close').click()
 p.locator('[data-studio-mode=interior]').click();p.locator('#simulation-studio [data-panel=eps]').click();f.locator('#assembly-dialog').wait_for(state='visible');assert f.locator('#ab-eps-form').is_visible();p.locator('#experience-close').click();p.locator('.studio-advanced-link').click();assert not f.locator('#assembly-dialog').is_visible();assert f.locator('#preset').is_visible();p.locator('#experience-close').click()
 for width in [320,390]:
  p.set_viewport_size({'width':width,'height':844});assert not p.evaluate('document.documentElement.scrollWidth>innerWidth');p.locator('#studio').scroll_into_view_if_needed();p.screenshot(path=str(OUT/('homepage-entry-'+str(width)+'.png')))
 assert not errors,errors;assert not bad,bad;print('Homepage design/EPS launches, explicit advanced tools and mobile layout passed. No messages sent.');b.close()
