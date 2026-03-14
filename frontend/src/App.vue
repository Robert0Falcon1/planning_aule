<template>
  <!--
    Mostra uno splash minimo mentre init() verifica il token.
    Evita il flash della dashboard (o della login) prima che
    isAuthenticated sia stato stabilito con certezza.
  -->
  <div v-if="!authStore.inizializzato" class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="progress-spinner progress-spinner-active" role="status">
      <span class="visually-hidden">Caricamento...</span>
    </div>
  </div>

  <!-- Layout autenticato: header + sidebar + contenuto -->
  <div v-else-if="authStore.isAuthenticated" class="it-header-wrapper">
    <AppHeader />

    <div class="container-fluid p-0">
      <div class="row g-0">
        <!-- ═══ DESKTOP: Sidebar classica ═══ -->
        <aside 
          class="sidebar-desktop d-none d-md-block border-right-muted"
          :class="{ 'sidebar-collapsed': !sidebarIsOpen }">
          <AppSidebar />
        </aside>

        <main 
          class="main-content p-4"
          :class="{ 'main-expanded': !sidebarIsOpen }">
          <AlertBanner />
          <router-view />
        </main>
      </div>
    </div>

    <AppFooter />
  </div>

  <!-- Layout pubblico (login): nessun chrome -->
  <div v-else>
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useSidebar } from '@/composables/useSidebar'
import AppHeader from '@/components/layout/AppHeader.vue'
import AppSidebar from '@/components/layout/AppSidebar.vue'
import AppFooter from '@/components/layout/AppFooter.vue'
import AlertBanner from '@/components/ui/AlertBanner.vue'

const authStore = useAuthStore()
const { isOpen: sidebarIsOpen } = useSidebar()
</script>

<style scoped>
.sidebar-desktop {
  width: 280px;
  flex-shrink: 0;
  transition: margin-left 0.3s ease-in-out;
}

.sidebar-collapsed {
  margin-left: -280px;
}

.main-content {
  flex: 1;
  transition: margin-left 0.3s ease-in-out;
  width: calc(100% - 280px);
}

.main-expanded {
  width: 100%;
  margin-left: 0;
}

.row {
  display: flex;
  flex-wrap: nowrap;
}

/* ── Layout principale ───────────────────────────────────────── */
.it-header-wrapper {
  display: flex;
  flex-direction: column;
  min-height: 100vh;        /* occupa tutta la viewport */
}

.container-fluid {
  flex: 1;                  /* cresce e spinge il footer in fondo */
  display: flex;
  flex-direction: column;
}

.row {
  display: flex;
  flex-wrap: nowrap;
  flex: 1;                  /* la row occupa tutto lo spazio del container */
}

/* ── Sidebar ─────────────────────────────────────────────────── */
.sidebar-desktop {
  width: 280px;
  flex-shrink: 0;
  transition: margin-left 0.3s ease-in-out;
}

.sidebar-collapsed {
  margin-left: -280px;
}

/* ── Main content ────────────────────────────────────────────── */
.main-content {
  flex: 1;
  transition: margin-left 0.3s ease-in-out;
  width: calc(100% - 280px);
}

.main-expanded {
  width: 100%;
  margin-left: 0;
}
</style>