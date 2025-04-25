import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src')
    }
  },
  build: {
    assetsInlineLimit: 0, // 禁用小资源内联，确保所有图片作为单独文件处理
    rollupOptions: {
      output: {
        manualChunks: {
          mapbox: ['mapbox-gl']
        }
      }
    }
  },
  server: {
    host: true
  }
})
