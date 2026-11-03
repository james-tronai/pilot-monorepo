import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// In DevSpace the dev server runs inside the cluster; the two APIs are reached by their
// Service names (env set in devspace.yaml). Locally they default to localhost.
const orders = process.env.API_ORDERS_URL ?? 'http://localhost:8001'
const chat = process.env.API_CHAT_URL ?? 'http://localhost:8002'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api/orders': { target: orders, changeOrigin: true },
      '/api/chat': { target: chat, changeOrigin: true },
    },
  },
})
