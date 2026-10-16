import assert from 'node:assert/strict';
import '../assets/facade-model.js';
const M=globalThis.GreenShiftFacade,base=M.defaults(),close=(a,b,t=1e-7)=>assert.ok(Math.abs(a-b)<t,`${a} != ${b}`);
const values=[];
for(const form of Object.keys(M.forms))for(const thickness of [10,12,15,20]){
 const p={...base,form,thickness,roof:form==='gable'?'gable':form==='asymmetric'?'skillion':'flat'},q=M.estimate(p),full=M.geometry(p,{holes:false}),holes=M.openings(p),holeVolumes=holes.reduce((sum,h)=>sum+M.geometry(p,{holes:false,patch:h}).volume,0);
 close(q.volume,full.volume-holeVolumes);close(q.volume,M.meshVolume(M.geometry(p).renderPositions));close(q.frontFinishArea,full.netArea-holes.reduce((s,h)=>s+h.w*h.h,0));close(q.supplyVolume,q.volume*1.05);assert.ok(q.volume>0&&Number.isFinite(q.volume));values.push(q.volume);
 if(p.roof==='flat'){const pro=M.profile(p),inner=pro.points.map(v=>M.at(pro,v.s)),outer=pro.points.map(v=>M.at(pro,v.s,thickness/100)).reverse(),polygon=[...inner,...outer];const area=Math.abs(polygon.reduce((s,a,i)=>{const b=polygon[(i+1)%polygon.length];return s+a.x*b.z-b.x*a.z;},0))/2;close(full.volume,area*p.h);}
 const sides=M.estimate({...p,left:true,right:true,extension:1});close(sides.volume,sides.surfaces.reduce((n,s)=>n+s.volume,0));assert.ok(sides.additionalFootprint>=8);
}
assert.equal(new Set(values.map(v=>v.toFixed(5))).size,24);
{const p={...base,form:'curve'},pro=M.profile(p),R=p.w*p.w/(8*p.formDepth)+p.formDepth/2,arc=2*R*Math.asin(p.w/(2*R));assert.ok(Math.abs(pro.length-arc)/arc<.0001);assert.ok(M.estimate(p).volume>M.estimate(base).volume);}
{const p={...base,roof:'gable'},q=M.estimate(p);close(q.grossArea,base.w*(base.h+base.roofRise/2));close(q.volume,(q.grossArea-q.openingArea)*.12);}
{const p={...base,openingOverrides:[{name:'Window 2.1',x:-1.4,y:3.7,w:1.6,h:1.2}]},q=M.estimate(p);assert.equal(q.holes.find(h=>h.name==='Window 2.1').w,1.6);close(q.openingArea,10.82-2.1+1.92);}
for(const patch of [{form:'unknown'},{roof:'unknown'},{designStyle:'unknown'},{w:3,form:'curve',formDepth:2},{w:3,form:'wave',formDepth:3,thickness:20,bays:0},{openingOverrides:[{name:'Entrance',x:0,y:1,w:1,h:2}]},{openingOverrides:[{name:'Window 1.1',x:0,y:0,w:3,h:3}]}])assert.throws(()=>M.estimate({...base,...patch}));
close(M.estimate({...base,roof:'skillion'}).roofArea,6*Math.hypot(8,1.2));close(M.estimate({...base,roof:'gable'}).roofArea,12*Math.hypot(4,1.2));
console.log('Facade forms passed: 24 form/thickness combinations, independent polygon-volume integration, hole subtraction, arc convergence, roof area, returns, individual edits and invalid/tight profiles.');
