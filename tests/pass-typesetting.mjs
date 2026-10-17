import assert from 'node:assert/strict';import '../assets/pass-typesetting.js';
const T=globalThis.GreenShiftPassType,measure=s=>Array.from(s).reduce((n,c)=>n+(c==='W'?14:c==='i'?3:8),0);
for(const value of ['A name with spaces and words. '.repeat(20),'W'.repeat(1000),'i'.repeat(1500),'日本語の計画'.repeat(100),'🏡🌱'.repeat(120),'Line one\n\nLine three','x\n'.repeat(80)]){
 const fit=T.fit(value,{width:210,height:91,fontSize:18,lineHeight:26,maxLines:3},measure);assert.ok(fit.lines.length<=3);for(const line of fit.lines)assert.ok(measure(line)<=210);assert.ok(fit.lines.length*fit.lineHeight<=91);
}
assert.deepEqual(T.lines('One\nTwo',210,measure),['One','Two']);assert.equal(T.fit('WWW '.repeat(100),{width:210,height:91,fontSize:18,lineHeight:26,maxLines:3},measure).truncated,true);
console.log('Pass typesetting: bounded long words, CJK, emoji, explicit newlines, measured width, line count and truncation passed.');
