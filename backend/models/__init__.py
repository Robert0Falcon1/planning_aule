"""
Esporta tutti i modelli ORM per facilitarne l'importazione.
L'ordine di importazione rispetta le dipendenze tra le tabelle.
"""

from backend.models.enums import (
    RuoloUtente, StatoPrenotazione, StatoRichiesta,
    TipoPrenotazione, TipoRicorrenza, TipoAttrezzatura,
    TipoFinanziamento, TipoConflitto, StatoRisoluzioneConflitto,
    # Enum v3
    StatoCorso, OreAccertamento, TipoLezione,
    TipologiaDocente, Sesso, Cittadinanza, ResidenzaIn,
    LivelloIstruzione, CondizioneOccupazionale,
    DisabilitaVulnerabilita, SvantaggioAbitativo,
)
from backend.models.sede         import Sede
from backend.models.aula         import Aula
from backend.models.utente       import Utente
from backend.models.docente      import Docente
from backend.models.allievo      import Allievo
from backend.models.corso        import Corso
from backend.models.lezione      import Lezione
from backend.models.slot_orario  import SlotOrario
from backend.models.prenotazione import (
    Prenotazione, PrenotazioneSingola,
    PrenotazioneMassiva, RichiestaPrenotazione,
)
from backend.models.attrezzatura import Attrezzatura, RichiestaAttrezzatura
from backend.models.catalogo     import Catalogo
from backend.models.conflitto    import ConflittoPrenotazione

__all__ = [
    # Enum
    "RuoloUtente", "StatoPrenotazione", "StatoRichiesta", "TipoPrenotazione",
    "TipoRicorrenza", "TipoAttrezzatura", "TipoFinanziamento",
    "TipoConflitto", "StatoRisoluzioneConflitto",
    "StatoCorso", "OreAccertamento", "TipoLezione", "TipologiaDocente",
    "Sesso", "Cittadinanza", "ResidenzaIn", "LivelloIstruzione",
    "CondizioneOccupazionale", "DisabilitaVulnerabilita", "SvantaggioAbitativo",
    # Modelli
    "Sede", "Aula",
    "Utente",
    "Docente", "Allievo",
    "Corso", "Lezione",
    "SlotOrario",
    "Prenotazione", "PrenotazioneSingola", "PrenotazioneMassiva",
    "RichiestaPrenotazione", "ConflittoPrenotazione",
    "Attrezzatura", "RichiestaAttrezzatura",
    "Catalogo",
]