import { cp, mkdir, rm } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const output = new URL('../dist/', import.meta.url);
await rm(output, {recursive:true, force:true});
await mkdir(output, {recursive:true});
for (const file of ['index.html','cinematic.html','editorial.html','atelier.html','app.js','content.js','style.css','.nojekyll','assets']) {
  await cp(root + file, new URL(file, output), {recursive:true});
}
console.log('Static website built in dist/ — no npm dependencies or bundler required.');
