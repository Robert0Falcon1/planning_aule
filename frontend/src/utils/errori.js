// ─────────────────────────────────────────────────────────────────────────────
// Utility — Parsing errori API
//
// Il client fetch lancia sempre `new Error(msg)` dove msg è già la stringa
// estratta da `detail` (stringa o array Pydantic 422).
// Questa utility gestisce anche i casi in cui il chiamante riceva un errore
// grezzo di rete o un oggetto non standard.
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Estrae un messaggio leggibile da un errore lanciato dal client fetch.
 *
 * Casi gestiti:
 *   1. Error standard con .message  → usa il messaggio direttamente
 *   2. Oggetto con .detail stringa  → (errori FastAPI non ancora parsati)
 *   3. Oggetto con .detail array    → errori validazione Pydantic 422
 *   4. Tutto il resto               → fallback
 *
 * @param {unknown} err       Errore catturato nel catch
 * @param {string}  fallback  Messaggio di default
 * @returns {string}
 */
export function estraiErrore(err, fallback = 'Si è verificato un errore. Riprova.') {
  if (!err) return fallback

  // Caso 1: Error standard — il client fetch imposta già err.message = detail
  if (err instanceof Error) return err.message || fallback

  // Caso 2 e 3: oggetto grezzo con .detail (es. chiamate fuori dal client)
  const detail = err?.detail
  if (!detail) return fallback

  if (typeof detail === 'string') return detail

  if (Array.isArray(detail)) {
    return detail
      .map(e => {
        const campo = e.loc?.slice(1).join(' → ') ?? ''
        const msg   = e.msg ?? ''
        return campo ? `${campo}: ${msg}` : msg
      })
      .join(' | ')
  }

  try { return JSON.stringify(detail) } catch { return fallback }
}

/**
 * Restituisce true se l'errore è un 401 (sessione scaduta / non autenticato).
 * Utile per mostrare un messaggio specifico o fare redirect al login.
 *
 * Il client fetch include il codice HTTP nel messaggio con formato "Errore 401".
 *
 * @param {unknown} err
 * @returns {boolean}
 */
export function isUnauthorized(err) {
  if (err instanceof Error) return err.message.includes('401')
  return false
}

/**
 * Restituisce true se l'errore è un 403 (permessi insufficienti).
 * @param {unknown} err
 * @returns {boolean}
 */
export function isForbidden(err) {
  if (err instanceof Error) return err.message.includes('403')
  return false
}

/**
 * Restituisce true se l'errore è un 409 (conflitto, es. aula già prenotata).
 * @param {unknown} err
 * @returns {boolean}
 */
export function isConflitto(err) {
  if (err instanceof Error) return err.message.includes('409')
  return false
}