<template>
  <div class="d-flex flex-column align-items-center justify-content-center py-5 text-center">
    <div class="display-1 text-muted mb-3">404</div>
    <h2 class="h4 fw-bold mb-2">Pagina non trovata</h2>
    <p class="text-muted mb-4">La pagina che cerchi non esiste o non hai i permessi per vederla.</p>
    <router-link :to="{ name: 'Dashboard' }" class="btn btn-primary">
      ← Torna alla Dashboard
    </router-link>
  </div>
</template>
