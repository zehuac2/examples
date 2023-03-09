import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  assetsInclude: ['**/*.mp3'],
  base: '/static/',
  server: {
    origin: 'http://localhost:3000',
  },
  build: {
    outDir: 'static',
    manifest: true,
    emptyOutDir: false,
    rollupOptions: {
      input: path.join('src', 'index.js'),
    },
  },
});
