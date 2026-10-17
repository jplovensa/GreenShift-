"""Exercise the timed intro on the production Pages path, including failure exits."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
BASE='http://localhost:4174/GreenShift-/'
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox'])
    errors=[]
    for width,height in [(1440,900),(390,844),(844,390)]:
        page=browser.new_page(viewport={'width':width,'height':height})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.add_init_script("new MutationObserver(()=>{const n=document.querySelector('.intro-number');if(n&&window.introStart===undefined)window.introStart=n.textContent}).observe(document,{subtree:true,childList:true})")
        page.goto(BASE,wait_until='domcontentloaded')
        page.wait_for_selector('.intro-number')
        assert page.evaluate('window.introStart')=='540'
        assert page.locator('#app').evaluate('(e)=>e.inert')
        page.wait_for_timeout(1400)
        assert page.locator('.intro-video').evaluate('(v)=>!v.paused&&v.currentTime>0'), 'Intro footage did not play'
        n=int(page.locator('.intro-number').inner_text());assert 45<n<540,n
        page.screenshot(path=str(ROOT/f'verification/cinematic-count-{width}.png'))
        page.wait_for_function('document.querySelector(".studio-intro")?.classList.contains("is-arrived")')
        assert page.locator('.intro-number').inner_text()=='45'
        page.screenshot(path=str(ROOT/f'verification/cinematic-45-{width}.png'))
        page.wait_for_function('document.querySelector(".studio-intro")?.classList.contains("is-brand")')
        page.wait_for_timeout(950)
        page.screenshot(path=str(ROOT/f'verification/cinematic-brand-{width}.png'))
        assert page.locator('.intro-brand img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)')
        page.wait_for_selector('.studio-intro',state='detached',timeout=5000)
        assert not page.locator('#app').evaluate('(e)=>e.inert')
        assert not page.locator('body').evaluate('(e)=>e.classList.contains("intro-open")')
        assert page.locator('#hero').is_visible()
        print(f'{width}×{height}: countdown, 45 hold, brand reveal and homepage exit passed.',flush=True)
        page.close()
    for exit in ['click','Escape','reduced','failed-video','stalled-animation','hidden-tab','no-script']:
        page=browser.new_page(reduced_motion='reduce' if exit=='reduced' else 'no-preference',java_script_enabled=exit!='no-script')
        page.on('pageerror',lambda e:errors.append(str(e)))
        if exit=='stalled-animation':page.add_init_script('window.requestAnimationFrame=()=>1')
        if exit=='failed-video':page.route('**/*.mp4',lambda r:r.abort())
        page.goto(BASE,wait_until='domcontentloaded')
        if exit=='click':
            assert page.locator('.intro-skip').evaluate('(e)=>e===document.activeElement')
            page.keyboard.press('Tab');assert page.locator('.intro-skip').evaluate('(e)=>e===document.activeElement')
            page.locator('.intro-skip').click()
        elif exit=='Escape':page.keyboard.press('Escape')
        elif exit=='hidden-tab':page.evaluate("Object.defineProperty(document,'hidden',{value:true});document.dispatchEvent(new Event('visibilitychange'))")
        elif exit=='reduced':assert page.locator('.studio-intro').evaluate('(e)=>e.classList.contains("is-reduced")')
        page.wait_for_selector('.studio-intro',state='detached',timeout=9500)
        assert not page.locator('#app').evaluate('(e)=>e.inert')
        assert page.locator('#hero').is_visible()
        if exit in ['click','Escape']:assert page.locator('#app a').first.evaluate('(e)=>e===document.activeElement')
        print(exit+': homepage accessible.',flush=True)
        page.close()
    assert not errors,errors
    browser.close()
