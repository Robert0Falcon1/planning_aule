<template>
  <!-- Singola voce del menu laterale con active state automatico da Vue Router -->
  <li class="nav-item mb-1">
    <router-link
      class="nav-link d-flex align-items-center gap-2"
      active-class="active fw-semibold"
      :to="to"
    >
      <svg class="icon icon-sm">
        <use :href="`#${icon}`"></use>
      </svg>
      {{ label }}
    </router-link>
  </li>
</template>

<script setup>
defineProps({
  /** Oggetto rotta Vue Router ({ name: '...' } o stringa path) */
  to:    { type: [String, Object], required: true },
  /** ID dell'icona Bootstrap Italia (es: "it-calendar") */
  icon:  { type: String, required: true },
  /** Testo della voce di menu */
  label: { type: String, required: true },
})
</script>
