import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/analyze': 'http://localhost:8000',
      '/scrape': 'http://localhost:8000',
      '/find_linkedin': 'http://localhost:8000',
      '/check_internet': 'http://localhost:8000'
    }
  }
});
