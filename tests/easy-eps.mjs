import assert from 'node:assert/strict';
import '../assets/assembly-model.js';import '../assets/easy-eps.js';
const A=globalThis.GreenShiftAssembly,E=globalThis.GreenShiftEasyEPS,near=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
const input={unit:'m',length:'6',height:'3',thickness:'12',openings:[{kind:'door',width:'.9',height:'2.1',left:'.2',sill:0},{kind:'window',width:'1.2',height:'1.2',left:'2.4',sill:'.9'}]};
// Independent physical quantities: 18 m² gross - 1.89 door - 1.44 window = 14.67 m².
input.openings.forEach(o=>{for(const k of ['width','height','left','sill'])if(String(o[k]).startsWith('.'))o[k]='0'+o[k];});
for(const core of [10,12,15,20]){const q=E.measure({...input,thickness:core});near(q.gross,18);near(q.openings,3.33);near(q.net,14.67);near(q.volume,14.67*core/100);const p={...A.defaults(),w:8,d:6,h:4,parts:[q.wall]};near(A.estimate(p).volume,q.volume);near(A.estimate({...p,parts:[{...q.wall,angle:15}]}).volume,q.volume);assert.deepEqual(A.normalize(JSON.parse(JSON.stringify(p))),A.normalize(p));}
const metric=E.measure(input),cm={...input,unit:'cm',length:600,height:300,openings:input.openings.map(o=>Object.fromEntries(Object.entries(o).map(([k,v])=>[k,k==='kind'?v:Number(v)*100])))};near(E.measure(cm).volume,metric.volume);near(E.measure({...input,length:'6,0',height:'3,0'}).volume,metric.volume);
assert.throws(()=>E.measure({...input,length:''}));assert.throws(()=>E.measure({...input,length:'1,000.0'}));assert.throws(()=>E.measure({...input,openings:[...input.openings,input.openings[0]]}),/overlap/);assert.throws(()=>E.measure({...input,openings:[{...input.openings[0],left:'5.5'}]}),/fit/);assert.throws(()=>E.measure({...input,openings:[{...input.openings[0],left:'0'}]}),/fit/);
// Solids can fill a measured cutout; collision rejects filling the actual EPS next to it.
const p={...A.defaults(),w:8,d:6,h:4,parts:[metric.wall]},doorGlass=A.part('glass',{length:.8,height:2,depth:.03,x:-2.35,y:.01});assert.doesNotThrow(()=>A.normalize({...p,parts:[...p.parts,doorGlass]}));assert.throws(()=>A.normalize({...p,parts:[...p.parts,{...doorGlass,x:-1}]}),/overlap/);
console.log('Beginner EPS: four cores, independent multi-opening area, metres/centimetres/comma equivalence, opening fit and overlap rejection, cutout collisions, rotation and JSON restore passed.');
