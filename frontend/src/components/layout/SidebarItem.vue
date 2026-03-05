<template>
  <li>
    <RouterLink :to="to" class="sidebar-link" :class="{ 'sidebar-link--collapsed': collapsed }" :title="collapsed ? label : undefined">
      <svg class="icon icon-white icon-sm flex-shrink-0">
        <use :href="sprites + '#${icon}'"></use>
      </svg>
      <span v-if="!collapsed" class="sidebar-link__label">{{ label }}</span>
    </RouterLink>
  </li>
</template>

<script setup>
import sprites from 'bootstrap-italia/dist/svg/sprites.svg?url'
defineProps({
  to:        { type: [String, Object], required: true },
  icon:      { type: String, required: true },
  label:     { type: String, required: true },
  collapsed: { type: Boolean, default: false },
})
</script>

<style scoped>
.sidebar-link {
  display: flex;
  align-items: center;
  gap: .75rem;
  padding: .6rem 1rem;
  color: rgba(255,255,255,.85);
  text-decoration: none;
  transition: background .15s, color .15s;
  border-radius: 0;
  white-space: nowrap;
}
.sidebar-link:hover {
  background: rgba(255,255,255,.12);
  color: white;
}
.sidebar-link.router-link-active {
  background: rgba(255,255,255,.18);
  color: white;
  font-weight: 600;
  border-left: 3px solid white;
}
.sidebar-link--collapsed {
  justify-content: center;
  padding: .6rem;
}
.sidebar-link__label {
  font-size: .9rem;
  overflow: hidden;
}
</style>
