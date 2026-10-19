"""Reference-driven catalogue, material swatches, dimension annotations and responsive summary."""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
OUT=Path('/workspace/greenshift-reference-check');OUT.mkdir(exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1600,'height':1000});p.set_default_navigation_timeout(90000);errors=[];bad=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 for studio in ['renovation','facade']:
  p.goto(BASE+'assets/'+studio+'-studio.html?assembly=1&lang=en');p.locator('#assembly-dialog').wait_for(state='visible');p.wait_for_function('GreenShiftAssemblyStudio.getRenderInfo().triangles>0');p.screenshot(path=str(OUT/(studio+'-reference-concept.png')));assert p.locator('.ab-configuration-summary').is_visible();before=p.evaluate('GreenShiftAssemblyStudio.getPlan()');p.locator('[data-workflow=build]').click();p.locator('.ab-palette img').first.evaluate('(e)=>e.decode()');assert p.locator('.ab-palette img').count()==15;p.locator('#ab-clear').click();p.locator('[data-ab-add=wall]').click();core=p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume');assert p.locator('[data-measure=length]').inner_text()=='2.4 m';assert p.locator('[data-measure=height]').inner_text()=='2.7 m';assert p.locator('[data-measure=depth]').inner_text()=='0.12 m';p.locator('#ab-dimensions').click();assert not p.locator('[data-measure]').count();assert p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume')==core;p.locator('#ab-dimensions').click();assert p.locator('[data-measure]').count()==3;p.screenshot(path=str(OUT/(studio+'-reference-build.png')))
  p.locator('[data-workflow=materials]').click();p.locator('.ab-catalog summary').filter(has_text='03 / Finish & presentation').click()
  for finish in ['timber','clay','stone','concrete','mineral']:
   p.locator('[data-finish-choice='+finish+']').click();assert p.evaluate('GreenShiftAssemblyStudio.getPlan().finish')==finish;assert p.locator('#ab-finish').input_value()==finish;assert p.locator('[data-finish-choice='+finish+']').get_attribute('aria-pressed')=='true';assert p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume')==core
  p.locator('#ab-finish').select_option('stone');assert p.locator('[data-finish-choice=stone]').get_attribute('aria-pressed')=='true';p.locator('[data-workflow=build]').click();p.screenshot(path=str(OUT/(studio+'-reference-catalogue.png')))
  for width in [320,390,844]:
   p.set_viewport_size({'width':width,'height':844 if width<500 else 390});assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');assert p.locator('#ab-use').is_visible();p.screenshot(path=str(OUT/(studio+'-reference-'+str(width)+'.png')))
  p.set_viewport_size({'width':1600,'height':1000});print(studio+': catalogue previews, bidirectional finish swatches, measured labels, EPS invariance, fixed summary and 320/390/844px layouts passed.',flush=True)
 assert not bad,bad;assert not errors,errors;b.close()
