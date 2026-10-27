"""Capture the actual HDR-lit Three.js model for the two homepage studio covers."""
import os,base64,io
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1600,'height':1000});p.set_default_navigation_timeout(90000)
 for studio,name in [('renovation','asset-repurposing-cover.webp'),('facade','facade-concept-cover.webp')]:
  p.goto(BASE+'assets/'+studio+'-studio.html?lang=en',wait_until='domcontentloaded');p.wait_for_function('GreenShiftAssemblyStudio.getRenderInfo().hdr',timeout=90000);p.locator('[data-workflow=materials]').click();p.locator('.ab-catalog summary').filter(has_text='03 / Finish & presentation').click();p.locator('#ab-cutaway').check();data=p.evaluate('GreenShiftAssemblyStudio.getRenderImages(2)[0]');im=Image.open(io.BytesIO(base64.b64decode(data.split(',')[1])));im.save(ROOT/'assets'/name,quality=93);print(name,str(im.size),flush=True)
 b.close()
