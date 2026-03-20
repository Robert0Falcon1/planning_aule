<template>
  <nav class="sidebar-nav bg-white h-100 py-4" :class="{ 'border-end': !isMobile }" aria-label="Menu laterale">
    <ul class="nav flex-column pe-4">
      <template v-if="authStore.isOperativo || authStore.isCoordinamento">
        <SidebarSection titolo="Prenotazioni">
          <SidebarLink :to="{ name: 'NuovaPrenotazione' }" icon="it-plus-circle" label="Nuova" />
          <SidebarLink :to="{ name: 'MiePrenotazioni' }"   icon="it-list"        :label="authStore.isCoordinamento ? 'Riepilogo' : 'Le Mie Prenotazioni'" />
          <SidebarLink :to="{ name: 'Calendario' }"        icon="it-calendar"    label="Calendario" />
        </SidebarSection>

        <SidebarSection titolo="Aule">
          <SidebarLink :to="{ name: 'SediAule' }" icon="it-map-marker" label="Sedi &amp; Aule" />
        </SidebarSection>
      </template>

      <template v-if="authStore.isCoordinamento">
        <SidebarSection titolo="Coordinamento">
          <SidebarLink :to="{ name: 'DashboardCoordinamento' }" icon="it-chart-line"   label="Dashboard" />
          <SidebarLink :to="{ name: 'SituazioneOggi' }"        icon="it-pa"           label="Situazione Oggi" />
          <SidebarLink :to="{ name: 'Conflitti' }"             icon="it-error"        label="Conflitti" />
          <SidebarLink :to="{ name: 'Grafici' }"               icon="it-presentation" label="Grafici &amp; Report" />
        </SidebarSection>

        <SidebarSection titolo="Amministrazione">
          <SidebarLink :to="{ name: 'GestioneUtenti' }"   icon="it-user"     label="Utenti" />
          <SidebarLink :to="{ name: 'GestioneSediAule' }" icon="it-settings" label="Gestione Sedi/Aule" />
        </SidebarSection>
      </template>
    </ul>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import SidebarSection from '@/components/layout/SidebarSection.vue'
import SidebarLink from '@/components/layout/SidebarLink.vue'

const authStore = useAuthStore()

const isMobile = computed(() => window.innerWidth < 768)
</script>

<style scoped>
.sidebar-nav { 
  min-height: 100%; 
}

/* Rimuovi border su mobile (già gestito con :class) */
@media (max-width: 767px) {
  .sidebar-nav {
    border-right: none !important;
  }
}
</style>