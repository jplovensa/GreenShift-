"""Render a concept-process film from the real local studios, without production hooks.
Requires ffmpeg, Python Playwright/Chromium and the production-path server on 4174.
Frames live in /tmp; no client data or third-party footage is used.
"""
import base64,json,subprocess,re
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];FRAMES=Path('/tmp/greenshift-film');FRAMES.mkdir(exist_ok=True)
BASE='http://localhost:4174/GreenShift-/assets/'
FPS=24;DURATION=4;WIDTH=1280;HEIGHT=720
# The instrumentation is inserted only into the capture browser response.
HOOK='''
window.__filmFrame=(t,kind,chapter,title,detail)=>{
 renderer.setPixelRatio(1);renderer.setSize(1280,720,false);camera.aspect=16/9;camera.updateProjectionMatrix();
 const ease=t*t*(3-2*t);
 if(kind==='interior'){
  const radius=Math.max(state.room.w,state.room.d)*1.42;
  const a=.61+(ease-.5)*.2;
  camera.position.set(Math.sin(a)*radius,5.7-ease*.35,Math.cos(a)*radius);
  camera.lookAt(0,.75,0);roomGroup.traverse(o=>{if(o.userData.overhead)o.visible=false});if(grid)grid.visible=false;
 }else{
  const a=.29+(ease-.5)*.24,span=Math.max(state.w,state.h+state.roofRise,state.d+state.extension+state.formDepth)*1.65;
  camera.position.set(Math.sin(a)*span,state.h*.9+1-ease*.25,state.d/2+Math.cos(a)*span);
  camera.lookAt(0,state.h*.46,state.d/2);
 }
 camera.updateMatrixWorld();renderer.render(scene,camera);
 const c=document.createElement('canvas');c.width=1280;c.height=720;const x=c.getContext('2d');
 x.drawImage(renderer.domElement,0,0,1280,720);
 const shade=x.createLinearGradient(0,440,0,720);shade.addColorStop(0,'rgba(5,25,20,0)');shade.addColorStop(1,'rgba(5,25,20,.94)');x.fillStyle=shade;x.fillRect(0,440,1280,280);
 x.fillStyle='#143a2d';x.fillRect(0,0,1280,44);x.fillStyle='#dbeadf';x.font='500 11px Inter';x.fillText('GREENSHIFT  /  DESIGN & DEVELOPMENT',40,28);x.textAlign='right';x.fillStyle='#acccbb';x.fillText('STUDIO CONCEPT FILM',1240,28);x.textAlign='left';
 x.fillStyle='#a7e2c5';x.font='500 12px Inter';x.fillText(chapter.toUpperCase(),40,567);
 x.fillStyle='#fff';x.font='400 36px Inter';x.fillText(title,40,618);
 x.fillStyle='#d4dfd7';x.font='400 15px Inter';x.fillText(detail,40,654);
 x.fillStyle='#9ab7a6';x.font='400 10px Inter';x.fillText('ILLUSTRATIVE DESIGN STUDY / GREENSHIFT STUDIO MODELS',40,697);
 x.fillStyle='#ffffff30';x.fillRect(890,692,350,1);x.fillStyle='#a7e2c5';x.fillRect(890,692,350*t,1);
 return c.toDataURL('image/jpeg',.94).split(',')[1];
};
'''
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path='/usr/bin/chromium',args=['--no-sandbox','--enable-unsafe-swiftshader','--use-angle=swiftshader']);p=b.new_page(viewport={'width':1440,'height':1000});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
 def instrument(route):
  name=route.request.url.split('/')[-1].split('?')[0]
  src=(ROOT/'assets'/name).read_text();a=src.rfind('})();');src=src[:a]+HOOK+src[a:];route.fulfill(status=200,content_type='application/javascript',body=src)
 p.route(re.compile(r'/(?:renovation|facade)-studio\.js(?:\?.*)?$'),instrument)
 shots=[]
 def capture(name,kind,chapter,title,detail):
  p.wait_for_timeout(150);p.evaluate('document.fonts.ready');folder=FRAMES/name;folder.mkdir(exist_ok=True)
  for i in range(FPS*DURATION):
   data=p.evaluate('([t,k,c,h,d])=>__filmFrame(t,k,c,h,d)',[i/(FPS*DURATION-1),kind,chapter,title,detail]);(folder/f'{i:04}.jpg').write_bytes(base64.b64decode(data))
  out=FRAMES/(name+'.mp4');subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(folder/'%04d.jpg'),'-c:v','libx264','-preset','medium','-crf','19','-pix_fmt','yuv420p',str(out)],check=True);shots.append(out);print('Rendered '+name,flush=True)
 p.goto(BASE+'renovation-studio.html?guided=1&v=studio4');p.wait_for_function('window.__filmFrame&&window.GreenShiftPlanner');p.locator('[data-style="japandi"]').click()
 p.locator('[data-item="epswall"]').click();p.locator('#auto-place').click();p.locator('#wall-opening').select_option('door');p.locator('#apply-wall').click()
 p.locator('[data-build-stage="existing"]').click()
 capture('01-retain','interior','01 / Read the space','Retain the asset.','Start with the existing shell. Understand what can work harder.')
 p.locator('[data-build-stage="eps"]').click();q=p.evaluate('GreenShiftPlanner.getTakeoff()');plan=p.evaluate('GreenShiftPlanner.getPlan()');print('Interior capture takeoff: '+json.dumps(q),flush=True)
 capture('02-plan','interior','02 / Shape the plan','Give the space a new purpose.','Place measured EPS partitions. Coordinate openings and movement.')
 p.locator('[data-build-stage="proposed"]').click()
 capture('03-finish','interior','03 / Material & light','Make the design tangible.','Review finishes, furniture and lighting as one coordinated direction.')
 p.goto(BASE+'facade-studio.html?guided=1&v=studio4');p.wait_for_function('window.__filmFrame&&window.GreenShiftFacadeStudio');p.locator('[data-form="curve"]').click();p.locator('[data-style="tropical"]').click();p.locator('[data-build-stage="eps"]').click()
 capture('04-envelope','facade','04 / Form & envelope','Change the building’s presence.','Explore curved profiles, measured openings and the EPS envelope.')
 p.locator('[data-build-stage="proposed"]').click()
 capture('05-present','facade','05 / Present the concept','Review the direction. Together.','Walk the interior. Explore the facade. Take the concept into development.')
 assert not errors,errors;b.close()
# Editorial dissolves join the five original, moving WebGL shots.
cmd=['ffmpeg','-y','-loglevel','error','-filter_complex_threads','1']
for shot in shots:cmd+=['-i',str(shot)]
filters=[];previous='0:v'
for i in range(1,len(shots)):
 out=f'x{i}';filters.append(f'[{previous}][{i}:v]xfade=transition=fade:duration=0.5:offset={3.5*i}[{out}]');previous=out
filters.append(f'[{previous}]scale=in_range=full:out_range=limited,format=yuv420p[film]');previous='film'
cmd+=['-filter_complex',';'.join(filters),'-map',f'[{previous}]','-c:v','libx264','-preset','slow','-crf','20','-pix_fmt','yuv420p','-color_range','tv','-movflags','+faststart','-an',str(ROOT/'assets/studio-process-film.mp4')];subprocess.run(cmd,check=True)
subprocess.run(['ffmpeg','-y','-loglevel','error','-ss','8.5','-i',str(ROOT/'assets/studio-process-film.mp4'),'-frames:v','1','-q:v','2',str(ROOT/'assets/studio-process-film-poster.jpg')],check=True)
print('Built studio-process-film.mp4: five real-model sequences, 18s, 1280×720 / 24fps.',flush=True)
