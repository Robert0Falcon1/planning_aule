// ─────────────────────────────────────────────────────────────────────────────
// Store — UI (Pinia)
// Gestisce lo stato dell'interfaccia: alert globali, spinner di caricamento.
// ─────────────────────────────────────────────────────────────────────────────

import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUiStore = defineStore('ui', () => {
  // ── Alert globale ─────────────────────────────────────────────────────────
  /** @type {Ref<{ type: 'success'|'danger'|'warning'|'info', message: string }|null>} */
  const alert = ref(null)

  /** Timer per auto-dismiss dell'alert */
  let alertTimer = null

  /**
   * Mostra un alert globale con auto-dismiss dopo `durata` ms.
   * @param {'success'|'danger'|'warning'|'info'} type
   * @param {string} message
   * @param {number} durata  millisecondi prima della scomparsa automatica
   */
  function mostraAlert(type, message, durata = 4000) {
    if (alertTimer) clearTimeout(alertTimer)
    alert.value = { type, message }
    alertTimer = setTimeout(() => { alert.value = null }, durata)
  }

  /** Scorciatoie semantiche */
  const successo = (msg)  => mostraAlert('success', msg)
  const errore   = (msg)  => mostraAlert('danger',  msg)
  const avviso   = (msg)  => mostraAlert('warning', msg)
  const info     = (msg)  => mostraAlert('info',    msg)

  function chiudiAlert() {
    if (alertTimer) clearTimeout(alertTimer)
    alert.value = null
  }

  // ── Spinner di caricamento globale ────────────────────────────────────────
  const loading = ref(false)

  function iniziaCaricamento()  { loading.value = true  }
  function fineCaricamento()    { loading.value = false }

  return {
    alert,
    mostraAlert,
    successo,
    errore,
    avviso,
    info,
    chiudiAlert,
    loading,
    iniziaCaricamento,
    fineCaricamento,
  }
})
