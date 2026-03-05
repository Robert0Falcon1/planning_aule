// ─────────────────────────────────────────────────────────────────────────────
// Router — Vue Router 4 con lazy-loading e guardie RBAC
//
// Architettura semplificata a 2 gruppi funzionali:
//   OPERATIVO      → può prenotare, vedere le proprie prenotazioni, conflitti, sedi
//   COORDINAMENTO  → tutto ciò che fa OPERATIVO + dashboard aggregata, report,
//                    grafici, gestione utenti, gestione sedi/aule
//
// Specchio di backend/core/permissions.py
// ─────────────────────────────────────────────────────────────────────────────
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// ── Costanti ruolo ───────────────────────────────────────────────────────────
// Definite inline per non dipendere da utils/constants.js durante il boot.
// Devono essere identiche ai valori restituiti dall'API (campo `ruolo` dell'utente).
const RUOLO = {
  OPERATIVO:      'OPERATIVO',
  COORDINAMENTO:  'COORDINAMENTO',
}

const TUTTI = [RUOLO.OPERATIVO, RUOLO.COORDINAMENTO]
const SOLO_COORDINAMENTO = [RUOLO.COORDINAMENTO]

// ── Rotte ────────────────────────────────────────────────────────────────────
const routes = [

  // ── Pubblica ────────────────────────────────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { public: true },
  },

  // ── Radice: redirect dinamico basato su ruolo ────────────────────────────────
  {
    path: '/',
    name: 'Home',
    redirect: () => {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) return { name: 'Login' }
      return auth.ruolo === RUOLO.COORDINAMENTO
        ? { name: 'DashboardCoordinamento' }
        : { name: 'DashboardOperativo' }
    },
  },

  // ── Dashboard OPERATIVO ──────────────────────────────────────────────────────
  {
    path: '/operativo/dashboard',
    name: 'DashboardOperativo',
    component: () => import('@/pages/operativo/DashboardOperativoPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },

  // ── Dashboard COORDINAMENTO ─────────────────────────────────────────────────
  {
    path: '/coordinamento/dashboard',
    name: 'DashboardCoordinamento',
    component: () => import('@/pages/coordinamento/DashboardCoordinamentoPage.vue'),
    meta: { requiresAuth: true, roles: SOLO_COORDINAMENTO },
  },

  // ────────────────────────────────────────────────────────────────────────────
  // CONDIVISE — accessibili da entrambi i ruoli
  // ────────────────────────────────────────────────────────────────────────────

  {
    path: '/calendario',
    name: 'Calendario',
    component: () => import('@/pages/shared/CalendarioPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/prenotazioni/nuova',
    name: 'NuovaPrenotazione',
    // NuovaPrenotazionePage gestisce sia singola che massiva tramite tab interni
    component: () => import('@/pages/operativo/NuovaPrenotazionePage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/prenotazioni/mie',
    name: 'MiePrenotazioni',
    component: () => import('@/pages/operativo/MiePrenotazioniPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/conflitti',
    name: 'Conflitti',
    // ⚠ RINOMINA il tuo GestioneConflittiPage.vue → ConflittiPage.vue
    // oppure mantieni il vecchio nome e aggiorna solo l'import qui sotto
    component: () => import('@/pages/shared/ConflittiPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/sedi',
    name: 'SediAule',
    component: () => import('@/pages/shared/SediAulePage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },

  // ────────────────────────────────────────────────────────────────────────────
  // COORDINAMENTO ONLY — supervisione e amministrazione
  // ────────────────────────────────────────────────────────────────────────────

  {
    path: '/coordinamento/situazione-oggi',
    name: 'SituazioneOggi',
    component: () => import('@/pages/coordinamento/SituazioneOggiPage.vue'),
    meta: { requiresAuth: true, roles: SOLO_COORDINAMENTO },
  },
  {
    path: '/coordinamento/grafici',
    name: 'Grafici',
    component: () => import('@/pages/coordinamento/GraficiPage.vue'),
    meta: { requiresAuth: true, roles: SOLO_COORDINAMENTO },
  },
  {
    path: '/coordinamento/utenti',
    name: 'GestioneUtenti',
    component: () => import('@/pages/coordinamento/GestioneUtentiPage.vue'),
    meta: { requiresAuth: true, roles: SOLO_COORDINAMENTO },
  },
  {
    path: '/coordinamento/sedi',
    name: 'GestioneSediAule',
    component: () => import('@/pages/coordinamento/GestioneSediAulePage.vue'),
    meta: { requiresAuth: true, roles: SOLO_COORDINAMENTO },
  },

  // ── Fallback 404 ─────────────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFoundPage.vue'),
  },
]

// ── Istanza router ────────────────────────────────────────────────────────────
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// ── Guardia globale ───────────────────────────────────────────────────────────
router.beforeEach((to) => {
  const auth = useAuthStore()

  // Rotta pubblica → sempre accessibile
  if (to.meta.public) return true

  // Rotta protetta senza autenticazione → redirect al login
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'Login', query: { redirect: to.fullPath } }
  }

  // Controllo RBAC: se la rotta ha `roles`, il ruolo dell'utente deve essere incluso
  const rolesRichiesti = to.meta.roles
  if (rolesRichiesti && !rolesRichiesti.includes(auth.ruolo)) {
    // Redirect alla dashboard corretta invece di rimbalzare all'infinito
    const fallback = auth.ruolo === RUOLO.COORDINAMENTO
      ? { name: 'DashboardCoordinamento' }
      : { name: 'DashboardOperativo' }
    return fallback
  }

  return true
})

export default router