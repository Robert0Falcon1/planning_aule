<template>
  <!-- Raggruppamento di voci nel menu laterale con titolo separatore -->
  <li class="nav-item">
    <p class="nav-link text-muted small text-uppercase fw-semibold mb-1 mt-2">
      {{ titolo }}
    </p>
  </li>
  <slot />
</template>

<script setup>
defineProps({
  /** Titolo della sezione (es: "Prenotazioni", "Gestione Richieste") */
  titolo: { type: String, required: true },
})
</script>
