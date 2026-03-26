<template>
  <div class="card border-0 shadow-sm kpi-card">
    <div class="card-body">
      <div class="kpi-value" :class="`text-${color}`">{{ value }}</div>
      <div class="kpi-label">
        <slot name="label">{{ label }}</slot>
      </div>
      <slot name="extra" />
    </div>
  </div>
</template>

<script setup>
defineProps({
  value: { type: [String, Number], required: true },
  label: { type: String, default: '' },
  icon:  { type: String, default: 'it-info-circle' },
  color: { type: String, default: 'primary' },
})
</script>

<style scoped>
.kpi-card {
  border-radius: 12px;
}
.kpi-value {
  font-size: 2rem;
  font-weight: 800;
  line-height: 1;
}
.kpi-label {
  font-size: .8rem;
  color: #666;
  margin-top: .25rem;
  font-weight: 400;
}
</style>