<template>
  <!--
    Card di metrica numerica per le dashboard.
    Mostra un valore aggregato con etichetta e colore contestuale.

    Uso:
      <StatCard titolo="In Attesa" :valore="45" colore="warning" icon="it-clock" />
  -->
  <div class="card border-0 shadow-sm h-100">
    <div class="card-body d-flex align-items-center gap-3">
      <!-- Icona colorata -->
      <div
        class="rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
        :class="`bg-${colore} bg-opacity-10`"
        style="width: 56px; height: 56px;"
      >
        <svg class="icon" :class="`icon-${colore}`" style="width:28px;height:28px;">
          <use :href="`#${icon}`"></use>
        </svg>
      </div>

      <!-- Testo -->
      <div>
        <div class="h3 mb-0 fw-bold">{{ valore }}</div>
        <div class="small text-muted">{{ titolo }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  /** Etichetta della metrica */
  titolo:  { type: String, required: true },
  /** Valore numerico da mostrare */
  valore:  { type: [Number, String], default: 0 },
  /** Classe colore Bootstrap (primary, success, warning, danger, secondary) */
  colore:  { type: String, default: 'primary' },
  /** ID icona Bootstrap Italia (es: "it-calendar") */
  icon:    { type: String, default: 'it-list' },
})
</script>
