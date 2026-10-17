"""Clean, actual WebGL style references for the brief; no baked-in UI or quantities."""
from pathlib import Path
import base64,re
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE='http://localhost:4174/GreenShift-/assets/'
HOOK='''window.__spaceReference=()=>{renderer.setPixelRatio(1);renderer.setSize(840,600,false);camera.aspect=840/600;camera.updateProjectionMatrix();if(document.getElementById('room-canvas')){camera.position.set(8,7.7,10);camera.lookAt(0,.65,0);if(grid)grid.visible=false;roomGroup.traverse(o=>{if(o.userData.overhead)o.visible=false;});}else{camera.position.set(10,7,22);camera.lookAt(0,2.5,3);}camera.updateMatrixWorld();renderer.render(scene,camera);return renderer.domElement.toDataURL('image/webp',.88).split(',')[1]};'''
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def instrument(route):
  name=route.request.url.split('/')[-1].split('?')[0];s=(ROOT/'assets'/name).read_text();i=s.rfind('})();');route.fulfill(status=200,content_type='application/javascript',body=s[:i]+HOOK+s[i:])
 p.route(re.compile(r'/(?:renovation|facade)-studio\.js(?:\?.*)?$'),instrument)
 for kind,studio in [('interior','renovation'),('facade','facade')]:
  p.goto(BASE+studio+'-studio.html?v=space1');p.wait_for_function('window.__spaceReference')
  if kind=='facade':p.locator('[data-form="curve"]').click()
  for key in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
   p.locator('[data-style="'+key+'"]').click();p.wait_for_timeout(70);data=p.evaluate('__spaceReference()');(ROOT/f'assets/space-{kind}-{key}.webp').write_bytes(base64.b64decode(data));print(kind,key,flush=True)
 assert not errors,errors;b.close()
