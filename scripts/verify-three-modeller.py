"""Real mouse-driven Three.js modelling, parallel cameras, render modes and Pass restoration."""
import os,math,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
OUT=Path('/workspace/greenshift-modeller-check');OUT.mkdir(exist_ok=True)
def plan(p):return p.evaluate('GreenShiftAssemblyStudio.getPlan()')
def qty(p):return p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume')
def near(a,b):assert abs(a-b)<1e-6,(a,b)
def screen(p,x,y,z):return p.evaluate('''([x,y,z])=>{const v=GreenShiftAssemblyStudio.getView(),point=new THREE.Vector3(x,y,z).applyMatrix4(new THREE.Matrix4().fromArray(v.matrix).invert()).applyMatrix4(new THREE.Matrix4().fromArray(v.projection)),r=document.getElementById('ab-canvas').getBoundingClientRect();return {x:r.left+(point.x+1)*r.width/2,y:r.top+(1-point.y)*r.height/2}}''',[x,y,z])
def drag(p,a,b):p.mouse.move(a['x'],a['y']);p.mouse.down();p.mouse.move(b['x'],b['y'],steps=10);p.mouse.up()
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1600,'height':1000});p.set_default_navigation_timeout(90000);errors=[];bad=[];p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None);p.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 for studio in ['renovation','facade']:
  p.goto(BASE+'assets/'+studio+'-studio.html?lang=en',wait_until='domcontentloaded');p.locator('#assembly-dialog').wait_for(state='visible');p.wait_for_function('GreenShiftAssemblyStudio.getRenderInfo().hdr',timeout=90000);assert p.evaluate('GreenShiftAssemblyStudio.getRenderInfo().textured')>0;assert p.evaluate('GreenShiftAssemblyStudio.getRenderInfo().normalMapped')>0;assert p.evaluate('GreenShiftAssemblyStudio.getRenderInfo().roughnessMapped')>0;p.screenshot(path=str(OUT/(studio+'-render.png')))
  p.locator('[data-workflow=eps]').click();p.locator('#ab-eps-only').click();p.locator('[data-workflow=build]').click();p.locator('[data-ab-add=wall]').click();core=qty(p);near(core,.7776);p.locator('[data-ab-tool=move]').click();o=plan(p)['parts'][0];size=max(.65,min(2.4,p.evaluate('GreenShiftAssemblyStudio.getView().distance')*.08));a=screen(p,o['x']+size*.6,o['y']+o['height']/2,o['z']);z=screen(p,o['x']+size*.6+.4,o['y']+o['height']/2,o['z']);drag(p,a,z);near(plan(p)['parts'][0]['x'],.4);near(qty(p),core)
  o=plan(p)['parts'][0];a=screen(p,o['x'],o['y']+o['height']/2+size*.6,o['z']);z=screen(p,o['x'],o['y']+o['height']/2+size*.6+.3,o['z']);drag(p,a,z);near(plan(p)['parts'][0]['y'],.3);near(qty(p),core)
  p.locator('[data-ab-tool=push]').click();o=plan(p)['parts'][0];left=o['x']-o['length']/2;drag(p,screen(p,o['x']+o['length']/2,o['y']+o['height']/2,o['z']),screen(p,o['x']+o['length']/2+.5,o['y']+o['height']/2,o['z']));o=plan(p)['parts'][0];near(o['length'],2.9);near(o['x']-o['length']/2,left);near(qty(p),2.9*2.7*.12)
  drag(p,screen(p,o['x'],o['y']+o['height'],o['z']),screen(p,o['x'],o['y']+o['height']+.4,o['z']));near(plan(p)['parts'][0]['height'],3.1);near(qty(p),2.9*3.1*.12);p.screenshot(path=str(OUT/(studio+'-pushpull.png')))
  p.locator('[data-ab-tool=rotate]').click();o=plan(p)['parts'][0];radius=max(o['length'],o['depth'])/2+.35;before=qty(p);drag(p,screen(p,o['x']+radius,o['y']+.05,o['z']),screen(p,o['x']+radius*math.cos(math.pi/6),o['y']+.05,o['z']-radius*.5));near(plan(p)['parts'][0]['angle'],30);near(qty(p),before)
  for view in ['top','front','right','back','left']:
   p.locator('[data-cube-view='+view+']').click();assert p.evaluate('GreenShiftAssemblyStudio.getView().cameraType')=='OrthographicCamera';near(qty(p),before)
  p.locator('[data-cube-view=iso]').click();p.locator('#ab-projection').click();assert p.evaluate('GreenShiftAssemblyStudio.getView().cameraType')=='OrthographicCamera'
  for style in ['model','clay','render']:
   saved=plan(p);p.locator('#ab-display-style').select_option(style);assert p.evaluate('GreenShiftAssemblyStudio.getView().displayStyle')==style;assert plan(p)==saved;near(qty(p),before)
  p.locator('#ab-clear').click();p.locator('[data-ab-tool=draw]').click();start=screen(p,-1,0,0);p.mouse.click(start['x'],start['y']);p.locator('#ab-draw-length').fill('3.17');p.locator('#ab-draw-apply').click();near(plan(p)['parts'][0]['length'],3.17);near(qty(p),3.17*2.7*.12)
  p.locator('[data-cube-view=iso]').click();p.locator('[data-ab-tool=pan]').click();rect=p.locator('#ab-canvas').bounding_box();x=rect['x']+rect['width']*.7;y=rect['y']+rect['height']*.6;p.mouse.move(x,y);p.mouse.down();p.mouse.move(x+45,y+20,steps=8);p.mouse.up();v=p.evaluate('GreenShiftAssemblyStudio.getView()');assert any(abs(n)>.01 for n in v['pan'].values());p.locator('#ab-display-style').select_option('model');saved=plan(p);v=p.evaluate('GreenShiftAssemblyStudio.getView()');p.locator('#ab-pass').click();p.locator('#greenshift-pass-dialog').wait_for(state='visible');assert plan(p)==saved;after=p.evaluate('GreenShiftAssemblyStudio.getView()');assert after['cameraType']==v['cameraType'] and after['displayStyle']==v['displayStyle'];assert after['pan']==v['pan'];near(after['distance'],v['distance'])
  with p.expect_download() as dl:p.locator('#gsp-top-pdf').click()
  pdf=OUT/(studio+'-modelling-Pass.pdf');dl.value.save_as(str(pdf));assert 'Pages:           1' in subprocess.check_output(['pdfinfo',str(pdf)],text=True);p.locator('#gsp-close').click()
  p.set_viewport_size({'width':390,'height':844});assert not p.locator('#assembly-dialog').evaluate('(e)=>e.scrollWidth>e.clientWidth');p.screenshot(path=str(OUT/(studio+'-mobile.png')));p.set_viewport_size({'width':1600,'height':1000});print(studio+': HDR/PBR, real XYZ gizmo drags, anchored push/pull, ring rotation, parallel views, display invariance, exact typed draw, pan and one-page Pass/view restoration passed.',flush=True)
 assert not errors,errors;assert not bad,bad;b.close()
