"""Capture actual WebGL form/style assets. Start the local server on port 4173 first."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];ASSETS=ROOT/'assets'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://localhost:4173/assets/facade-studio.html?guided=1&v=studio4');p.wait_for_function('window.GreenShiftFacadeStudio')
 for form in ['box','curve','wave','folded','asymmetric','gable']:
  p.locator('[data-form="'+form+'"]').click();p.wait_for_timeout(200);p.locator('#facade-canvas').screenshot(path=str(ASSETS/('facade-form-'+form+'.png')))
 p.locator('[data-form="curve"]').click()
 for key in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
  p.locator('[data-style="'+key+'"]').click();p.wait_for_timeout(200);p.locator('#facade-canvas').screenshot(path=str(ASSETS/('facade-style-'+key+'.png')))
 p.locator('[data-form="asymmetric"]').click();p.locator('[data-style="tropical"]').click();p.reload();p.wait_for_function('window.GreenShiftFacadeStudio');p.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');p.locator('#facade-canvas').screenshot(path=str(ASSETS/'studio-facade.png'));p.screenshot(path=str(ASSETS/'facade-studio-preview.png'))
 p.goto('http://localhost:4173/assets/renovation-studio.html?guided=1&v=studio4');p.wait_for_function('window.GreenShiftPlanner')
 for key in ['contemporary','japandi','tropical','industrial','mediterranean','bold']:
  p.locator('[data-style="'+key+'"]').click();p.wait_for_timeout(200);p.locator('#room-canvas').screenshot(path=str(ASSETS/('interior-style-'+key+'.png')))
 p.locator('[data-style="japandi"]').click();p.locator('[data-item="epswall"]').click();p.locator('#auto-place').click();p.locator('#wall-opening').select_option('door');p.locator('#apply-wall').click();p.reload();p.wait_for_function('window.GreenShiftPlanner');p.evaluate('document.querySelectorAll("aside").forEach(el=>el.scrollTop=0)');p.locator('#room-canvas').screenshot(path=str(ASSETS/'studio-interior.png'));p.screenshot(path=str(ASSETS/'renovation-playground-preview.png'))
 assert not errors,errors;print('Captured all six facade forms and six coordinated styles in both actual WebGL studios.');b.close()
