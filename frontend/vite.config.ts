import { defineConfig } from 'vite';
import { svelte } from '@sveltejs/vite-plugin-svelte';
import path from 'path';

export default defineConfig({
  plugins: [svelte()],
  build: {
    outDir: path.resolve(__dirname, '../backend/static'),
    emptyOutDir: true
  },
  server: {
    host: '0.0.0.0',
    port: 5173
  }
});
