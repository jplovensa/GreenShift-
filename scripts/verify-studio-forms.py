"""Real WebGL workflows for form-based facade renovation and complete interior styles."""
import json,csv,os,hashlib
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4173').rstrip('/');FLAGS=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']
def close(a,b):assert abs(a-b)<1e-6,(a,b)
def fp(p):return p.evaluate('GreenShiftFacadeStudio.getPlan()')
def fq(p):return p.evaluate('GreenShiftFacadeStudio.getTakeoff()')
def ip(p):return p.evaluate('GreenShiftPlanner.getPlan()')
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=FLAGS);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];bad=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('response',lambda r:bad.append(r.url) if r.status>=400 and '/assets/' in r.url else None)
 p.goto(BASE+'/assets/facade-studio.html?v=studio4');p.wait_for_function('window.GreenShiftFacadeStudio');assert not p.locator('#webgl-error').is_visible();close(fq(p)['volume'],4.4616)
 quantities=[]
 for form in ['box','curve','wave','folded','asymmetric','gable']:
  p.locator('[data-form="'+form+'"]').click();assert fp(p)['form']==form;quantities.append(fq(p)['volume']);assert form=='box' or fq(p)['volume']!=4.4616
  for cm in [10,12,15,20]:p.locator('[data-thickness="'+str(cm)+'"]').click();assert fp(p)['thickness']==cm;assert fq(p)['volume']>0
  p.locator('[data-thickness="12"]').click()
 assert len(set(round(q,5) for q in quantities))==6
 p.locator('[data-form="curve"]').click();before=fq(p)['volume']
 for style in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
  p.locator('[data-style="'+style+'"]').click();assert fp(p)['designStyle']==style;close(fq(p)['volume'],before)
 p.locator('[data-style="contemporary"]').click()
 # Click the actual curved pane using the public, read-only camera and profile matrices.
 point=p.evaluate('''()=>{const p=GreenShiftFacadeStudio.getPlan(),h=GreenShiftFacadeStudio.getTakeoff().holes.find(h=>h.name==='Window 2.1'),pro=GreenShiftFacade.profile(p),a=GreenShiftFacade.at(pro,(h.s0+h.s1)/2-h.w*.22,-.02),v=new THREE.Vector3(a.x,h.y+h.h*.5,p.d/2+p.extension+a.z),view=GreenShiftFacadeStudio.getView(),inv=new THREE.Matrix4().fromArray(view.cameraMatrix).invert(),projection=new THREE.Matrix4().fromArray(view.projectionMatrix),r=document.getElementById('facade-canvas').getBoundingClientRect();v.applyMatrix4(inv).applyMatrix4(projection);return {x:r.left+(v.x+1)*r.width/2,y:r.top+(1-v.y)*r.height/2};}''')
 p.mouse.click(point['x'],point['y']);assert p.locator('#opening-select').input_value()=='Window 2.1'
 p.locator('#opening-x').fill('-1.35');p.locator('#opening-y').fill('3.7');p.locator('#opening-w').fill('1.5');p.locator('#opening-h').fill('1.25');p.locator('#apply-opening').click();assert fp(p)['openingOverrides'][0]['w']==1.5;assert fq(p)['volume']!=before
 saved=fp(p);p.locator('#opening-x').fill('0');p.locator('#opening-y').fill('0');p.locator('#opening-w').fill('3');p.locator('#opening-h').fill('3');p.locator('#apply-opening').click();assert fp(p)==saved;assert 'overlap' in p.locator('#studio-status').inner_text() or 'fit' in p.locator('#studio-status').inner_text()
 p.locator('#undo').click();assert not fp(p)['openingOverrides'];p.locator('#redo').click();assert fp(p)==saved
 core=fq(p)['volume'];shots=[]
 for stage in ['existing','frame','eps','services','finishes','proposed']:
  p.locator('[data-build-stage="'+stage+'"]').click();assert p.evaluate('GreenShiftFacadeStudio.getView().phase')==stage;close(fq(p)['volume'],core);shots.append(hashlib.sha256(p.locator('#facade-canvas').screenshot()).hexdigest())
 assert len(set(shots))==6
 with p.expect_download() as d:p.locator('#export-build').click()
 assert 'developedLength' in d.value.path().read_text();assert p.evaluate('GreenShiftFacadeStudio.getBuildSchedule().form')=='Sweeping curve'
 with p.expect_download() as d:p.locator('#export').click()
 exported=json.load(open(d.value.path()));assert exported==saved;p.reload();p.wait_for_function('window.GreenShiftFacadeStudio');assert fp(p)==saved;close(fq(p)['volume'],core)
 p.locator('[data-form="asymmetric"]').click();p.locator('[data-style="tropical"]').click();p.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');p.locator('#studio-toast').evaluate('(el)=>el.hidden=true');p.screenshot(path=str(ROOT/'verification/studio4-facade-desktop.png'));assert p.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)');assert not errors,errors;assert not bad,bad;print('Facade: six real forms × four cores, six coordinated styles, direct curved-window picking/editing, invalid edits, six build stages, schedule/JSON, undo/redo and persistence passed.',flush=True)
 p.goto(BASE+'/assets/renovation-studio.html?v=studio4');p.wait_for_function('window.GreenShiftPlanner');p.locator('#preset').select_option('blank');p.locator('#add-measured-wall').click();p.locator('#turn-right').click();p.locator('[data-item="chair"]').click();p.locator('#auto-place').click();p.locator('#item-x').fill('1.75');p.locator('#item-z').fill('0.75');p.locator('#move-item').click();objects=ip(p)['objects'];core=p.evaluate('GreenShiftPlanner.getTakeoff().volume')
 for style in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
  p.locator('[data-style="'+style+'"]').click();assert ip(p)['designStyle']==style;assert ip(p)['objects']==objects;close(p.evaluate('GreenShiftPlanner.getTakeoff().volume'),core)
 shots=[]
 for stage in ['existing','frame','eps','services','finishes','proposed']:
  p.locator('[data-build-stage="'+stage+'"]').click();assert p.evaluate('GreenShiftPlanner.getView().phase')==stage;close(p.evaluate('GreenShiftPlanner.getTakeoff().volume'),core);p.wait_for_timeout(120);shots.append(hashlib.sha256(p.locator('#room-canvas').screenshot()).hexdigest())
 assert len(set(shots))==6;p.locator('#feature-wall').uncheck();p.locator('#ceiling-lighting').uncheck();assert ip(p)['fitout']=={'featureWall':False,'lighting':False}
 with p.expect_download() as d:p.locator('#export-build').click()
 assert 'partitionFinishFaces' in d.value.path().read_text();schedule=p.evaluate('GreenShiftPlanner.getBuildSchedule()');close(schedule['partitionFinishFaces'],12.96)
 p.locator('[data-style="japandi"]').click();saved=ip(p);p.reload();p.wait_for_function('window.GreenShiftPlanner');assert ip(p)==saved;p.locator('[data-build-stage="services"]').click();p.locator('[data-view="walk"]').click();assert p.evaluate('GreenShiftPlanner.getView().phase')=='proposed';p.locator('[data-view="iso"]').click();p.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');p.locator('#studio-toast').evaluate('(el)=>el.hidden=true');p.screenshot(path=str(ROOT/'verification/studio4-interior-desktop.png'));assert p.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)');assert not errors,errors;print('Interior: six complete styles preserve measured layout/core, six distinct stages, support frame/services, fit-out toggles, finish CSV, save/restore and walkthrough passed.',flush=True)
 # The facade summary must carry the form and quantities through the real website dialog.
 p.goto(BASE+'/');p.wait_for_function('!document.querySelector(".studio-intro")',timeout=12000);p.locator('[data-experience="facade"]').click();f=p.frame_locator('#experience-frame iframe');f.locator('#send').click();p.wait_for_function('!document.getElementById("experience-dialog").open');message=p.locator('#inquiry [name=message]').input_value();assert 'Asymmetric wing' in message and 'Facade EPS:' in message;print('Website handoff includes facade form, design and measured EPS quantities.',flush=True)
 m=b.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True);m.on('pageerror',lambda e:errors.append(str(e)))
 for studio,api in [('facade','GreenShiftFacadeStudio'),('renovation','GreenShiftPlanner')]:
  m.goto(BASE+'/assets/'+studio+'-studio.html?v=studio4');m.wait_for_function('window.'+api);m.locator('[data-style="mediterranean"]').tap()
  if studio=='facade':m.locator('#quick-form').select_option('curve');assert fp(m)['form']=='curve'
  else:m.locator('#preset').select_option('blank');m.locator('#add-measured-wall').tap();m.locator('#turn-right').tap();assert ip(m)['objects'][0]['angle']==15
  for stage in ['frame','services','proposed']:m.locator('[data-build-stage="'+stage+'"]').tap();assert m.evaluate(api+'.getView().phase')==stage
  assert m.evaluate('document.documentElement.scrollWidth<=innerWidth');m.evaluate('scrollTo(0,0)');m.locator('#studio-toast').evaluate('(el)=>el.hidden=true');m.screenshot(path=str(ROOT/('verification/studio4-'+studio+'-mobile.png')))
 assert not errors,errors;print('Mobile form/style selection, staged build, EPS rotation, quantity updates and no overflow passed.',flush=True);b.close()
