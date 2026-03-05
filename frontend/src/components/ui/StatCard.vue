<template>
  <div class="card border-0 shadow-sm h-100">
    <div class="card-body d-flex align-items-center gap-3">
      <div class="stat-icon rounded-3 p-3" :class="`bg-${color}-subtle`">
        <svg class="icon" :class="`icon-${color}`">
          <use :href="sprites + '#${icon}'"></use>
        </svg>
      </div>
      <div>
        <div class="stat-value">{{ value }}</div>
        <div class="stat-label text-muted">{{ label }}</div>
        <slot name="extra" />
      </div>
    </div>
  </div>
</template>

<script setup>
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
defineProps({
  value: { type: [String, Number], required: true },
  label: { type: String, required: true },
  icon:  { type: String, default: 'it-info-circle' },
  color: { type: String, default: 'primary' },
})
</script>

<style scoped>
.stat-value { font-size: 1.6rem; font-weight: 700; line-height: 1.1; }
.stat-label { font-size: .8rem; }
.stat-icon  { display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
</style>
