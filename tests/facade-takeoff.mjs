import assert from 'node:assert/strict';
import '../assets/facade-model.js';
import '../assets/asset-studio-model.js';
const F=globalThis.GreenShiftFacade,E=globalThis.GreenShiftEPS,close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const p=F.defaults();
for(const t of [10,12,15,20]){const q=F.estimate({...p,thickness:t});close(q.grossArea,48);close(q.openingArea,10.82);close(q.netArea,37.18);close(q.volume,37.18*t/100);close(q.supplyVolume,q.volume*1.05);}
{const q=F.estimate({...p,left:true,right:true,thickness:20,extension:1.5,waste:10});close(q.netArea,37.18+2*7.7*6);close(q.volume,25.916);close(q.supplyVolume,28.5076);close(q.extensionArea,12);for(const s of q.surfaces)close(s.netArea,s.grossArea-s.openingArea);}
{const q=F.estimate({...p,front:false,left:true,right:true,thickness:20});close(q.volume,14.4);close(q.openingArea,0);assert.equal(q.surfaces.length,2);close(q.returnJointLength,0);}
{const q=F.estimate({...p,front:false});close(q.volume,0);close(q.supplyVolume,0);}
{const q=F.estimate({...p,bays:0});close(q.openingArea,2.42);assert.equal(q.holes.length,1);}
for(const invalid of [{windowW:3,bays:4},{doorH:4},{h:3,floors:2},{thickness:11},{w:NaN},{front:'yes'},{extension:4},{windowH:2.4,h:2.4,floors:1}])assert.throws(()=>F.estimate({...p,...invalid}));
{const wall={id:'custom',type:'epswall',length:3.17,height:2.71,thickness:15,opening:'both',doorWidth:1.01,doorHeight:2.13,windowWidth:1.23,windowHeight:1.11,windowSill:.8};const eps={...E.defaults(),height:2.71};const q=E.estimate({room:{w:8,d:6},eps,objects:[wall]});close(q.openingArea,1.01*2.13+1.23*1.11);close(q.volume,(3.17*2.71-1.01*2.13-1.23*1.11)*.15);for(const angle of [0,15,37,90,180,270,359])close(E.estimate({room:{w:8,d:6},eps,objects:[{...wall,angle}]}).volume,q.volume);assert.throws(()=>E.wall({...wall,windowWidth:3},eps));assert.throws(()=>E.wall({...wall,doorWidth:NaN},eps));assert.throws(()=>E.wall({...wall,windowSill:-1},eps));}
console.log('Facade and measured-opening takeoffs passed: 4 thicknesses, selected surfaces, exterior butt joints, extension, allowance, validation, custom cutouts and rotation-invariant volume.');
