"""
Esporta tutti i modelli ORM per facilitarne l'importazione.
L'ordine di importazione rispetta le dipendenze tra le tabelle.
"""

from backend.models.enums import (
    RuoloUtente, StatoPrenotazione, StatoRichiesta,
    TipoPrenotazione, TipoRicorrenza, TipoAttrezzatura,
    TipoFinanziamento, TipoConflitto,
    # Nuovi enum v3
    StatoCorso, OreAccertamento, TipoLezione,
    TipologiaDocente, Sesso, Cittadinanza, ResidenzaIn,
    LivelloIstruzione, CondizioneOccupazionale,
    DisabilitaVulnerabilita, SvantaggioAbitativo,
)
from backend.models.sede        import Sede
from backend.models.aula        import Aula
from backend.models.utente      import (Utente, ResponsabileCorso, ResponsabileSede,
                                         SegreteriaSede, SegreteriaDidattica, Coordinamento)
from backend.models.docente     import Docente
from backend.models.allievo     import Allievo
from backend.models.corso       import Corso
from backend.models.lezione     import Lezione
from backend.models.slot_orario  import SlotOrario
from backend.models.prenotazione import (Prenotazione, PrenotazioneSingola,
                                          PrenotazioneMassiva, RichiestaPrenotazione,
                                          Conflitto)
from backend.models.attrezzatura import Attrezzatura, RichiestaAttrezzatura
from backend.models.catalogo     import Catalogo


__all__ = [
    # Enum
    "RuoloUtente", "StatoPrenotazione", "StatoRichiesta", "TipoPrenotazione",
    "TipoRicorrenza", "TipoAttrezzatura", "TipoFinanziamento", "TipoConflitto",
    "StatoCorso", "OreAccertamento", "TipoLezione", "TipologiaDocente",
    "Sesso", "Cittadinanza", "ResidenzaIn", "LivelloIstruzione",
    "CondizioneOccupazionale", "DisabilitaVulnerabilita", "SvantaggioAbitativo",
    # Modelli
    "Sede", "Aula",
    "Utente", "ResponsabileCorso", "ResponsabileSede",
    "SegreteriaSede", "SegreteriaDidattica", "Coordinamento",
    "Docente", "Allievo",
    "Corso", "Lezione",
    "SlotOrario",
    "Prenotazione", "PrenotazioneSingola", "PrenotazioneMassiva",
    "RichiestaPrenotazione", "Conflitto",
    "Attrezzatura", "RichiestaAttrezzatura",
    "Catalogo",
]


__all__ = [
    # Enum
    "RuoloUtente", "StatoPrenotazione", "StatoRichiesta", "TipoPrenotazione",
    "TipoRicorrenza", "TipoAttrezzatura", "TipoFinanziamento", "TipoConflitto",
    "StatoCorso", "OreAccertamento", "TipoLezione", "TipologiaDocente",
    "Sesso", "Cittadinanza", "ResidenzaIn", "LivelloIstruzione",
    "CondizioneOccupazionale", "DisabilitaVulnerabilita", "SvantaggioAbitativo",
    # Modelli spazi 
    "Sede", "Aula",
    # Modelli persone con ruoli sul Gestionale
    "Utente", "ResponsabileCorso", "ResponsabileSede", "SegreteriaSede",
    "SegreteriaDidattica", "Coordinamento", 
    # Modelli altre figure coinvolte
    "Docente", "Allievo",
    # Modelli calendario
    "Corso", "Lezione",
    # Modello orario
    "SlotOrario",
    # Modelli prenotazioni
    "Prenotazione", "PrenotazioneSingola", "PrenotazioneMassiva",
    # Modelli richieste
    "RichiestaPrenotazione", "Conflitto",
    # Modelli attrezzatura
    "Attrezzatura", "RichiestaAttrezzatura",
    # Modello catalogo
    "Catalogo",
]

