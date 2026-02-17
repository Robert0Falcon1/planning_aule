<template>
  <!--
    Badge colorato per lo stato di una prenotazione.
    Usa la configurazione da constants.js per colore e icona.

    Uso:
      <BadgeStato stato="confermata" />
  -->
  <span class="badge" :class="badge.class">
    {{ badge.icon }} {{ badge.label }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { badgeStato } from '@/utils/formatters'

const props = defineProps({
  stato: { type: String, required: true },
})

const badge = computed(() => badgeStato(props.stato))
</script>
