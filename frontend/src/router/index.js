// ─────────────────────────────────────────────────────────────────────────────
// Router — Vue Router 4 con lazy-loading e guardie RBAC
//
// Due gruppi funzionali (specchio di backend/core/permissions.py):
//   OPERATIVO    → RC / Segreteria Didattica / Segreteria di Sede
//   SUPERVISIONE → Responsabile Sede / Coordinamento
// ─────────────────────────────────────────────────────────────────────────────

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { RUOLI } from '@/utils/constants'

// ── Gruppi funzionali ───────────────────────────────────────────────────────
const OPERATIVO = [
  RUOLI.RESPONSABILE_CORSO,
  RUOLI.SEGRETERIA_DIDATTICA,
  RUOLI.SEGRETERIA_SEDE,
]

const SUPERVISIONE = [
  RUOLI.RESPONSABILE_SEDE,
  RUOLI.COORDINAMENTO,
]

const TUTTI = [...OPERATIVO, ...SUPERVISIONE]

// ── Rotte ───────────────────────────────────────────────────────────────────
const routes = [
  // ── Pubblica ──────────────────────────────────────────────────────────────
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/pages/LoginPage.vue'),
    meta: { public: true },
  },

  // ── Radice: redirect dinamico in base all'autenticazione ──────────────────
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
  // OPERATIVO — prenotazioni e gestione slot
  // (RC + Segreteria Didattica + Segreteria di Sede)
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/prenotazioni/nuova',
    name: 'NuovaPrenotazione',
    component: () => import('@/pages/operativo/NuovaPrenotazionePage.vue'),
    meta: { requiresAuth: true, roles: OPERATIVO },
  },
  {
    path: '/prenotazioni/massiva',
    name: 'PrenotazioneMassiva',
    component: () => import('@/pages/operativo/PrenotazioneMassivaPage.vue'),
    meta: { requiresAuth: true, roles: OPERATIVO },
  },
  {
    path: '/prenotazioni/mie',
    name: 'MiePrenotazioni',
    component: () => import('@/pages/operativo/MiePrenotazioniPage.vue'),
    meta: { requiresAuth: true, roles: OPERATIVO },
  },
  {
    path: '/prenotazioni/conflitti',
    name: 'GestioneConflitti',
    component: () => import('@/pages/operativo/GestioneConflittiPage.vue'),
    meta: { requiresAuth: true, roles: OPERATIVO },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // TUTTI — visualizzazione e report (operativo + supervisione)
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/aule/slot-liberi',
    name: 'SlotLiberi',
    component: () => import('@/pages/supervisione/SlotLiberiPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/sede/prenotazioni',
    name: 'PrenotazioniSede',
    component: () => import('@/pages/supervisione/PrenotazioniSedePage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/sede/saturazione',
    name: 'SaturazioneSpazi',
    component: () => import('@/pages/supervisione/SaturazioneSpazi.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },
  {
    path: '/report',
    name: 'Report',
    component: () => import('@/pages/supervisione/ReportPage.vue'),
    meta: { requiresAuth: true, roles: TUTTI },
  },

  // ──────────────────────────────────────────────────────────────────────────
  // COORDINAMENTO — admin (solo Coordinamento)
  // ──────────────────────────────────────────────────────────────────────────
  {
    path: '/coordinamento/globale',
    name: 'VistaGlobale',
    component: () => import('@/pages/coordinamento/VistaGlobalePage.vue'),
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