<template>
  <!--
    Sidebar di navigazione.
    Le voci del menu si adattano automaticamente al ruolo dell'utente.
  -->
  <nav class="sidebar-nav border-end bg-white h-100 py-4" aria-label="Menu laterale">
    <ul class="nav flex-column px-2">
      <!-- Dashboard -->
      <li class="nav-item mb-1">
        <router-link class="nav-link d-flex align-items-center gap-2" :to="{ name: 'Dashboard' }">
          <svg class="icon icon-sm"><use href="#it-dashboard"></use></svg>
          Dashboard
        </router-link>
      </li>

      <hr class="my-2" />

      <!-- ── RESPONSABILE CORSO ─────────────────────────────────────────── -->
      <template v-if="authStore.isResponsabileCorso">
        <SidebarSection titolo="Prenotazioni">
          <SidebarLink :to="{ name: 'NuovaPrenotazione' }"    icon="it-calendar" label="Nuova Prenotazione" />
          <SidebarLink :to="{ name: 'PrenotazioneMassiva' }"  icon="it-refresh"  label="Prenotazione Massiva" />
          <SidebarLink :to="{ name: 'MiePrenotazioni' }"      icon="it-list"     label="Le Mie Prenotazioni" />
          <SidebarLink :to="{ name: 'SlotLiberi' }"           icon="it-search"   label="Slot Disponibili" />
        </SidebarSection>
      </template>

      <!-- ── SEGRETERIA DI SEDE ────────────────────────────────────────── -->
      <template v-if="authStore.isSegreteriaSede">
        <SidebarSection titolo="Gestione Richieste">
          <SidebarLink :to="{ name: 'RichiestePendenti' }"   icon="it-check"      label="Richieste Pendenti" />
          <SidebarLink :to="{ name: 'GestioneConflitti' }"   icon="it-warning-circle" label="Conflitti" />
          <SidebarLink :to="{ name: 'CalendarioSede' }"      icon="it-calendar"   label="Calendario Sede" />
          <SidebarLink :to="{ name: 'PrenotazioniSede' }"    icon="it-list"       label="Tutte le Prenotazioni" />
        </SidebarSection>
      </template>

      <!-- ── RESPONSABILE DI SEDE ──────────────────────────────────────── -->
      <template v-if="authStore.isResponsabileSede">
        <SidebarSection titolo="La Mia Sede">
          <SidebarLink :to="{ name: 'PrenotazioniSede' }"   icon="it-list"      label="Prenotazioni Sede" />
          <SidebarLink :to="{ name: 'SaturazioneSpazi' }"   icon="it-chart-line" label="Saturazione Spazi" />
        </SidebarSection>
      </template>

      <!-- ── SEGRETERIA DIDATTICA ──────────────────────────────────────── -->
      <template v-if="authStore.isSegreteriaDidattica">
        <SidebarSection titolo="Corsi">
          <SidebarLink :to="{ name: 'PrenotazioniCorso' }"  icon="it-list"     label="Prenotazioni per Corso" />
        </SidebarSection>
      </template>

      <!-- ── COORDINAMENTO ────────────────────────────────────────────── -->
      <template v-if="authStore.isCoordinamento">
        <SidebarSection titolo="Vista Globale">
          <SidebarLink :to="{ name: 'VistaGlobale' }"       icon="it-map-marker"  label="Vista Globale" />
          <SidebarLink :to="{ name: 'Report' }"             icon="it-chart-line"  label="Report Saturazione" />
          <SidebarLink :to="{ name: 'GestioneUtenti' }"     icon="it-user"        label="Gestione Utenti" />
        </SidebarSection>
      </template>
    </ul>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

// Sotto-componenti inline definiti qui per semplicità
import SidebarSection from '@/components/layout/SidebarSection.vue'
import SidebarLink    from '@/components/layout/SidebarLink.vue'

const authStore = useAuthStore()
</script>

<style scoped>
/* Personalizza qui l'altezza/colori della sidebar senza toccare Bootstrap Italia */
.sidebar-nav {
  min-height: calc(100vh - 120px);
}
</style>
