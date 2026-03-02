<template>
  <!--
    Dashboard Operativa
    Per: Responsabile Corso, Segreteria Didattica, Segreteria di Sede
    Azioni: prenotare, modificare, confermare, disdire, visualizzare
  -->
  <div class="container-fluid px-4 py-4">
    <div class="row mb-4">
      <div class="col">
        <h2 class="fw-bold">Area Operativa</h2>
        <p class="text-muted">
          Gestisci le prenotazioni delle aule e monitora la situazione della sede.
        </p>
      </div>
    </div>

    <!-- Azioni operative -->
    <div class="row g-4 mb-4">
      <div class="col-lg-3 col-md-6" v-for="card in azioniOperative" :key="card.to">
        <div class="card shadow-sm h-100 card-teaser">
          <div class="card-body">
            <div class="d-flex align-items-center mb-3">
              <svg class="icon icon-primary me-2"><use :href="card.icon"></use></svg>
              <h5 class="card-title mb-0">{{ card.titolo }}</h5>
            </div>
            <p class="card-text text-muted">{{ card.descrizione }}</p>
            <router-link :to="card.to" class="btn btn-primary btn-sm">
              {{ card.azione }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Visualizzazione e report -->
    <div class="row mb-3">
      <div class="col">
        <h4 class="fw-semibold">Situazione sede</h4>
      </div>
    </div>
    <div class="row g-4">
      <div class="col-lg-3 col-md-6" v-for="card in sezioneVisualizzazione" :key="card.to">
        <div class="card shadow-sm h-100 card-teaser">
          <div class="card-body">
            <div class="d-flex align-items-center mb-3">
              <svg class="icon icon-secondary me-2"><use :href="card.icon"></use></svg>
              <h5 class="card-title mb-0">{{ card.titolo }}</h5>
            </div>
            <p class="card-text text-muted">{{ card.descrizione }}</p>
            <router-link :to="card.to" class="btn btn-outline-primary btn-sm">
              {{ card.azione }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Card operative — azioni di prenotazione e gestione
 */
const azioniOperative = [
  {
    titolo: 'Nuova prenotazione',
    descrizione: 'Prenota un\'aula per una lezione o un evento.',
    to: '/prenotazioni/nuova',
    icon: '#it-plus-circle',
    azione: 'Prenota',
  },
  {
    titolo: 'Prenotazione massiva',
    descrizione: 'Prenota più date ricorrenti in un colpo solo.',
    to: '/prenotazioni/massiva',
    icon: '#it-calendar',
    azione: 'Configura',
  },
  {
    titolo: 'Le mie prenotazioni',
    descrizione: 'Visualizza, modifica o annulla le tue prenotazioni.',
    to: '/prenotazioni/mie',
    icon: '#it-list',
    azione: 'Gestisci',
  },
  {
    titolo: 'Conflitti',
    descrizione: 'Verifica e risolvi eventuali sovrapposizioni.',
    to: '/prenotazioni/conflitti',
    icon: '#it-warning-circle',
    azione: 'Controlla',
  },
]

/**
 * Card di visualizzazione — accessibili anche alla supervisione
 */
const sezioneVisualizzazione = [
  {
    titolo: 'Slot liberi',
    descrizione: 'Consulta la disponibilità delle aule per sede.',
    to: '/aule/slot-liberi',
    icon: '#it-search',
    azione: 'Cerca',
  },
  {
    titolo: 'Prenotazioni sede',
    descrizione: 'Panoramica delle prenotazioni della tua sede.',
    to: '/sede/prenotazioni',
    icon: '#it-map-marker-circle',
    azione: 'Visualizza',
  },
  {
    titolo: 'Saturazione',
    descrizione: 'Dati sull\'occupazione e capienza delle aule.',
    to: '/sede/saturazione',
    icon: '#it-chart-line',
    azione: 'Analizza',
  },
  {
    titolo: 'Report',
    descrizione: 'Report complessivo con export CSV.',
    to: '/report',
    icon: '#it-file',
    azione: 'Genera',
  },
]
</script>