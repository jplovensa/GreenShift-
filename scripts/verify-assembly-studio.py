"""Real assembly edits, drawing, handles, copy/paste, quantities and handoff in both studios."""
import os,json,math
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
OUT=Path('/workspace/greenshift-assembly-check');OUT.mkdir(exist_ok=True)
def near(a,b):assert abs(a-b)<1e-7,(a,b)
def plan(p):return p.evaluate('GreenShiftAssemblyStudio.getPlan()')
def q(p):return p.evaluate('GreenShiftAssemblyStudio.getTakeoff()')
def screen(p,x,y,z):
 return p.evaluate('''([x,y,z])=>{const v=GreenShiftAssemblyStudio.getView(),point=new THREE.Vector3(x,y,z).applyMatrix4(new THREE.Matrix4().fromArray(v.matrix).invert()).applyMatrix4(new THREE.Matrix4().fromArray(v.projection)),r=document.getElementById('ab-canvas').getBoundingClientRect();return {x:r.left+(point.x+1)*r.width/2,y:r.top+(1-point.y)*r.height/2}}''',[x,y,z])
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1600,'height':1000});errors=[];bad=[];p.on('pageerror',lambda e:errors.append(e.stack));p.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
 for studio in ['renovation','facade']:
  p.goto(BASE+'assets/'+studio+'-studio.html?assembly=1&lang=en');p.locator('#assembly-dialog').wait_for(state='visible');p.locator('#ab-clear').click();p.locator('[data-ab-add=wall]').click();assert not p.locator('#ab-webgl').is_visible();near(q(p)['volume'],.7776)
  p.locator('#ab-length').fill('3');p.locator('#ab-part-height').fill('3');p.locator('#ab-thickness').select_option('.2' if p.locator('#ab-thickness option[value=".2"]').count() else '0.2');p.locator('#ab-opening').select_option('door');p.locator('#ab-apply').click();near(q(p)['volume'],(9-1.89)*.2)
  original=plan(p)['parts'][0];p.locator('#ab-copy').click();p.locator('#ab-paste').click();assert len(plan(p)['parts'])==2;near(q(p)['volume'],2*(9-1.89)*.2);assert plan(p)['parts'][1]['opening']=='door';assert plan(p)['parts'][0]['id']!=plan(p)['parts'][1]['id']
  p.locator('#ab-undo').click();assert len(plan(p)['parts'])==1;p.locator('#ab-redo').click();assert len(plan(p)['parts'])==2
  p.locator('#ab-canvas').focus();p.keyboard.press('Control+c');p.keyboard.press('Control+v');assert len(plan(p)['parts'])==3;p.keyboard.press('Control+z');assert len(plan(p)['parts'])==2
  # One clear panel for an actual direct-manipulation resize.
  p.locator('#ab-clear').click();p.locator('[data-ab-add=wall]').click();p.locator('[data-ab-view=iso]').click();p.locator('#ab-parts button').first.click();p.wait_for_timeout(200);start=screen(p,1.2,1.35,0);end=screen(p,1.6,1.35,0);p.mouse.move(start['x'],start['y']);p.mouse.down();p.mouse.move(end['x'],end['y'],steps=8);p.mouse.up();assert plan(p)['parts'][0]['length']>2.4;near(q(p)['volume'],plan(p)['parts'][0]['length']*2.7*.12)
  # Invalid measurements must preserve the last valid build and quantity.
  before=plan(p);p.locator('#ab-length').fill('20');p.locator('#ab-apply').click();assert plan(p)==before
  p.locator('#ab-clear').click();p.locator('[data-ab-tool=draw]').click();p.wait_for_timeout(200);a=screen(p,-1,0,-1);z=screen(p,1,0,-1);p.mouse.click(a['x'],a['y']);p.mouse.click(z['x'],z['y']);assert len(plan(p)['parts'])==1;near(plan(p)['parts'][0]['length'],2)
  # Numeric lift + roof creates a real additional assembly, excluded from EPS.
  core=q(p)['volume'];p.locator('[data-ab-add=roof]').click();near(q(p)['volume'],core);assert len(plan(p)['parts'])==2
  p.locator('#ab-multi').click();p.locator('#ab-parts button').first.click();assert len(p.evaluate('GreenShiftAssemblyStudio.getSelection()'))==2;dims=[(o['length'],o['height'],o['depth']) for o in plan(p)['parts']];p.locator('#ab-y').fill('0.2');p.locator('#ab-apply').click();assert [(o['length'],o['height'],o['depth']) for o in plan(p)['parts']]==dims;near(q(p)['volume'],core);p.locator('#ab-turn').click();near(q(p)['volume'],core);p.locator('#ab-duplicate').click();assert len(plan(p)['parts'])==4;near(q(p)['volume'],core*2);p.locator('#ab-undo').click();assert len(plan(p)['parts'])==2;p.locator('#ab-multi').click()
  p.locator('.ab-catalog summary').filter(has_text='Save & share').click()
  with p.expect_download() as dl:p.locator('#ab-export').click()
  saved=json.loads(dl.value.path().read_text());p.locator('#ab-clear').click();p.locator('#ab-import').set_input_files({'name':'assembly.json','mimeType':'application/json','buffer':json.dumps(saved).encode()});p.wait_for_function('(n)=>GreenShiftAssemblyStudio.getPlan().parts.length===n',arg=len(saved['parts']));assert plan(p)==saved
  with p.expect_download() as dl:p.locator('#ab-csv').click()
  assert 'SUPPLY' in dl.value.path().read_text();p.reload();p.locator('#assembly-dialog').wait_for(state='visible');assert plan(p)==saved
  p.locator('#ab-room').click();near(q(p)['volume'],6.74568);p.locator('[data-ab-view=walk]').click();p.locator('#ab-canvas').focus();p.keyboard.press('w');p.locator('[data-ab-view=iso]').click();p.screenshot(path=str(OUT/(studio+'-assembly-desktop.png')))
  for w in [320,390,844]:
   p.set_viewport_size({'width':w,'height':844 if w<500 else 390});assert not p.evaluate('document.documentElement.scrollWidth>innerWidth');assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.locator('#ab-close').click();assert not p.evaluate('document.documentElement.scrollWidth>innerWidth');p.locator('#assembly-launch').click()
  p.set_viewport_size({'width':1600,'height':1000});print(studio+': measured edits, panel copy, keyboard paste/undo, direct resize handles, invalid edits, two-click wall drawing, roof assembly, JSON/CSV, persistence, walkthrough and responsive layout passed.',flush=True)
 p.goto(BASE+'assets/facade-studio.html?assembly=1&lang=id');p.wait_for_function('document.getElementById("assembly-title").textContent.includes("Konsep Anda")');before=plan(p);p.evaluate('GreenShiftLanguage.set("en")');assert plan(p)==before;p.evaluate('GreenShiftLanguage.set("id")');assert plan(p)==before;p.set_viewport_size({'width':320,'height':844});assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.screenshot(path=str(OUT/'assembly-mobile-id.png'));p.set_viewport_size({'width':1600,'height':1000})
 # Existing guided EPS controls are independently useful.
 p.goto(BASE+'assets/renovation-studio.html?lang=en');p.locator('#preset').select_option('blank');p.locator('#add-measured-wall').click();base=p.evaluate('GreenShiftPlanner.getTakeoff().volume');p.locator('#guide-copy').click();p.locator('#guide-paste').click();near(p.evaluate('GreenShiftPlanner.getTakeoff().volume'),base*2);p.locator('[data-guide-size="length:0.1"]').click();assert p.evaluate('GreenShiftPlanner.getPlan().objects.at(-1).length')==2.5
 p.locator('#assembly-launch').click();p.locator('#ab-from-guided').click();assert len(plan(p)['parts'])==2;near(q(p)['volume'],p.evaluate('GreenShiftPlanner.getTakeoff().volume'));p.locator('#ab-close').click()
 # Main site opens either assembly directly and accepts its measured concept.
 p.goto(BASE+'?lang=en');p.locator('.intro-skip').click();assert 'Space for your' in p.locator('#hero h1').inner_text();p.locator('[data-studio-mode=interior]').click();p.locator('[data-experience=renovation][data-assembly]').click();f=p.frame_locator('#experience-frame iframe');f.locator('#assembly-dialog').wait_for(state='visible');f.locator('#ab-use').click();p.wait_for_function('!document.getElementById("experience-dialog").open');assert 'Assembly EPS core' in p.locator('#field-message').input_value()
 assert not errors,errors;assert not bad,bad;print('Guided EPS copy/resize and homepage-to-assembly-to-inquiry passed. Nothing sent.');b.close()
