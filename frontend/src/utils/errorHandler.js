/**
 * Formatta gli errori API in messaggi leggibili per l'utente
 */
export function formatErrorMessage(error) {
  // Errore di rete (server offline, CORS, timeout)
  if (!error.response && error instanceof TypeError) {
    if (error.message === 'Failed to fetch' || error.message.includes('fetch')) {
      return 'Impossibile contattare il server. Verifica la connessione.'
    }
    if (error.message.includes('timeout')) {
      return 'Richiesta scaduta. Riprova.'
    }
    return 'Errore di connessione al server.'
  }

  // Se è già un messaggio formattato, ritorna così com'è
  if (typeof error === 'string') return error

  // Estrai status e data dalla risposta
  const status = error.status
  const data = error.data

  if (!status) return error.message || 'Errore sconosciuto'

  // 422 - Errori di validazione (Pydantic)
  if (status === 422) {
    if (Array.isArray(data?.detail)) {
      // FastAPI validation errors: [{loc, msg, type}]
      const errors = data.detail
        .map(err => {
          const field = err.loc?.slice(-1)[0] || 'campo'
          return `${field}: ${err.msg}`
        })
        .join('; ')
      return `Dati non validi: ${errors}`
    }
    if (typeof data?.detail === 'string') return data.detail
    return 'Dati di input non validi.'
  }

  // 401 - Non autenticato
  if (status === 401) {
    return 'Sessione scaduta. Effettua nuovamente il login.'
  }

  // 403 - Non autorizzato
  if (status === 403) {
    return 'Non hai i permessi per questa operazione.'
  }

  // 404 - Non trovato
  if (status === 404) {
    return data?.detail || 'Risorsa non trovata.'
  }

  // 409 - Conflitto
  if (status === 409) {
    return data?.detail || 'Conflitto: la risorsa esiste già.'
  }

  // 500+ - Errore server
  if (status >= 500) {
    return 'Errore del server. Riprova più tardi.'
  }

  // Fallback: usa detail dal backend o messaggio generico
  return data?.detail || data?.message || `Errore ${status}: operazione non riuscita.`
}