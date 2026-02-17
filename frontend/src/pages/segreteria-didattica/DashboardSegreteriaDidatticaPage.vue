<template>
  <div>
    <h2 class="h4 fw-bold mb-4">👋 Dashboard — Segreteria Didattica</h2>

    <div class="alert alert-info mb-4">
      Monitora le prenotazioni associate ai corsi di tua competenza.
    </div>

    <div class="d-flex flex-wrap gap-2">
      <router-link :to="{ name: 'PrenotazioniCorso' }" class="btn btn-primary">
        📋 Prenotazioni per Corso
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
const authStore = useAuthStore()
</script>
