<template>
  <!--
    Alert globale: reagisce allo store UI.
    Si posiziona in cima al contenuto principale e scompare automaticamente.
  -->
  <transition name="fade">
    <div
      v-if="uiStore.alert"
      class="alert d-flex align-items-center mb-4"
      :class="`alert-${uiStore.alert.type}`"
      role="alert"
    >
      <!-- Icona contestuale -->
      <svg class="icon me-2" :class="iconClass">
        <use :href="iconHref"></use>
      </svg>

      <span class="flex-grow-1">{{ uiStore.alert.message }}</span>

      <!-- Chiusura manuale -->
      <button type="button" class="btn-close ms-3" @click="uiStore.chiudiAlert" />
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'
import { useUiStore } from '@/stores/ui'

const uiStore = useUiStore()

/** Icona Bootstrap Italia in base al tipo di alert */
const iconHref = computed(() => {
  const map = {
    success: '#it-check-circle',
    danger:  '#it-error',
    warning: '#it-warning-circle',
    info:    '#it-info-circle',
  }
  return map[uiStore.alert?.type] ?? '#it-info-circle'
})

const iconClass = computed(() => {
  const map = {
    success: 'icon-success',
    danger:  'icon-danger',
    warning: 'icon-warning',
    info:    'icon-info',
  }
  return map[uiStore.alert?.type] ?? ''
})
</script>

<style scoped>
/* Transizione morbida sull'alert */
.fade-enter-active,
.fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from,
.fade-leave-to     { opacity: 0; }
</style>
