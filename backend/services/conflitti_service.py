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
        
        print(f"🔍 FIND_CONFLICTING_SLOTS:")
        print(f"  aula_id={aula_id}, data={data}")
        print(f"  ora_inizio={ora_inizio}, ora_fine={ora_fine}")
        print(f"  exclude_booking_id={exclude_booking_id}")
        
        query = (
            db.query(Prenotazione, SlotOrario)
            .join(SlotOrario, SlotOrario.prenotazione_id == Prenotazione.id)
            .filter(
                SlotOrario.aula_id == aula_id,      
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

        all_results = query.all()
        print(f"  Trovati {len(all_results)} slot candidati:")
        for pren, slot in all_results:
            print(f"    - Pren {pren.id}, Slot {slot.id}: {slot.ora_inizio}-{slot.ora_fine}")

        results = []
        for pren, slot in all_results:
            if ConflittoService.check_time_overlap(
                ora_inizio, ora_fine,
                slot.ora_inizio, slot.ora_fine
            ):
                results.append((pren, slot))
                print(f"  ✓ OVERLAP con Pren {pren.id}, Slot {slot.id}")
            else:
                print(f"  ✗ NO overlap con Pren {pren.id}, Slot {slot.id}")
        
        print(f"  Totale conflitti trovati: {len(results)}")
        return results


    @staticmethod
    def detect_and_record_conflicts(
        db: Session,
        prenotazione: Prenotazione
    ) -> List[ConflittoPrenotazione]:
        """
        Rileva e registra TUTTI i conflitti per ogni slot della prenotazione.
        
        FIX PERMANENTE: quando trova N slot in conflitto (N>1), genera TUTTE
        le coppie possibili, non solo quelle con il nuovo slot.
        """
        conflitti_creati = []

        for slot in prenotazione.slots:
            if slot.annullato:
                continue

            # ── Conflitti con altre prenotazioni ─────────────────────────────
            coppie_in_conflitto = ConflittoService.find_conflicting_slots(
                db,
                slot.aula_id,
                slot.data,
                slot.ora_inizio,
                slot.ora_fine,
                exclude_booking_id=prenotazione.id
            )

            print(f"📍 DETECT_AND_RECORD per slot {slot.id} (pren {prenotazione.id}):")
            print(f"   Trovate {len(coppie_in_conflitto)} coppie in conflitto")

            # Raccogli tutti gli slot in conflitto (incluso quello nuovo)
            tutti_slot_in_conflitto = [slot] + [conflicting_slot for _, conflicting_slot in coppie_in_conflitto]
            
            print(f"   tutti_slot_in_conflitto: {[s.id for s in tutti_slot_in_conflitto]}")
            
            # Genera TUTTE le coppie possibili
            for i in range(len(tutti_slot_in_conflitto)):
                for j in range(i + 1, len(tutti_slot_in_conflitto)):
                    slot_a = tutti_slot_in_conflitto[i]
                    slot_b = tutti_slot_in_conflitto[j]
                    
                    # Ordina per ID slot (minore sempre come slot_id_1)
                    s1 = min(slot_a.id, slot_b.id)
                    s2 = max(slot_a.id, slot_b.id)

                    print(f"   Coppia slot {s1} <-> {s2}")

                    # Verifica se esiste già UN CONFLITTO ATTIVO (non risolto)
                    existing = db.query(ConflittoPrenotazione).filter(
                        ConflittoPrenotazione.slot_id_1 == s1,
                        ConflittoPrenotazione.slot_id_2 == s2,
                        ConflittoPrenotazione.stato_risoluzione == None  # ← AGGIUNGI QUESTO
                    ).first()

                    print(f"     Existing? {existing.id if existing else 'NO'}")

                    if not existing:
                        # Ordina per ID prenotazione
                        if slot_a.prenotazione_id < slot_b.prenotazione_id:
                            id1, id2 = slot_a.prenotazione_id, slot_b.prenotazione_id
                            sid1, sid2 = slot_a.id, slot_b.id
                        else:
                            id1, id2 = slot_b.prenotazione_id, slot_a.prenotazione_id
                            sid1, sid2 = slot_b.id, slot_a.id

                        print(f"     CREANDO conflitto: pren {id1}<->{id2}, slot {sid1}<->{sid2}")

                        conflitto = ConflittoPrenotazione(
                            prenotazione_id_1=id1,
                            prenotazione_id_2=id2,
                            slot_id_1=sid1,
                            slot_id_2=sid2,
                            tipo_conflitto=TipoConflitto.OVERLAP_ORARIO,
                        )
                        db.add(conflitto)
                        conflitti_creati.append(conflitto)

            # ── Conflitti intra-prenotazione (stessa prenotazione) ────────────
            for altro_slot in prenotazione.slots:
                if altro_slot.id == slot.id or altro_slot.annullato:
                    continue
                if altro_slot.aula_id != slot.aula_id:
                    continue
                if altro_slot.data != slot.data:
                    continue
                if not ConflittoService.check_time_overlap(
                    slot.ora_inizio, slot.ora_fine,
                    altro_slot.ora_inizio, altro_slot.ora_fine
                ):
                    continue

                # Conflitto trovato — dedup per coppia di slot
                s1 = min(slot.id, altro_slot.id)
                s2 = max(slot.id, altro_slot.id)

                existing = db.query(ConflittoPrenotazione).filter(
                    ConflittoPrenotazione.slot_id_1 == s1,
                    ConflittoPrenotazione.slot_id_2 == s2,
                    ConflittoPrenotazione.stato_risoluzione == None  # ← AGGIUNGI QUESTO
                ).first()
                
                if not existing:
                    conflitto = ConflittoPrenotazione(
                        prenotazione_id_1=prenotazione.id,
                        prenotazione_id_2=prenotazione.id,
                        slot_id_1=s1,
                        slot_id_2=s2,
                        tipo_conflitto=TipoConflitto.OVERLAP_ORARIO,
                    )
                    db.add(conflitto)
                    conflitti_creati.append(conflitto)

        if conflitti_creati:
            prenotazione.ha_conflitti_attivi = True
            if prenotazione.richiesta:
                prenotazione.richiesta.ha_conflitti = True

        print(f"✅ TOTALE CONFLITTI CREATI: {len(conflitti_creati)}")
        db.flush()
        return conflitti_creati

    @staticmethod
    def get_active_conflicts(
        db: Session,
        sede_id: Optional[int] = None
    ) -> List[ConflittoPrenotazione]:
        query = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == None
        )
        if sede_id:
            from backend.models import Aula
            query = (
                query
                .join(SlotOrario, ConflittoPrenotazione.slot_id_1 == SlotOrario.id)
                .join(Aula, SlotOrario.aula_id == Aula.id)
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
            ConflittoPrenotazione.stato_risoluzione == None,
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

        conflitto.risolto_da = risolto_da_id
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

        else:
            raise ValueError(f"Azione non valida: {azione}")

        # FIX: rimosso db.commit() — il commit è responsabilità esclusiva del router/caller.
        # Ricalcola ha_conflitti su entrambe le prenotazioni (solo flush, niente commit)
        ConflittoService._aggiorna_flag_conflitti(db, conflitto.prenotazione_id_1)
        if db.query(Prenotazione).filter(
            Prenotazione.id == conflitto.prenotazione_id_2
        ).first():
            ConflittoService._aggiorna_flag_conflitti(db, conflitto.prenotazione_id_2)
        db.flush()

        return conflitto