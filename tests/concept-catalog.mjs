import assert from 'node:assert/strict';
import '../assets/assembly-model.js';import '../assets/concept-catalog.js';
const A=globalThis.GreenShiftAssembly,C=globalThis.GreenShiftConcepts,near=(a,b)=>assert.ok(Math.abs(a-b)<1e-7,`${a} != ${b}`);
let count=0;
for(const context of ['interior','facade'])for(const [program,variants] of Object.entries(C.variants))for(const variant of Object.keys(variants)){
 const p=C.create(context,program,variant,C.features[program]);assert.equal(p.brief.program,program);assert.equal(p.brief.variant,variant);assert.ok(p.parts.some(o=>A.referenceTypes.includes(o.type)));assert.ok(p.parts.some(o=>o.type==='glass'));const q=A.estimate(p);assert.ok(q.volume>0);near(A.estimate({...p,showFurniture:false,cutaway:false}).volume,q.volume);
 const withoutReferences={...p,parts:p.parts.filter(o=>!A.referenceTypes.includes(o.type))};near(A.estimate(withoutReferences).volume,q.volume);const restored=A.normalize(JSON.parse(JSON.stringify(p)));assert.deepEqual(restored,p);
 const minimal=C.applyFeatures(p,[]);assert.ok(minimal.parts.length<p.parts.length);near(A.estimate(minimal).volume,q.volume);assert.equal(minimal.brief.features.length,0);const readded=C.applyFeatures(minimal,C.features[program]);assert.deepEqual(readded.brief.features,C.features[program]);near(A.estimate(readded).volume,q.volume);count++;
}
const p=C.create('interior','villa','family');p.brief.client='Ayu & Martin';p.brief.project='Rumah Senja';p.brief.questions='Retain the structure?';assert.equal(A.normalize(p).brief.questions,p.brief.questions);assert.throws(()=>A.normalize({...p,brief:{...p.brief,program:'unknown'}}));assert.throws(()=>A.normalize({...p,brief:{...p.brief,client:'x'.repeat(101)}}));assert.throws(()=>A.normalize({...p,light:'laser'}));
console.log(`${count} concept/context combinations: all features, furnished layouts, glazing cutouts, no overlaps, EPS exclusion, hide/cutaway invariance, feature removal/reapply, metadata and JSON restore passed.`);
