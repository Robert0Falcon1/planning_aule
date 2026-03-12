<template>
  <li class="nav-item mb-1">
    <router-link
      class="nav-link d-flex align-items-center gap-2"
      active-class="active fw-semibold"
      :to="to"
    >
      <svg class="icon icon-sm">
        <use :href="sprites + '#' + icon"></use>
      </svg>
      {{ label }}
    </router-link>
  </li>
</template>

<script setup>
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'

defineProps({
  to:    { type: [String, Object], required: true },
  icon:  { type: String, required: true },
  label: { type: String, required: true },
})
</script>