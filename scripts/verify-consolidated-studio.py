"""Client-facing hub, material handoff and architecture-only planner regression."""
import os,json
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
 p=b.new_page(viewport={'width':1440,'height':1000});errors=[];bad=[]
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
 p.goto(BASE+'?lang=en');p.locator('.intro-skip').click()
 assert p.locator('main>section').evaluate_all('(es)=>es.map(e=>e.id)')==['hero','philosophy','services','tiers','projects','studio','working-together','start-with-space','contact']
 assert p.locator('#space-photo').count()==0
 assert p.locator('#space-photo-preview').count()==0
 p.reload();p.locator('.studio-intro video').wait_for();p.locator('.intro-skip').click()
 assert p.locator('#tiers').is_visible();p.locator('[data-deployment-filter=existing]').click();assert p.locator('.deployment-card:visible').count()==1;p.locator('[data-deployment-filter=new]').click();assert p.locator('.deployment-card:visible').count()==3;p.locator('[data-deployment-filter=all]').click()
 p.locator('[data-tier=Luxury]').click();p.locator('#tier-dialog').wait_for(state='visible');p.locator('.close-tier').click()
 assert p.locator('#hero video source').get_attribute('src').endswith('hero-architecture.mp4')
 # Keyboard navigation and exactly one active studio mode.
 p.locator('[data-studio-mode=presentation]').focus();p.keyboard.press('ArrowRight');assert p.locator('#studio-panel-interior').is_visible();assert p.locator('[data-studio-panel]:visible').count()==1
 p.locator('#materials-workspace>summary').click();p.locator('[data-asset-detail=joinery]').first.click();assert 'Ceilings & architectural details' in p.locator('#asset-material-title').inner_text();p.locator('#asset-detail-save').click();p.locator('.asset-material-close').click();p.locator('#asset-inquiry').click();assert 'Ceilings & architectural details' in p.locator('#field-message').input_value()
 # Existing deep links reveal the relevant mode and closed material drawer.
 p.goto(BASE+'?lang=en#material-library');assert p.locator('#studio-panel-interior').is_visible();assert p.locator('#materials-workspace').evaluate('(e)=>e.open')
 p.locator('[data-studio-mode=facade]').click();p.locator('#facelift-studio [data-experience]').click();f=p.frame_locator('#experience-frame iframe');f.locator('#facade-canvas').wait_for();assert not f.locator('#webgl-error').is_visible();p.locator('#experience-close').click()
 p.locator('[data-studio-mode=interior]').click();p.locator('#simulation-studio img').evaluate('(e)=>e.decode()');assert p.locator('#simulation-studio img').evaluate('(e)=>e.naturalWidth')>=2560;p.locator('#simulation-studio [data-experience]').click();f=p.frame_locator('#experience-frame iframe');f.locator('#room-canvas').wait_for();assert f.locator('[data-item]').evaluate_all('(es)=>es.map(e=>e.dataset.item)')==['epswall','partition','panel','portal','raft']
 f.locator('#preset').select_option('blank');f.locator('#new-wall-length').fill('3');f.locator('#new-wall-opening').select_option('door');f.locator('#add-measured-wall').click();q=f.locator('body').evaluate('()=>GreenShiftPlanner.getTakeoff().volume');assert q>0
 f.locator('#turn-right').click();assert abs(f.locator('body').evaluate('()=>GreenShiftPlanner.getTakeoff().volume')-q)<1e-9
 f.locator('[data-item=panel]').click();f.locator('#auto-place').click();assert abs(f.locator('body').evaluate('()=>GreenShiftPlanner.getTakeoff().volume')-q)<1e-9
 with p.expect_download() as dl:f.locator('#export').click()
 plan=json.loads(dl.value.path().read_text());assert all(o['type'] in ['epswall','partition','panel','portal','raft'] for o in plan['objects'])
 f.locator('#import-plan').set_input_files({'name':'plan.json','mimeType':'application/json','buffer':json.dumps(plan).encode()});assert f.locator('body').evaluate('()=>GreenShiftPlanner.getPlan()')==plan
 for key in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
  f.locator('[data-style='+key+']').click();assert abs(f.locator('body').evaluate('()=>GreenShiftPlanner.getTakeoff().volume')-q)<1e-9
 f.locator('#send').click();p.wait_for_function('!document.getElementById("experience-dialog").open');assert 'EPS core estimate' in p.locator('#field-message').input_value()
 # Both languages and optional content at phone widths.
 for w in [320,390,844]:
  p.set_viewport_size({'width':w,'height':844 if w<500 else 390});p.locator('[data-language=id]').first.click();p.locator('[data-studio-mode=interior]').click();assert 'Fungsi yang baru.' in p.locator('#simulation-heading').inner_text();assert not p.evaluate('document.documentElement.scrollWidth>innerWidth')
  p.locator('#materials-workspace').evaluate('(e)=>e.open=true');assert not p.evaluate('document.documentElement.scrollWidth>innerWidth');p.locator('[data-language=en]').first.click()
 assert not errors,errors;assert not bad,bad
 print('Nine-section flow, restored cinematic opening, no photo controls, visible deployment filters, HD cover, keyboard tabs, deep links, materials-to-inquiry, both WebGL modes, measured EPS/rotation, architectural elements, plan import/export, six styles and bilingual mobile layouts passed. Nothing sent.')
 b.close()
