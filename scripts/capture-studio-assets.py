import base64,json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
root=ROOT/'assets'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader'])
 page=b.new_page(viewport={'width':1440,'height':1000})
 errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 def hook(route):
  src=(root/'renovation-studio.js').read_text().replace('sync();save();init();','sync();save();init();globalThis.__thumbnailFurniture=furniture;')
  route.fulfill(status=200,content_type='text/javascript',body=src)
 page.route('**/renovation-studio.js*',hook)
 page.goto('http://127.0.0.1:4173/assets/renovation-studio.html?v=studio3');page.wait_for_function('window.GreenShiftPlanner');page.wait_for_timeout(1500)
 assert not errors,errors
 result=page.evaluate('''() => {const T=THREE,r=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});r.setSize(320,240);r.setPixelRatio(1);r.outputColorSpace=T.SRGBColorSpace;r.toneMapping=T.ACESFilmicToneMapping;r.setClearColor(0xf3f4e9);const scene=new T.Scene(),camera=new T.PerspectiveCamera(35,4/3,.1,100);scene.add(new T.HemisphereLight(0xffffff,0x6e7e65,2.3));const light=new T.DirectionalLight(0xffedcf,3.5);light.position.set(-3,7,5);scene.add(light);const result={};for(const type of ['epswall','sofa','chair','desk','table','partition','storage','plant','rug']){const obj=__thumbnailFurniture({id:'preview',type,x:0,z:0,rot:0,length:2.4,height:2.7,thickness:12,opening:'door'});const bounds=new T.Box3().setFromObject(obj),center=bounds.getCenter(new T.Vector3()),size=bounds.getSize(new T.Vector3()),d=Math.max(size.x,size.y,size.z)*2.3;camera.position.set(center.x+d*.7,center.y+d*.55,center.z+d);camera.lookAt(center);scene.add(obj);r.render(scene,camera);result[type]=r.domElement.toDataURL('image/png').split(',')[1];scene.remove(obj);}r.dispose();return result;}''')
 for key,data in result.items():(root/('asset-'+key+'.png')).write_bytes(base64.b64decode(data))
 # The menu's interior is a real isometric room asset, not a UI screenshot.
 page.locator('#room-canvas').screenshot(path=str(root/'studio-interior.png'))
 page.locator('[data-item="epswall"]').click();page.locator('#auto-place').click();assert page.evaluate('GreenShiftPlanner.getTakeoff().volume')>0
 page.locator('#wall-opening').select_option('door');page.locator('#apply-wall').click();page.locator('[data-light="golden"]').click();page.locator('#render-quality').select_option('studio');page.wait_for_timeout(500);page.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');page.locator('#studio-toast').evaluate('(el)=>el.hidden=true');page.screenshot(path=str(root/'renovation-playground-preview.png'))
 page.goto('http://127.0.0.1:4173/assets/facade-studio.html?v=studio3');page.wait_for_function('window.GreenShiftFacadeStudio');page.wait_for_timeout(1500)
 assert not page.locator('#webgl-error').is_visible();assert not errors,errors
 for key in ['mineral','timber','terracotta']:
  page.locator('[data-direction="'+key+'"]').click();page.wait_for_timeout(300);page.locator('#facade-canvas').screenshot(path=str(root/('facade-'+key+'.png')))
 page.locator('[data-direction="timber"]').click();page.locator('[data-light="golden"]').click();page.wait_for_timeout(300)
 page.locator('#facade-canvas').screenshot(path=str(root/'studio-facade.png'))
 page.reload();page.wait_for_function('window.GreenShiftFacadeStudio');page.wait_for_timeout(500);page.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');page.screenshot(path=str(root/'facade-studio-preview.png'))
 assert not errors,errors
 print('Captured local 3D furniture, interior and facade assets. No page errors.')
 b.close()
