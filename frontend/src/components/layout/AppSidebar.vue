<template>
  <nav class="sidebar-nav border-end bg-white h-100 py-4" aria-label="Menu laterale">
    <ul class="nav flex-column px-2">

      <!-- ── OPERATIVO ──────────────────────────────────────────────────── -->
      <template v-if="authStore.isOperativo || authStore.isCoordinamento">
        <SidebarSection titolo="Prenotazioni">
          <SidebarLink :to="{ name: 'NuovaPrenotazione' }" icon="it-plus-circle" label="Nuova Prenotazione" />
          <SidebarLink :to="{ name: 'MiePrenotazioni' }"   icon="it-list"        :label="authStore.isCoordinamento ? 'Riepilogo Prenotazioni' : 'Le Mie Prenotazioni'" />
          <SidebarLink :to="{ name: 'Calendario' }"        icon="it-calendar"    label="Calendario" />
        </SidebarSection>

        <SidebarSection titolo="Aule">
          <SidebarLink :to="{ name: 'SediAule' }" icon="it-map-marker" label="Sedi &amp; Aule" />
        </SidebarSection>
      </template>

      <!-- ── COORDINAMENTO ─────────────────────────────────────────────── -->
      <template v-if="authStore.isCoordinamento">
        <SidebarSection titolo="Coordinamento">
          <SidebarLink :to="{ name: 'DashboardCoordinamento' }" icon="it-chart-line"   label="Dashboard" />
          <SidebarLink :to="{ name: 'SituazioneOggi' }"        icon="it-pa"           label="Situazione Oggi" />
          <SidebarLink :to="{ name: 'Grafici' }"               icon="it-presentation" label="Grafici &amp; Report" />
          <SidebarLink :to="{ name: 'Conflitti' }"             icon="it-error"        label="Conflitti" />
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
import { useAuthStore }  from '@/stores/auth'
import SidebarSection    from '@/components/layout/SidebarSection.vue'
import SidebarLink       from '@/components/layout/SidebarLink.vue'

const authStore = useAuthStore()
</script>

<style scoped>
.sidebar-nav { min-height: calc(100vh - 120px); }
</style>