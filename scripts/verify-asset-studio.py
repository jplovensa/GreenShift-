import json,math,hashlib,os
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4173').rstrip('/');FLAGS=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']
def plan(p):return p.evaluate('GreenShiftPlanner.getPlan()')
def q(p):return p.evaluate('GreenShiftPlanner.getTakeoff()')
def close(a,b):assert abs(a-b)<1e-7,(a,b)
def load(p,state):
 p.locator('#import-plan').set_input_files({'name':'asset.json','mimeType':'application/json','buffer':json.dumps(state).encode()});p.wait_for_function('(s)=>JSON.stringify(GreenShiftPlanner.getPlan())===JSON.stringify(s)',arg=state)
def blank(p):
 p.locator('details.lining-settings').evaluate('(el)=>el.open=true')
 p.locator('#preset').select_option('blank');p.locator('#line-rear').uncheck();p.locator('#line-left').uncheck();p.locator('#rear-openings').fill('0') if p.locator('#rear-openings').is_enabled() else None;p.locator('#apply-eps').click()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=FLAGS);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)));p.goto(BASE+'/assets/renovation-studio.html');p.wait_for_function('window.GreenShiftPlanner');assert not p.locator('#webgl-error').is_visible();assert plan(p)['version']==2;close(q(p)['volume'],0);p.locator('details.lining-settings').evaluate('(el)=>el.open=true');p.locator('#line-rear').check();p.locator('#line-left').check();p.locator('#apply-eps').click();close(q(p)['volume'],3.52512)
 for cm in [10,12,15,20]:
  p.locator('[data-thickness="'+str(cm)+'"]').click();assert plan(p)['eps']['thickness']==cm;close(q(p)['volume'],2.7*(11-cm/100)*cm/100)
 p.locator('[data-thickness="12"]').click()
 blank(p);close(q(p)['volume'],0);p.locator('[data-item="epswall"]').click();p.locator('#auto-place').click();assert plan(p)['objects'][0]['type']=='epswall'
 for cm,volume in [(10,.648),(12,.7776),(15,.972),(20,1.296)]:p.locator('#wall-thickness').select_option(str(cm));p.locator('#apply-wall').click();close(q(p)['volume'],volume);assert plan(p)['objects'][0]['thickness']==cm
 p.locator('#wall-thickness').select_option('12');p.locator('#wall-opening').select_option('door');p.locator('#apply-wall').click();close(q(p)['volume'],.5508)
 p.locator('#wall-opening').select_option('window');p.locator('#apply-wall').click();close(q(p)['volume'],.6048)
 p.locator('#wall-opening').select_option('both');p.locator('#apply-wall').click();close(q(p)['volume'],.378)
 p.locator('#wall-length').fill('0.8');p.locator('#apply-wall').click();assert plan(p)['objects'][0]['length']==2.4;assert 'opening' in p.locator('#studio-status').inner_text().lower() or 'window' in p.locator('#studio-status').inner_text().lower()
 p.locator('#wall-length').fill('2.4');p.locator('#wall-opening').select_option('solid');p.locator('#apply-wall').click();p.locator('#duplicate').click();assert len(plan(p)['objects'])==2;close(q(p)['volume'],1.5552)
 p.locator('#wall-thickness').select_option('20');p.locator('#apply-wall').click();assert [g['thickness'] for g in q(p)['groups']]==[12,20];close(q(p)['volume'],2.0736)
 p.locator('#undo').click();close(q(p)['volume'],1.5552);p.locator('#undo-redo').click();close(q(p)['volume'],2.0736)
 with p.expect_download() as csvfile:p.locator('#export-eps').click()
 import csv
 rows=list(csv.reader(open(csvfile.value.path(),encoding='utf-8-sig')));assert rows[-1][0]=='TOTAL';close(float(rows[-1][7]),2.0736)
 p.locator('[data-phase="eps"]').click();assert p.evaluate('GreenShiftPlanner.getView().phase')=='eps';p.locator('#object-list button').last.click();assert p.locator('#gizmo-hint').is_visible();p.locator('#focus-item').click();assert p.evaluate('GreenShiftPlanner.getView().distance')==6
 p.screenshot(path='verification/asset-repurposing-eps-desktop.png')
 before=plan(p);p.locator('[data-phase="existing"]').click();assert plan(p)==before;p.locator('[data-phase="proposed"]').click();assert plan(p)==before
 p.locator('[data-light="golden"]').click();assert plan(p)['light']=='golden';p.locator('#render-quality').select_option('performance');p.locator('#render-quality').select_option('studio')
 with p.expect_download() as download:p.locator('#capture').click()
 assert download.value.suggested_filename.endswith('.png');assert download.value.path().stat().st_size>1000
 with p.expect_download() as download:p.locator('#export').click()
 exported=json.load(open(download.value.path()));p.reload();p.wait_for_function('window.GreenShiftPlanner');assert plan(p)==exported
 # Geometry-backed retained lining with explicit opening areas and a butt-joint deduction.
 blank(p);p.locator('[data-thickness="20"]').click();p.locator('#asset-height').fill('3');p.locator('#line-rear').check();p.locator('#line-left').check();p.locator('#rear-openings').fill('1.8');p.locator('#left-openings').fill('1.2');p.locator('#waste-percent').fill('10');p.locator('#apply-eps').click();close(q(p)['volume'],5.88);close(q(p)['supplyVolume'],6.468);p.screenshot(path='verification/asset-repurposing-lining-desktop.png')
 p.locator('#rear-openings').fill('100');p.locator('#apply-eps').click();close(q(p)['volume'],5.88);assert 'exceeds' in p.locator('#studio-status').inner_text()
 # Existing v1 plans migrate, without silently adding lining or changing the old layout.
 legacy={'version':1,'room':{'w':6,'d':5},'floor':'oak','wall':'chalk','preset':'blank','objects':[],'flags':{'intent':True,'customized':False,'walked':False}};p.locator('#import-plan').set_input_files({'name':'legacy.json','mimeType':'application/json','buffer':json.dumps(legacy).encode()});p.wait_for_function('GreenShiftPlanner.getPlan().eps.rear===false');assert plan(p)['version']==2;close(q(p)['volume'],0)
 p.locator('[data-item="epswall"]').click();p.locator('#auto-place').click();p.locator('#wall-opening').select_option('door');p.locator('#apply-wall').click();p.locator('[data-view="walk"]').click();p.locator('#room-canvas').focus();shot=p.locator('#room-canvas').screenshot();p.keyboard.down('w');p.wait_for_timeout(400);p.keyboard.up('w');assert hashlib.sha256(shot).digest()!=hashlib.sha256(p.locator('#room-canvas').screenshot()).digest()
 p.locator('[data-view="iso"]').click();p.locator('#object-list button').first.click();p.locator('#rotate').click();assert plan(p)['objects'][0]['rot']==1
 p.locator('#preset').select_option('lounge');p.locator('[data-item="epswall"]').click();p.locator('#auto-place').click();p.locator('[data-light="golden"]').click();p.screenshot(path='verification/asset-repurposing-proposed-desktop.png')
 assert not errors,errors;print('Desktop: four EPS thicknesses, openings, mixed takeoff, lining/corner/waste, validation, duplicate/redo, phase views, materials, capture, save/export, v1 migration and walk passed.',flush=True)
 # Homepage handoff must carry EPS quantities, including the short-message fallback.
 p.goto(BASE+'/');p.wait_for_function('!document.querySelector(".studio-intro")',timeout=8000);p.locator('[data-experience="renovation"]').click();f=p.frame_locator('#experience-frame iframe');f.locator('[data-item="epswall"]').click();f.locator('#auto-place').click();f.locator('#send').click();p.wait_for_function('!document.getElementById("experience-dialog").open');message=p.locator('#inquiry [name=message]').input_value();assert 'EPS core estimate:' in message and 'm³ installed' in message;print('Homepage EPS brief handoff passed.',flush=True)
 mobile=b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True);mobile.on('pageerror',lambda e:errors.append(str(e)));mobile.goto(BASE+'/assets/renovation-studio.html');mobile.wait_for_function('window.GreenShiftPlanner');blank(mobile);mobile.locator('[data-item="epswall"]').tap();mobile.locator('#auto-place').tap();mobile.locator('#wall-thickness').select_option('15');mobile.locator('#wall-opening').select_option('window');mobile.locator('#apply-wall').tap();close(q(mobile)['volume'],.756);mobile.locator('[data-phase="eps"]').tap();assert mobile.evaluate('document.documentElement.scrollWidth<=innerWidth');mobile.evaluate('window.scrollTo(0,0)');mobile.screenshot(path='verification/asset-repurposing-mobile.png');assert not errors,errors
 print('Mobile: EPS placement, thickness and opening edits, correct quantity, EPS cutaway and no overflow passed.',flush=True);b.close()
