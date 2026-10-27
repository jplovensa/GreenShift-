"""Measured EPS and the one-page Pass remain usable without WebGL."""
import os,subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright
BASE=os.environ.get('GREENSHIFT_TEST_URL','http://localhost:4175/GreenShift-/').rstrip('/')+'/'
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-webgl']);p=b.new_page(viewport={'width':1200,'height':900});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 for studio in ['renovation','facade']:
  p.goto(BASE+'assets/'+studio+'-studio.html?assembly=1&lang=en');p.locator('#assembly-dialog').wait_for(state='visible');assert p.locator('#ab-webgl').is_visible();p.locator('#ab-canvas').focus();p.keyboard.press('Escape');assert p.locator('#assembly-dialog').is_visible();p.locator('[data-workflow=eps]').click();p.locator('#ab-eps-only').click();p.locator('#ab-eps-length').fill('3');p.locator('#ab-eps-height').fill('3');p.locator('#ab-eps-add').click();assert abs(p.evaluate('GreenShiftAssemblyStudio.getTakeoff().volume')-1.08)<1e-9;p.locator('#ab-pass').click()
  with p.expect_download() as dl:p.locator('#gsp-top-pdf').click()
  assert 'Pages:           1' in subprocess.check_output(['pdfinfo',str(dl.value.path())],text=True);out=Path('/workspace/greenshift-planner-check')/(studio+'-fallback-Pass.pdf');dl.value.save_as(str(out));assert out.stat().st_size>20000;assert not errors,errors;print(studio+': disabled-WebGL measured editing and one-page plan-backed PDF passed.',flush=True)
 b.close()
