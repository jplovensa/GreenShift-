import assert from 'node:assert/strict';import '../assets/assembly-model.js';import '../assets/modelling-tools.js';
const A=GreenShiftAssembly,M=GreenShiftModelling,near=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
const o=A.part('wall',{length:4,height:3,depth:.12,opening:'window',ow:1.2,oh:1.2,sill:.9}),p={...A.defaults(),w:12,d:12,h:6,parts:[o]},q=A.estimate(p).volume;
for(const axis of ['x','y','z']){const moved=M.move(p,[o.id],axis,.5);near(moved.parts[0][axis],.5);near(A.estimate(moved).volume,q);assert.equal(p.parts[0][axis],0);}
for(const angle of [15,90,137,359])near(A.estimate(M.rotate(p,[o.id],angle)).volume,q);
const pulled=M.pushPull(p,o.id,'length',1),w=pulled.parts[0];near(w.length,5);near(w.x,.5);near(w.x-w.length/2,-2);near(A.holes(w)[0].x+w.x,0);near(A.estimate(pulled).volume,q+3*.12);
const high=M.pushPull(p,o.id,'height',.5);near(high.parts[0].y,0);near(A.estimate(high).volume,q+4*.5*.12);
assert.throws(()=>M.pushPull(p,o.id,'depth',.05),/EPS thickness/);assert.throws(()=>M.pushPull(p,o.id,'length',-3.9));assert.throws(()=>M.move(p,[o.id],'y',-.1));assert.deepEqual(p.parts[0],o);
const rotated=M.rotate(p,[o.id],90),r=M.pushPull(rotated,o.id,'length',1).parts[0];near(r.z,-.5);near(r.x,0);const inferred=M.infer({...p,parts:[]},{x:0,z:0},{x:3,z:.1});near(inferred.z,0);assert.equal(inferred.inference,'x');assert.equal(M.infer({...p,parts:[]},{x:0,z:0},{x:.1,z:3}).inference,'z');
console.log('Modelling: XYZ moves, rotation-invariant EPS, anchored push/pull, fixed opening world positions, invalid edit preservation and axis inference passed.');

const floor={...A.defaults(),w:8,d:6,h:4.5,parts:[A.part('slab',{length:6,depth:5,height:.12})]};const drawn=A.drawWall(floor,{x:-1,z:0},{x:1,z:0},{base:.12});near(drawn.plan.parts.at(-1).y,.12);near(A.estimate(drawn.plan).volume,2*2.7*.12);

const pair={...A.defaults(),w:12,d:12,h:6,parts:[A.part('wall',{length:1,height:3,depth:.12,x:-2}),A.part('wall',{length:1,height:3,depth:.15,x:2})]};const rotatedPair=M.rotate(pair,pair.parts.map(p=>p.id),15);near(rotatedPair.parts[0].x,-2*Math.cos(Math.PI/12));near(rotatedPair.parts[0].z,2*Math.sin(Math.PI/12));near(A.estimate(rotatedPair).volume,A.estimate(pair).volume);
