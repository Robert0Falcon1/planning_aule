<template>
  <!-- Slim header: nome ente -->
  <div class="it-header-slim-wrapper">
    <div class="container-fluid">
      <div class="it-header-slim-wrapper-content">
        <span class="navbar-brand">
          <router-link class="navbar-brand" :to="homePath">
            <img class="logo filter-logo hover-link" src="/img/logo_ICE.png">
          </router-link>
        </span>
        <div class="header-slim-right-zone">
          <button class="btn btn-sm btn-outline-light" @click="handleLogout">
            <svg class="icon icon-sm icon-light me-1">
              <use :href="sprites + '#it-logout'"></use>
            </svg>
            Esci
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Navbar principale -->
  <div class="it-header-navbar-wrapper theme-dark-desk theme-dark-mobile bg-primary">
    <div class="container-fluid">
      <div class="row mx-0">
        <div class="col-12 d-flex px-3">
          <nav class="navbar navbar-expand-md w-100 py-0" aria-label="Navigazione principale">
            <!-- <span class="fw-bold text-white me-3">Planning Aule</span> -->
            <div class="d-flex align-items-center py-2">
              <div class="d-flex">
                <span class="text-white d-flex justify-content-center align-items-center">
                  <svg class="icon icon-sm icon-light me-1">
                    <use :href="sprites + '#it-user'"></use>
                  </svg>
                  {{ authStore.nomeUtente }}
                </span>
              </div>
              <div class="d-flex">
                <span class="badge d-flex align-items-center justify-content-center my-2 ms-2 text-uppercase"
                  :class="authStore.ruolo === 'COORDINAMENTO' ? 'bg-warning text-dark' : 'badge-ruolo'">
                  {{ labelRuolo(authStore.ruolo) }}
                </span>
              </div>

            </div>

            <!-- Pulsante hamburger MOBILE -->
            <button class="btn text-white d-md-none ms-auto" style="padding-right: 5px;" type="button"
              data-bs-toggle="offcanvas" data-bs-target="#mobileSidebar" aria-controls="mobileSidebar"
              aria-label="Apri menu">
              ☰
            </button>

            <div class="collapse navbar-collapse" id="navbarPrincipal"></div>
          </nav>
        </div>
      </div>
    </div>
  </div>

  <!-- ═══ MOBILE: Offcanvas sidebar ═══ -->
  <div class="offcanvas offcanvas-start" tabindex="-1" id="mobileSidebar" aria-labelledby="mobileSidebarLabel"
    style="width: 280px;">
    <div class="offcanvas-header justify-content-flex-end">
      <!-- <h5 class="offcanvas-title" id="mobileSidebarLabel">Menu</h5> -->
      <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Chiudi menu"></button>
    </div>
    <div class="offcanvas-body p-0">
      <!-- Contenuto sidebar duplicato per mobile -->
      <nav class="bg-white h-100 py-4" aria-label="Menu laterale mobile">
        <ul class="nav flex-column px-2">
          <template v-if="authStore.isOperativo || authStore.isCoordinamento">
            <SidebarSection titolo="Prenotazioni">
              <SidebarLink :to="{ name: 'NuovaPrenotazione' }" icon="it-plus-circle" label="Nuova Prenotazione" />
              <SidebarLink :to="{ name: 'MiePrenotazioni' }" icon="it-list"
                :label="authStore.isCoordinamento ? 'Riepilogo Prenotazioni' : 'Le Mie Prenotazioni'" />
              <SidebarLink :to="{ name: 'Calendario' }" icon="it-calendar" label="Calendario" />
            </SidebarSection>

            <SidebarSection titolo="Aule">
              <SidebarLink :to="{ name: 'SediAule' }" icon="it-map-marker" label="Sedi &amp; Aule" />
            </SidebarSection>
          </template>

          <template v-if="authStore.isCoordinamento">
            <SidebarSection titolo="Coordinamento">
              <SidebarLink :to="{ name: 'DashboardCoordinamento' }" icon="it-chart-line" label="Dashboard" />
              <SidebarLink :to="{ name: 'SituazioneOggi' }" icon="it-pa" label="Situazione Oggi" />
              <SidebarLink :to="{ name: 'Grafici' }" icon="it-presentation" label="Grafici &amp; Report" />
              <SidebarLink :to="{ name: 'Conflitti' }" icon="it-error" label="Conflitti" />
            </SidebarSection>

            <SidebarSection titolo="Amministrazione">
              <SidebarLink :to="{ name: 'GestioneUtenti' }" icon="it-user" label="Utenti" />
              <SidebarLink :to="{ name: 'GestioneSediAule' }" icon="it-settings" label="Gestione Sedi/Aule" />
            </SidebarSection>
          </template>
        </ul>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { labelRuolo } from '@/utils/formatters'
import SidebarSection from '@/components/layout/SidebarSection.vue'
import SidebarLink from '@/components/layout/SidebarLink.vue'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const authStore = useAuthStore()
const router = useRouter()

const homePath = computed(() =>
  authStore.ruolo === 'COORDINAMENTO'
    ? { name: 'DashboardCoordinamento' }
    : { name: 'DashboardOperativo' }
)

function handleLogout() {
  authStore.logout()
  router.push({ name: 'Login' })
}
</script>