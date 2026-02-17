// ─────────────────────────────────────────────────────────────────────────────
// Router — Vue Router 4 con lazy-loading e guardie RBAC
// ─────────────────────────────────────────────────────────────────────────────

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { RUOLI } from '@/utils/constants'

const routes = [
  // ── Pubblica ──────────────────────────────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { public: true },
  },

  // ── Radice: redirect dinamico in base all'autenticazione ──────────────────
  // NON usiamo un redirect statico a /dashboard perché vogliamo mandare
  // al login gli utenti non autenticati senza passare per la guardia intermedia.
  {
    path: '/',
    name: 'Home',
    redirect: () => {
      const authStore = useAuthStore()
      return authStore.isAuthenticated ? { name: 'Dashboard' } : { name: 'Login' }
    },
  },

  // ── Dashboard (dispatcher per ruolo) ──────────────────────────────────────
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/pages/DashboardPage.vue'),
    meta: { requiresAuth: true },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // RESPONSABILE CORSO
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/prenotazioni/nuova',
    name: 'NuovaPrenotazione',
    component: () => import('@/pages/responsabile-corso/NuovaPrenotazionePage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.RESPONSABILE_CORSO] },
  },
  {
    path: '/prenotazioni/massiva',
    name: 'PrenotazioneMassiva',
    component: () => import('@/pages/responsabile-corso/PrenotazioneMassivaPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.RESPONSABILE_CORSO] },
  },
  {
    path: '/prenotazioni/mie',
    name: 'MiePrenotazioni',
    component: () => import('@/pages/responsabile-corso/MiePrenotazioniPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.RESPONSABILE_CORSO] },
  },
  {
    path: '/aule/slot-liberi',
    name: 'SlotLiberi',
    component: () => import('@/pages/responsabile-corso/SlotLiberiPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.RESPONSABILE_CORSO] },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // SEGRETERIA DI SEDE
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/segreteria/richieste',
    name: 'RichiestePendenti',
    component: () => import('@/pages/segreteria-sede/RichiestePendentiPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.SEGRETERIA_SEDE] },
  },
  {
    path: '/segreteria/conflitti',
    name: 'GestioneConflitti',
    component: () => import('@/pages/segreteria-sede/GestioneConflittiPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.SEGRETERIA_SEDE] },
  },
  {
    path: '/segreteria/calendario',
    name: 'CalendarioSede',
    component: () => import('@/pages/segreteria-sede/CalendarioSedePage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.SEGRETERIA_SEDE] },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // RESPONSABILE DI SEDE
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/sede/prenotazioni',
    name: 'PrenotazioniSede',
    component: () => import('@/pages/responsabile-sede/PrenotazioniSedePage.vue'),
    meta: {
      requiresAuth: true,
      roles: [RUOLI.RESPONSABILE_SEDE, RUOLI.SEGRETERIA_SEDE],
    },
  },
  {
    path: '/sede/saturazione',
    name: 'SaturazioneSpazi',
    component: () => import('@/pages/responsabile-sede/SaturazioneSpazi.vue'),
    meta: {
      requiresAuth: true,
      roles: [RUOLI.RESPONSABILE_SEDE, RUOLI.COORDINAMENTO],
    },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // SEGRETERIA DIDATTICA
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/didattica/corsi',
    name: 'PrenotazioniCorso',
    component: () => import('@/pages/segreteria-didattica/PrenotazioniCorsePage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.SEGRETERIA_DIDATTICA] },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // COORDINAMENTO
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/coordinamento/globale',
    name: 'VistaGlobale',
    component: () => import('@/pages/coordinamento/VistaGlobalePage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.COORDINAMENTO] },
  },
  {
    path: '/coordinamento/report',
    name: 'Report',
    component: () => import('@/pages/coordinamento/ReportSaturazionePage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.COORDINAMENTO] },
  },
  {
    path: '/coordinamento/utenti',
    name: 'GestioneUtenti',
    component: () => import('@/pages/coordinamento/GestioneUtentiPage.vue'),
    meta: { requiresAuth: true, roles: [RUOLI.COORDINAMENTO] },
  },

  // ── Fallback 404 ──────────────────────────────────────────────────────────
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/pages/NotFoundPage.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// ── Guardia globale ───────────────────────────────────────────────────────────
router.beforeEach((to) => {
  const authStore = useAuthStore()

  // Rotta pubblica: passa sempre
  if (to.meta.public) return true

  // Rotta protetta senza autenticazione → login
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'Login' }
  }

  // Controllo ruolo RBAC
  const rolesRichiesti = to.meta.roles
  if (rolesRichiesti && !rolesRichiesti.includes(authStore.ruolo)) {
    return { name: 'Dashboard' }
  }

  return true
})

export default router
