<template>
  <!--
    Header Bootstrap Italia con:
    - Slim header (nome ente)
    - Navbar principale con nome app e menu utente
  -->

  <!-- Slim header: nome ente e link rapidi -->
  <div class="it-header-slim-wrapper">
    <div class="container-fluid">
      <div class="it-header-slim-wrapper-content">
        <span class="navbar-brand">
          <strong>InforCoopEcipa Piemonte</strong>
        </span>
        <div class="header-slim-right-zone">
          <!-- Ruolo utente corrente -->
          <span class="badge bg-primary me-3">
            {{ labelRuolo(authStore.ruolo) }}
          </span>
          <!-- Pulsante logout -->
          <button class="btn btn-sm btn-outline-light" @click="handleLogout">
            <svg class="icon icon-sm icon-light me-1">
              <use href="#it-logout"></use>
            </svg>
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
        <div class="col-12 d-flex">
          <nav class="navbar navbar-expand-lg" aria-label="Navigazione principale">
            <!-- Logo / nome applicazione -->
            <router-link class="navbar-brand" :to="{ name: 'Dashboard' }">
              <span class="fw-bold">🏫 ICE Planning Aule</span>
            </router-link>

            <!-- Toggle mobile -->
            <button
              class="navbar-toggler"
              type="button"
              data-bs-toggle="collapse"
              data-bs-target="#navbarPrincipal"
              aria-controls="navbarPrincipal"
              aria-expanded="false"
            >
              <svg class="icon">
                <use href="#it-burger"></use>
              </svg>
            </button>

            <div class="collapse navbar-collapse" id="navbarPrincipal">
              <!-- Mostra il nome dell'utente nella navbar -->
              <ul class="navbar-nav ms-auto">
                <li class="nav-item">
                  <span class="nav-link text-white">
                    <svg class="icon icon-sm icon-light me-1">
                      <use href="#it-user"></use>
                    </svg>
                    {{ authStore.nomeCompleto }}
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
import { useAuthStore }  from '@/stores/auth'
import { useRouter }     from 'vue-router'
import { labelRuolo }    from '@/utils/formatters'

const authStore = useAuthStore()
const router    = useRouter()

function handleLogout() {
  authStore.logout()
  router.push({ name: 'Login' })
}
</script>
