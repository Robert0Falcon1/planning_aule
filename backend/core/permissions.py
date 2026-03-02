"""
Sistema RBAC (Role-Based Access Control).
Definisce quali azioni ogni ruolo può eseguire nel sistema.

Due gruppi funzionali:
  OPERATIVO    → RC / Segreteria Didattica / Segreteria di Sede
                 (prenotano, modificano, confermano/disdiscono)
  SUPERVISIONE → Responsabile Sede / Coordinamento
                 (visualizzano, report, saturazione)
"""

from backend.models.enums import RuoloUtente

# ── Gruppi funzionali ─────────────────────────────────────────────────────────

GRUPPO_OPERATIVO = [
    RuoloUtente.RESPONSABILE_CORSO,
    RuoloUtente.SEGRETERIA_DIDATTICA,
    RuoloUtente.SEGRETERIA_SEDE,
]

GRUPPO_SUPERVISIONE = [
    RuoloUtente.RESPONSABILE_SEDE,
    RuoloUtente.COORDINAMENTO,
]

TUTTI = GRUPPO_OPERATIVO + GRUPPO_SUPERVISIONE

# ── Matrice dei permessi ──────────────────────────────────────────────────────

PERMESSI: dict[str, list[RuoloUtente]] = {

    # ── Prenotazioni (operativo) ──────────────────────────────────────────────
    "prenotazione:richiedere":    GRUPPO_OPERATIVO,
    "prenotazione:confermare":    GRUPPO_OPERATIVO,
    "prenotazione:modificare":    GRUPPO_OPERATIVO,
    "prenotazione:annullare":     GRUPPO_OPERATIVO,
    "prenotazione:rifiutare":     GRUPPO_OPERATIVO,

    # ── Visualizzazione prenotazioni (tutti) ──────────────────────────────────
    "prenotazione:vedere_proprie": GRUPPO_OPERATIVO,
    "prenotazione:vedere_sede":    TUTTI,
    "prenotazione:vedere_tutte":   [RuoloUtente.COORDINAMENTO],

    # ── Aule e slot ───────────────────────────────────────────────────────────
    "aula:vedere_slot_liberi":    TUTTI,
    "aula:gestire":               [RuoloUtente.COORDINAMENTO],

    # ── Corsi ─────────────────────────────────────────────────────────────────
    "corso:creare":               [RuoloUtente.SEGRETERIA_DIDATTICA,
                                   RuoloUtente.COORDINAMENTO],
    "corso:vedere_propri":        GRUPPO_OPERATIVO,
    "corso:vedere_tutti":         TUTTI,

    # ── Report e analytics (supervisione + operativo) ─────────────────────────
    "report:sede":                TUTTI,
    "report:saturazione":         TUTTI,
    "report:export_csv":          TUTTI,
    "report:globale":             [RuoloUtente.COORDINAMENTO],

    # ── Gestione utenti (solo coordinamento) ──────────────────────────────────
    "utente:creare":              [RuoloUtente.COORDINAMENTO],
    "utente:vedere_tutti":        [RuoloUtente.COORDINAMENTO],

    # ── Attrezzature ──────────────────────────────────────────────────────────
    "attrezzatura:richiedere":    GRUPPO_OPERATIVO,
    "attrezzatura:gestire":       [RuoloUtente.COORDINAMENTO],
}


def ha_permesso(ruolo: RuoloUtente, azione: str) -> bool:
    """
    Verifica se un ruolo è autorizzato a eseguire un'azione.
    """
    ruoli_autorizzati = PERMESSI.get(azione, [])
    return ruolo in ruoli_autorizzati