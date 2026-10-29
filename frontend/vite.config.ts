import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://127.0.0.1:8000',
      '/health': 'http://127.0.0.1:8000',
      '/users': 'http://127.0.0.1:8000',
      '/products': 'http://127.0.0.1:8000',
      '/simulate-error': 'http://127.0.0.1:8000',
      '/simulate-timeout': 'http://127.0.0.1:8000',
      '/simulate-rate-limit': 'http://127.0.0.1:8000',
      '/metrics': 'http://127.0.0.1:8000'
    }
  }
});

