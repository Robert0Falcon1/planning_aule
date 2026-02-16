"""
Esporta tutti i modelli ORM per facilitarne l'importazione.
L'ordine di importazione rispetta le dipendenze tra le tabelle.
"""

from backend.models.enums import (
    RuoloUtente, StatoPrenotazione, StatoRichiesta,
    TipoPrenotazione, TipoRicorrenza, TipoAttrezzatura,
    TipoFinanziamento, TipoConflitto
)
from backend.models.sede       import Sede
from backend.models.aula       import Aula
from backend.models.utente     import (Utente, ResponsabileCorso, ResponsabileSede,
                                        SegreteriaSede, SegreteriaDidattica, Coordinamento)
from backend.models.corso      import Corso
from backend.models.slot_orario import SlotOrario
from backend.models.prenotazione import (Prenotazione, PrenotazioneSingola,
                                          PrenotazioneMassiva, RichiestaPrenotazione,
                                          Conflitto)
from backend.models.attrezzatura import Attrezzatura, RichiestaAttrezzatura

__all__ = [
    "RuoloUtente", "StatoPrenotazione", "StatoRichiesta", "TipoPrenotazione",
    "TipoRicorrenza", "TipoAttrezzatura", "TipoFinanziamento", "TipoConflitto",
    "Sede", "Aula", "Utente", "ResponsabileCorso", "ResponsabileSede",
    "SegreteriaSede", "SegreteriaDidattica", "Coordinamento",
    "Corso", "SlotOrario", "Prenotazione", "PrenotazioneSingola",
    "PrenotazioneMassiva", "RichiestaPrenotazione", "Conflitto",
    "Attrezzatura", "RichiestaAttrezzatura",
]