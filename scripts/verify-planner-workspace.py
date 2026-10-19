"""Beginner multi-opening EPS flow, live WebGL, contextual planner and bounded Pass stress tests."""
import json,os,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
OUT=Path('/workspace/greenshift-planner-check');OUT.mkdir(exist_ok=True)
def qty(p):return p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume')
def plan(p):return p.evaluate('GreenShiftAssemblyStudio.getPlan()')
def near(a,b):assert abs(a-b)<1e-8,(a,b)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1600,'height':1000});p.set_default_navigation_timeout(90000);errors=[];bad=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 for studio in ['renovation','facade']:
  p.goto(BASE+'assets/'+studio+'-studio.html?assembly=1&lang=en');p.locator('#assembly-dialog').wait_for(state='visible');p.wait_for_function('GreenShiftAssemblyStudio.getRenderInfo().contactShading');assert not p.locator('.ab-inspector').is_visible();assert p.locator('#ab-program').is_visible();p.screenshot(path=str(OUT/(studio+'-planner.png')))
  p.locator('[data-workflow=eps]').click();assert not p.locator('#ab-program').is_visible();p.locator('#ab-eps-only').click();near(qty(p),0);p.locator('#ab-eps-length').fill('6');p.locator('#ab-eps-height').fill('3');p.locator('#ab-eps-door').click();p.locator('#ab-eps-window').click();rows=p.locator('.ab-eps-opening');rows.nth(1).locator('[data-cut=left]').fill('2.4');assert not p.locator('#ab-eps-error').is_visible();assert '1.7604' in p.locator('#ab-eps-result').inner_text();p.locator('#ab-eps-add').click();near(qty(p),1.7604);assert len(plan(p)['parts'])==1;assert len(plan(p)['parts'][0]['openings'])==2;assert p.locator('.ab-inspector').is_visible()
  p.locator('#ab-eps-unit').select_option('cm');assert p.locator('#ab-eps-length').input_value()=='600';assert rows.nth(1).locator('[data-cut=left]').input_value()=='240';assert '1.7604' in p.locator('#ab-eps-result').inner_text()
  for core in [10,12,15,20]:p.locator('#ab-eps-core').select_option(str(core));p.locator('#ab-eps-update').click();near(qty(p),14.67*core/100)
  saved=plan(p);rows.nth(1).locator('[data-cut=left]').fill('20');assert p.locator('#ab-eps-error').is_visible();assert p.locator('#ab-eps-add').is_disabled();assert plan(p)==saved;rows.nth(1).locator('[data-cut=left]').fill('240');p.locator('#ab-eps-unit').select_option('m');p.locator('#ab-eps-length').fill('6,0');assert not p.locator('#ab-eps-error').is_visible();p.locator('#ab-eps-update').click();near(qty(p),2.934)
  p.locator('#ab-turn').click();near(qty(p),2.934);p.locator('#ab-copy').click();p.locator('#ab-paste').click();near(qty(p),5.868);assert len(plan(p)['parts'][1]['openings'])==2;p.locator('#ab-undo').click();near(qty(p),2.934);p.screenshot(path=str(OUT/(studio+'-eps.png')))
  p.locator('[data-workflow=concept]').click();p.locator('#ab-program').select_option('commercial');p.locator('#ab-variant').select_option('cafe');p.locator('#ab-concept-load').click();assert any(x['type']=='dining' for x in plan(p)['parts']);p.locator('[data-workflow=materials]').click();p.locator('.ab-catalog summary').filter(has_text='03 / Finish & presentation').click();p.locator('#ab-quality').select_option('render');p.locator('#ab-style').select_option('japandi');p.locator('#ab-cutaway').check();core=qty(p);p.locator('#ab-furniture').uncheck();near(qty(p),core);p.locator('#ab-furniture').check();p.screenshot(path=str(OUT/(studio+'-render.png')))
  p.locator('[data-workflow=brief]').click();p.locator('#ab-client').fill('W'*100);p.locator('#ab-project').fill('W'*120);p.locator('#ab-location').fill('W'*140);p.locator('#ab-budget').fill('W'*100);p.locator('#ab-timing').fill('W'*100);p.locator('#ab-priorities').fill(('Ruang untuk keluarga. '*50)[:800]);p.locator('#ab-questions').fill(('日本語の設計と工程について相談したい。 '*100)[:1200]);p.locator('#ab-client').click();saved=plan(p);p.locator('#ab-pass').click();p.locator('#greenshift-pass-dialog').wait_for(state='visible');assert plan(p)==saved
  with p.expect_download() as dl:p.locator('#gsp-top-pdf').click()
  pdf=OUT/(studio+'-Pass-stress.pdf');dl.value.save_as(str(pdf));assert 'Pages:           1' in subprocess.check_output(['pdfinfo',str(pdf)],text=True);meta=p.evaluate('GreenShiftPass.getLastPass()');layout=meta['layout'];m=layout['margin'];assert m/layout['width']*210>13.9
  blocks=layout['blocks']
  for block in blocks:
   assert block['x']>=m and block['y']>=m,(block['id'],'top/left margin');assert block['x']+block['w']<=layout['width']-m+.01,(block['id'],'right margin');assert block['y']+block['h']<=layout['height']-m+.01,(block['id'],'bottom margin');assert len(block['lines'])*block['lineHeight']<=block['h'];assert all(line['width']<=block['w']+.01 for line in block['lines']),block['id']
  for i,a in enumerate(blocks):
   for other in blocks[i+1:]:assert not(a['x']<other['x']+other['w'] and other['x']<a['x']+a['w'] and a['y']<other['y']+other['h'] and other['y']<a['y']+a['h']),(a['id'],other['id'])
  assert any(b['truncated'] for b in blocks);assert meta['brief']['questions']==saved['brief']['questions']
  with p.expect_download() as dl:p.locator('#gsp-json').click()
  data=json.loads(dl.value.path().read_text());assert data['plan']['brief']['questions']==saved['brief']['questions'];assert data['id']==meta['id'];(OUT/(studio+'-Pass-layout.json')).write_text(json.dumps(layout,indent=2));p.locator('#gsp-close').click()
  for width in [320,390]:
   p.set_viewport_size({'width':width,'height':844});assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.locator('[data-workflow=eps]').click();assert p.locator('#ab-eps-length').is_visible();p.screenshot(path=str(OUT/(studio+'-mobile-'+str(width)+'.png')));p.locator('#ab-pass').click();assert not p.locator('#greenshift-pass-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.locator('#gsp-close').click()
  p.set_viewport_size({'width':1600,'height':1000});p.locator('#ab-close').click();p.locator('[data-language=id]').click();p.locator('#assembly-launch').click();p.locator('[data-workflow=eps]').click();assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.screenshot(path=str(OUT/(studio+'-id.png')))
  print(studio+': beginner EPS units/cores/multiple openings, exact sums, invalid preservation, copy/rotate, contextual panels, PBR/contact shading, mobile, worst-case one-page Pass margins and matching editable JSON passed.',flush=True)
 assert not bad,bad;assert not errors,errors;print('No missing assets, JavaScript or shader errors.');b.close()
