"""
Servizio Gestione Conflitti - Sistema Automatico
"""

from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from backend.models import Prenotazione, SlotOrario, ConflittoPrenotazione, RichiestaPrenotazione
from backend.models.enums import StatoPrenotazione, TipoConflitto, StatoRisoluzioneConflitto


class ConflittoService:
    """Servizio per rilevamento e gestione conflitti prenotazioni"""
    
    @staticmethod
    def check_time_overlap(
        start1: time, end1: time,
        start2: time, end2: time
    ) -> bool:
        """Verifica sovrapposizione tra due intervalli orari"""
        def time_to_minutes(t: time) -> int:
            return t.hour * 60 + t.minute
        
        start1_min = time_to_minutes(start1)
        end1_min = time_to_minutes(end1)
        start2_min = time_to_minutes(start2)
        end2_min = time_to_minutes(end2)
        
        return start1_min < end2_min and start2_min < end1_min
    
    @staticmethod
    def find_conflicting_bookings(
        db: Session,
        aula_id: int,
        data: date,
        ora_inizio: time,
        ora_fine: time,
        exclude_booking_id: Optional[int] = None
    ) -> List[Prenotazione]:
        """Trova prenotazioni in conflitto"""
        query = (
            db.query(Prenotazione)
            .join(SlotOrario)
            .filter(
                Prenotazione.aula_id == aula_id,
                SlotOrario.data == data,
                Prenotazione.stato.in_([
                    StatoPrenotazione.CONFERMATA,
                    StatoPrenotazione.IN_ATTESA
                ])
            )
        )
        
        if exclude_booking_id:
            query = query.filter(Prenotazione.id != exclude_booking_id)
        
        existing_bookings = query.all()
        
        conflicts = []
        for booking in existing_bookings:
            for slot in booking.slots:
                if slot.data == data:
                    if ConflittoService.check_time_overlap(
                        ora_inizio, ora_fine,
                        slot.ora_inizio, slot.ora_fine
                    ):
                        conflicts.append(booking)
                        break
        
        return conflicts
    
    @staticmethod
    def detect_and_record_conflicts(
        db: Session,
        prenotazione: Prenotazione
    ) -> List[ConflittoPrenotazione]:
        """Rileva e registra conflitti automaticamente"""
        conflitti_creati = []
        
        for slot in prenotazione.slots:
            conflicting = ConflittoService.find_conflicting_bookings(
                db,
                prenotazione.aula_id,
                slot.data,
                slot.ora_inizio,
                slot.ora_fine,
                exclude_booking_id=prenotazione.id
            )
            
            for conflicting_booking in conflicting:
                existing = db.query(ConflittoPrenotazione).filter(
                    or_(
                        and_(
                            ConflittoPrenotazione.prenotazione_id_1 == prenotazione.id,
                            ConflittoPrenotazione.prenotazione_id_2 == conflicting_booking.id
                        ),
                        and_(
                            ConflittoPrenotazione.prenotazione_id_1 == conflicting_booking.id,
                            ConflittoPrenotazione.prenotazione_id_2 == prenotazione.id
                        )
                    ),
                    ConflittoPrenotazione.stato_risoluzione == StatoRisoluzioneConflitto.NON_RISOLTO
                ).first()
                
                if not existing:
                    conflitto = ConflittoPrenotazione(
                        prenotazione_id_1=min(prenotazione.id, conflicting_booking.id),
                        prenotazione_id_2=max(prenotazione.id, conflicting_booking.id),
                        tipo_conflitto=TipoConflitto.OVERLAP_ORARIO
                    )
                    db.add(conflitto)
                    conflitti_creati.append(conflitto)
        
        if conflitti_creati:
            prenotazione.ha_conflitti_attivi = True
        
        db.flush()
        return conflitti_creati
    
    @staticmethod
    def get_active_conflicts(
        db: Session,
        sede_id: Optional[int] = None
    ) -> List[ConflittoPrenotazione]:
        """Recupera conflitti attivi (non risolti)"""
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
    def resolve_conflict(
        db: Session,
        conflitto_id: int,
        risolto_da_user_id: int,
        azione: str,
        note: Optional[str] = None
    ) -> ConflittoPrenotazione:
        """Risolve un conflitto"""

        conflitto = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.id == conflitto_id
        ).first()

        if not conflitto:
            raise ValueError(f"Conflitto {conflitto_id} non trovato")

        if conflitto.is_risolto:
            raise ValueError(f"Conflitto {conflitto_id} già risolto")

        def elimina_prenotazione_con_richiesta(prenotazione):
            if not prenotazione:
                return

            # Elimina prima la richiesta associata
            richiesta = db.query(RichiestaPrenotazione).filter(
                RichiestaPrenotazione.prenotazione_id == prenotazione.id
            ).first()

            if richiesta:
                db.delete(richiesta)

            # Poi elimina la prenotazione
            db.delete(prenotazione)

        if azione == 'mantieni_1':
            elimina_prenotazione_con_richiesta(conflitto.prenotazione_2)
            stato = StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_1

        elif azione == 'mantieni_2':
            elimina_prenotazione_con_richiesta(conflitto.prenotazione_1)
            stato = StatoRisoluzioneConflitto.RISOLTO_MANTENUTA_2

        elif azione == 'elimina_entrambe':
            elimina_prenotazione_con_richiesta(conflitto.prenotazione_1)
            elimina_prenotazione_con_richiesta(conflitto.prenotazione_2)
            stato = StatoRisoluzioneConflitto.RISOLTO_ELIMINATE_ENTRAMBE

        elif azione == 'manuale':
            stato = StatoRisoluzioneConflitto.RISOLTO_MANUALE

        else:
            raise ValueError(f"Azione '{azione}' non valida")

        conflitto.risolvi(risolto_da_user_id, stato, note)

        db.flush()
        return conflitto