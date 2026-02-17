// ─────────────────────────────────────────────────────────────────────────────
// Utility — Parsing errori FastAPI
// FastAPI può restituire detail come:
//   • stringa:  { "detail": "Email già registrata" }
//   • array:    { "detail": [{ "loc": [...], "msg": "...", "type": "..." }] }  (422 Unprocessable Entity)
// ─────────────────────────────────────────────────────────────────────────────

/**
 * Estrae un messaggio leggibile dall'errore Axios.
 * @param {unknown} err  Errore catturato nel catch
 * @param {string}  fallback  Messaggio di default se non si riesce a parsare
 * @returns {string}
 */
export function estraiErrore(err, fallback = 'Si è verificato un errore. Riprova.') {
  const detail = err?.response?.data?.detail

  if (!detail) return fallback

  // Caso 1: detail è una stringa semplice
  if (typeof detail === 'string') return detail

  // Caso 2: detail è l'array di errori di validazione Pydantic (422)
  if (Array.isArray(detail)) {
    return detail
      .map(e => {
        const campo = e.loc?.slice(1).join(' → ') ?? ''  // ignora 'body'
        const msg   = e.msg ?? ''
        return campo ? `${campo}: ${msg}` : msg
      })
      .join(' | ')
  }

  // Caso 3: detail è un oggetto generico — serializza
  try { return JSON.stringify(detail) } catch { return fallback }
}
