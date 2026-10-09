import { defineConfig } from 'vite';
export default defineConfig({server:{host:'0.0.0.0',allowedHosts:['terminal.local']},build:{rollupOptions:{input:{index:'index.html',cinematic:'cinematic.html',editorial:'editorial.html',atelier:'atelier.html'}}}});
