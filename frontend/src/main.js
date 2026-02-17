import { createApp } from 'vue'
import { createPinia } from 'pinia'

// Bootstrap Italia: design system della PA italiana
import 'bootstrap-italia/dist/css/bootstrap-italia.min.css'
import 'bootstrap-italia/dist/js/bootstrap-italia.bundle.min.js'

// Foglio di stile custom (decommentare quando pronto)
// import '@/assets/custom.css'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

async function avviaApp() {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)

  // ── Verifica token PRIMA di montare l'app e avviare il router ─────────────
  // Questo impedisce il flash della dashboard quando il token è scaduto
  // e garantisce che isAuthenticated sia corretto al primo render.
  const authStore = useAuthStore()
  await authStore.init()

  app.use(router)
  app.mount('#app')
}

avviaApp()
