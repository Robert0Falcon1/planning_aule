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
        <aside class="col-lg-2 col-md-3 d-none d-md-block">
          <AppSidebar />
        </aside>
        <main class="col-lg-10 col-md-9 col-12 p-4">
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
import AppHeader   from '@/components/layout/AppHeader.vue'
import AppSidebar  from '@/components/layout/AppSidebar.vue'
import AppFooter   from '@/components/layout/AppFooter.vue'
import AlertBanner from '@/components/ui/AlertBanner.vue'

const authStore = useAuthStore()
</script>
