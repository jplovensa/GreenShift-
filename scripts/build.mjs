import { cp, mkdir, rm, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const output = new URL('../dist/', import.meta.url);
await rm(output, {recursive:true, force:true});
await mkdir(output, {recursive:true});
// Keep embedded behavior and styles synchronized with the editable source.
let html = await readFile(root + 'index.html', 'utf8');
for (const [id, file] of [['studio-styles', 'style.css'], ['studio-behavior', 'app.js'], ['studio-data', 'content.json']]) {
  let value = await readFile(root + file, 'utf8');
  if (id === 'studio-data') value = value.replaceAll('<', '\\u003c');
  const tag = id === 'studio-styles' ? 'style' : 'script';
  const pattern = new RegExp(`(<${tag} id="${id}"[^>]*>)[\\s\\S]*?(<\\/${tag}>)`);
  if (!pattern.test(html)) throw new Error(`Missing embedded section: ${id}`);
  html = html.replace(pattern, (_, start, end) => start + value + end);
}
await writeFile(root + 'index.html', html);
await writeFile(root + 'cinematic.html', html);
for (const file of ['index.html','cinematic.html','editorial.html','atelier.html','app.js','content.js','style.css','.nojekyll','assets']) {
  await cp(root + file, new URL(file, output), {recursive:true});
}
console.log('Static website built in dist/ — no npm dependencies or bundler required.');
