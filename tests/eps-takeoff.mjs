import assert from 'node:assert/strict';
import '../assets/asset-studio-model.js';
const EPS=globalThis.GreenShiftEPS;
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} ≠ ${b}`);
const base=()=>({room:{w:6,d:5},eps:EPS.defaults(),objects:[]});
const wall=(thickness=12,opening='solid',length=2.4)=>({id:'wall1',type:'epswall',length,height:2.7,thickness,opening});
for(const [thickness,expected] of [[10,.648],[12,.7776],[15,.972],[20,1.296]]){const p=base();p.objects=[wall(thickness)];const q=EPS.estimate(p);close(q.netArea,6.48);close(q.volume,expected);close(q.supplyVolume,expected*1.05);}
for(const [opening,area,volume] of [['door',1.89,.5508],['window',1.44,.6048],['both',3.33,.378]]){const p=base();p.objects=[wall(12,opening)];const q=EPS.estimate(p);close(q.openingArea,area);close(q.volume,volume);}
{const p=base();p.objects=[wall(10),{...wall(20,'door',3),id:'wall2'}];const q=EPS.estimate(p);close(q.volume,1.89);close(q.supplyVolume,1.9845);assert.deepEqual(q.groups.map(g=>g.thickness),[10,20]);}
{const p=base();p.eps={...p.eps,rear:true,left:true,height:3,thickness:20,rearOpenings:1.8,leftOpenings:1.2,waste:10};const q=EPS.estimate(p);close(q.grossArea,32.4);close(q.openingArea,3);close(q.netArea,29.4);close(q.volume,5.88);close(q.supplyVolume,6.468);close(q.cornerDeduction,.6);const a=EPS.estimate({...p,eps:{...p.eps,left:false}}),b=EPS.estimate({...p,eps:{...p.eps,rear:false}});close(a.volume+b.volume-q.volume,.12);for(const s of q.surfaces)close(s.holes.reduce((n,h)=>n+h.w*h.h,0),s.openingArea);}
{const p=base();p.objects=[{id:'glass',type:'partition'}];close(EPS.estimate(p).volume,0);close(EPS.estimate(p).supplyVolume,0);}
for(const invalid of [{thickness:11},{thickness:'12'},{waste:-1},{waste:21},{height:2.3},{height:5},{rearOpenings:-1}])assert.throws(()=>EPS.normalize({...EPS.defaults(),...invalid}));
assert.throws(()=>EPS.estimate({...base(),eps:{...EPS.defaults(),rear:true,rearOpenings:100}}));
assert.throws(()=>EPS.wall(wall(12,'door',.8),EPS.defaults()));
assert.throws(()=>EPS.wall({...wall(),height:3.5},EPS.defaults()));
assert.throws(()=>EPS.wall({...wall(),length:NaN},EPS.defaults()));
console.log('EPS takeoff passed: four thicknesses, doors/windows, mixed cores, corner joint, openings, allowance, scope exclusion and invalid inputs.');
