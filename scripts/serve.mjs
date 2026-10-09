import http from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const args=process.argv.slice(2);
const value=(key,fallback)=>args.includes(key)?args[args.indexOf(key)+1]:fallback;
const port=Number(value('--port','4173'));
const root=fileURLToPath(new URL(args.includes('--dist')?'../dist/':'../',import.meta.url));
const base=value('--base','/').replace(/\/$/,'');
const types={html:'text/html; charset=utf-8',js:'text/javascript; charset=utf-8',css:'text/css; charset=utf-8',png:'image/png',jpg:'image/jpeg',mp4:'video/mp4',woff2:'font/woff2'};
http.createServer(async(req,res)=>{
 try {
  let route=decodeURIComponent(new URL(req.url,'http://localhost').pathname);
  if(base && route!==base && !route.startsWith(base+'/')){res.writeHead(404).end();return;}
  route=route.slice(base.length).replace(/^\//,'')||'index.html';
  if(!/^(index\.html|cinematic\.html|editorial\.html|atelier\.html|app\.js|content\.js|style\.css|assets\/[A-Za-z0-9_.-]+)$/.test(route)){res.writeHead(404).end();return;}
  const body=await readFile(root+route);
  res.writeHead(200,{'Content-Type':types[route.split('.').pop()]||'application/octet-stream','Content-Length':body.length});
  res.end(req.method==='HEAD'?undefined:body);
 } catch {res.writeHead(404).end('Not found');}
}).listen(port,'0.0.0.0',()=>console.log(`GreenShift static server running on port ${port}${base||'/'}`));
