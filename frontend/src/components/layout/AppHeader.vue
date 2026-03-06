<template>
  <!-- Slim header: nome ente -->
  <div class="it-header-slim-wrapper">
    <div class="container-fluid">
      <div class="it-header-slim-wrapper-content">
        <span class="navbar-brand">
          <!-- <strong>InforCoopEcipa Piemonte</strong> -->
           <img class="logo filter-logo" src="/img/logo_ICE.png">
        </span>
        <div class="header-slim-right-zone">
          <span class="badge bg-primary me-3">
            {{ labelRuolo(authStore.ruolo) }}
          </span>
          <button class="btn btn-sm btn-outline-light" @click="handleLogout">
            <svg class="icon icon-sm icon-light me-1"><use :href="sprites + '#it-logout'"></use></svg>
            Esci
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Navbar principale -->
  <div class="it-header-navbar-wrapper theme-dark-desk theme-dark-mobile">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12 d-flex px-4 mx-2">
          <nav class="navbar navbar-expand-lg" aria-label="Navigazione principale">
            <router-link class="navbar-brand" :to="homePath">
              <span class="fw-bold text-white hover-link">Planning Aule</span>
            </router-link>

            <button class="navbar-toggler" type="button"
              data-bs-toggle="collapse" data-bs-target="#navbarPrincipal"
              aria-controls="navbarPrincipal" aria-expanded="false">
              <svg class="icon"><use :href="sprites + '#it-burger'"></use></svg>
            </button>

            <div class="collapse navbar-collapse" id="navbarPrincipal">
              <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                  <span class="nav-link text-white">
                    <svg class="icon icon-sm icon-light me-1"><use :href="sprites + '#it-user'"></use></svg>
                    {{ authStore.nomeUtente }}
                  </span>
                </li>
              </ul>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter }    from 'vue-router'
import { labelRuolo }   from '@/utils/formatters'
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

const authStore = useAuthStore()
const router    = useRouter()

// Redirect alla dashboard corretta in base al ruolo
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