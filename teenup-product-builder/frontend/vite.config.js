import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  

  server: {
    host: true,           // bind 0.0.0.0
    port: 3000,
    strictPort: true,
    watch: {
      usePolling: true    
    }
  },
  
  // Build cho production
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})