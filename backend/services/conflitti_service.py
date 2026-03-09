"""
Servizio Gestione Conflitti - Sistema Automatico
Aggiornato: conflitti tracciati a livello di slot, non prenotazione intera.
"""

from typing import List, Optional
from datetime import date, time, datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from backend.models import Prenotazione, SlotOrario, ConflittoPrenotazione, RichiestaPrenotazione
from backend.models.enums import StatoPrenotazione, TipoConflitto, StatoRisoluzioneConflitto


class ConflittoService:

    @staticmethod
    def check_time_overlap(
        start1: time, end1: time,
        start2: time, end2: time
    ) -> bool:
        def to_min(t: time) -> int:
            return t.hour * 60 + t.minute
        return to_min(start1) < to_min(end2) and to_min(start2) < to_min(end1)

    @staticmethod
    def find_conflicting_slots(
        db: Session,
        aula_id: int,
        data: date,
        ora_inizio: time,
        ora_fine: time,
        exclude_booking_id: Optional[int] = None
    ) -> List[tuple[Prenotazione, SlotOrario]]:
        """
        Restituisce coppie (prenotazione, slot) in conflitto con il range dato.
        Ignora slot annullati.
        """
        query = (
            db.query(Prenotazione, SlotOrario)
            .join(SlotOrario, SlotOrario.prenotazione_id == Prenotazione.id)
            .filter(
                Prenotazione.aula_id == aula_id,
                SlotOrario.data == data,
                SlotOrario.annullato == False,
                Prenotazione.stato.in_([
                    StatoPrenotazione.CONFERMATA,
                    StatoPrenotazione.IN_ATTESA,
                ])
            )
        )
        if exclude_booking_id:
            query = query.filter(Prenotazione.id != exclude_booking_id)

        results = []
        for pren, slot in query.all():
            if ConflittoService.check_time_overlap(
                ora_inizio, ora_fine,
                slot.ora_inizio, slot.ora_fine
            ):
                results.append((pren, slot))
        return results

    @staticmethod
    def detect_and_record_conflicts(
        db: Session,
        prenotazione: Prenotazione
    ) -> List[ConflittoPrenotazione]:
        """
        Rileva e registra conflitti automaticamente.
        Deduplicazione a livello di coppia di SLOT (non di prenotazione):
        ogni coppia di slot sovrapposti genera un conflitto separato.
        Questo è necessario per le prenotazioni massive con molti slot.
        """
        conflitti_creati = []

        for slot in prenotazione.slots:
            if slot.annullato:
                continue

            coppie_in_conflitto = ConflittoService.find_conflicting_slots(
                db,
                prenotazione.aula_id,
                slot.data,
                slot.ora_inizio,
                slot.ora_fine,
                exclude_booking_id=prenotazione.id
            )

            for conflicting_pren, conflicting_slot in coppie_in_conflitto:
                # Dedup per coppia di SLOT (non prenotazione) — ogni slot ha il suo conflitto
                s1 = min(slot.id, conflicting_slot.id)
                s2 = max(slot.id, conflicting_slot.id)

                existing = db.query(ConflittoPrenotazione).filter(
                    ConflittoPrenotazione.slot_id_1 == s1,
                    ConflittoPrenotazione.slot_id_2 == s2,
                    ConflittoPrenotazione.stato_risoluzione == StatoRisoluzioneConflitto.NON_RISOLTO,
                ).first()

                if not existing:
                    # Ordina le prenotazioni per id per normalizzare
                    if prenotazione.id < conflicting_pren.id:
                        id1, id2 = prenotazione.id, conflicting_pren.id
                        sid1, sid2 = slot.id, conflicting_slot.id
                    else:
                        id1, id2 = conflicting_pren.id, prenotazione.id
                        sid1, sid2 = conflicting_slot.id, slot.id

                    conflitto = ConflittoPrenotazione(
                        prenotazione_id_1=id1,
                        prenotazione_id_2=id2,
                        slot_id_1=sid1,
                        slot_id_2=sid2,
                        tipo_conflitto=TipoConflitto.OVERLAP_ORARIO,
                    )
                    db.add(conflitto)
                    conflitti_creati.append(conflitto)

        if conflitti_creati:
            prenotazione.ha_conflitti_attivi = True
            # Aggiorna anche richiesta.ha_conflitti (letto dal frontend)
            if prenotazione.richiesta:
                prenotazione.richiesta.ha_conflitti = True

        db.flush()
        return conflitti_creati

    @staticmethod
    def get_active_conflicts(
        db: Session,
        sede_id: Optional[int] = None
    ) -> List[ConflittoPrenotazione]:
        query = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == StatoRisoluzioneConflitto.NON_RISOLTO
        )
        if sede_id:
            from backend.models import Aula
            query = (
                query
                .join(Prenotazione, ConflittoPrenotazione.prenotazione_id_1 == Prenotazione.id)
                .join(Aula, Prenotazione.aula_id == Aula.id)
                .filter(Aula.sede_id == sede_id)
            )
        return query.all()

    @staticmethod
    def _aggiorna_flag_conflitti(db: Session, prenotazione_id: int):
        """
        Ricalcola richiesta.ha_conflitti per una prenotazione dopo una risoluzione.
        Se non ha più conflitti attivi, mette ha_conflitti = False.
        """
        ha_ancora = db.query(ConflittoPrenotazione).filter(
            or_(
                ConflittoPrenotazione.prenotazione_id_1 == prenotazione_id,
                ConflittoPrenotazione.prenotazione_id_2 == prenotazione_id,
            ),
            ConflittoPrenotazione.stato_risoluzione == StatoRisoluzioneConflitto.NON_RISOLTO,
        ).first() is not None

        richiesta = db.query(RichiestaPrenotazione).filter(
            RichiestaPrenotazione.prenotazione_id == prenotazione_id
        ).first()
        if richiesta:
            richiesta.ha_conflitti = ha_ancora

        pren = db.query(Prenotazione).filter(Prenotazione.id == prenotazione_id).first()
        if pren:
            pren.ha_conflitti_attivi = ha_ancora

    @staticmethod
    def _annulla_slot_e_cleanup(db: Session, pren: Prenotazione, slot_id: int):
        """
        Annulla uno slot specifico. Se era l'ultimo slot attivo, elimina la prenotazione.
        Restituisce True se la prenotazione è stata eliminata.
        """
        slot = db.query(SlotOrario).filter(
            SlotOrario.id == slot_id,
            SlotOrario.prenotazione_id == pren.id,
        ).first()
        if slot:
            slot.annullato = True
            db.flush()

        slot_attivi = [s for s in pren.slots if not s.annullato]
        if not slot_attivi:
            richiesta = db.query(RichiestaPrenotazione).filter(
                RichiestaPrenotazione.prenotazione_id == pren.id
            ).first()
            if richiesta:
                db.delete(richiesta)
            db.delete(pren)
            db.flush()
            return True
        return False

    @staticmethod
    def resolve_conflict(
        db: Session,
        conflitto_id: int,
        risolto_da_id: int,
        azione: str,
        note: str = None
    ) -> ConflittoPrenotazione:
        """
        Risolve un conflitto.

        Azioni disponibili (tutte operano a livello di slot, non intera prenotazione):
        - mantieni_1       → annulla solo lo slot in conflitto di prenotazione_2
        - mantieni_2       → annulla solo lo slot in conflitto di prenotazione_1
        - elimina_entrambe → annulla entrambi gli slot in conflitto
        - manuale          → segna risolto senza modifiche
        """
        from sqlalchemy.orm import joinedload

        conflitto = (
            db.query(ConflittoPrenotazione)
            .options(
                joinedload(ConflittoPrenotazione.prenotazione_1).joinedload(Prenotazione.slots),
                joinedload(ConflittoPrenotazione.prenotazione_2).joinedload(Prenotazione.slots),
            )
            .filter(ConflittoPrenotazione.id == conflitto_id)
            .first()
        )

        if not conflitto:
            raise ValueError(f"Conflitto {conflitto_id} non trovato")
        if conflitto.is_risolto:
            raise ValueError(f"Conflitto {conflitto_id} già risolto")

        conflitto.risolto_da_id = risolto_da_id
        conflitto.risolto_il    = datetime.now(timezone.utc).replace(tzinfo=None)
        conflitto.note_risoluzione = note

        def elimina_pren(pren: Prenotazione):
            richiesta = db.query(RichiestaPrenotazione).filter(
                RichiestaPrenotazione.prenotazione_id == pren.id
            ).first()
            if richiesta:
                db.delete(richiesta)
            db.delete(pren)

        if azione == "mantieni_1":
            # Mantieni slot_1, annulla slot_2 (solo lo slot in conflitto)
            conflitto.stato_risoluzione = StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_1
            db.flush()
            ConflittoService._annulla_slot_e_cleanup(
                db, conflitto.prenotazione_2, conflitto.slot_id_2
            )

        elif azione == "mantieni_2":
            # Mantieni slot_2, annulla slot_1 (solo lo slot in conflitto)
            conflitto.stato_risoluzione = StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_2
            db.flush()
            ConflittoService._annulla_slot_e_cleanup(
                db, conflitto.prenotazione_1, conflitto.slot_id_1
            )

        elif azione == "elimina_entrambe":
            # Annulla entrambi gli slot in conflitto (non le intere prenotazioni)
            conflitto.stato_risoluzione = StatoRisoluzioneConflitto.RISOLTO_ELIMINATE_ENTRAMBE
            db.flush()
            ConflittoService._annulla_slot_e_cleanup(
                db, conflitto.prenotazione_1, conflitto.slot_id_1
            )
            # Ricarica prenotazione_2 nel caso non sia stata eliminata
            pren2 = db.query(Prenotazione).filter(
                Prenotazione.id == conflitto.prenotazione_id_2
            ).first()
            if pren2:
                ConflittoService._annulla_slot_e_cleanup(
                    db, pren2, conflitto.slot_id_2
                )

        elif azione == "manuale":
            conflitto.stato_risoluzione = StatoRisoluzioneConflitto.RISOLTO_MANUALE

        else:
            raise ValueError(f"Azione non valida: {azione}")

        db.commit()

        # Ricalcola ha_conflitti su entrambe le prenotazioni
        ConflittoService._aggiorna_flag_conflitti(db, conflitto.prenotazione_id_1)
        # prenotazione_2 potrebbe essere stata eliminata — verifica prima
        if db.query(Prenotazione).filter(
            Prenotazione.id == conflitto.prenotazione_id_2
        ).first():
            ConflittoService._aggiorna_flag_conflitti(db, conflitto.prenotazione_id_2)
        db.commit()

        return conflitto