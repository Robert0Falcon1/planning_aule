<template>
  <div class="app-wrapper" :class="{ 'sidebar-collapsed': sidebarCollapsed }">
    <AppSidebar :collapsed="sidebarCollapsed" @toggle="sidebarCollapsed = !sidebarCollapsed" />
    <div class="app-main">
      <AppHeader @toggle-sidebar="sidebarCollapsed = !sidebarCollapsed" />
      <main class="app-content">
        <RouterView v-slot="{ Component }">
          <Transition name="fade" mode="out-in">
            <component :is="Component" />
          </Transition>
        </RouterView>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppSidebar from './AppSidebar.vue'
import AppHeader  from './AppHeader.vue'

const sidebarCollapsed = ref(false)
</script>

<style scoped>
.app-wrapper {
  display: flex;
  min-height: 100vh;
  background: #f5f6fa;
}
.app-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  margin-left: 260px;
  transition: margin-left .25s ease;
}
.sidebar-collapsed .app-main {
  margin-left: 64px;
}
.app-content {
  flex: 1;
  padding: 1.5rem;
}
.fade-enter-active,
.fade-leave-active { transition: opacity .15s ease; }
.fade-enter-from,
.fade-leave-to     { opacity: 0; }

@media (max-width: 991px) {
  .app-main { margin-left: 0 !important; }
}
</style>
