import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // This is important for Docker to expose the server correctly
    // and for the dev server to be accessible from outside the container.
    host: '0.0.0.0',
    port: 8080 // You can specify the port you want to use
  }
})