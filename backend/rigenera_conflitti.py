"""
Script per rigenerare TUTTI i conflitti tra slot.
Da eseguire quando il rilevamento automatico ha lasciato buchi.
"""

from sqlalchemy.orm import Session
from backend.database import SessionLocal
from backend.models import SlotOrario, ConflittoPrenotazione, Prenotazione
from backend.models.enums import StatoPrenotazione, TipoConflitto
from datetime import time


def check_time_overlap(start1: time, end1: time, start2: time, end2: time) -> bool:
    """Verifica sovrapposizione oraria."""
    def to_min(t: time) -> int:
        return t.hour * 60 + t.minute
    return to_min(start1) < to_min(end2) and to_min(start2) < to_min(end1)


def rigenera_tutti_i_conflitti():
    """
    Rigenera TUTTI i conflitti da zero.
    1. Elimina tutti i conflitti NON risolti
    2. Scansiona tutti gli slot attivi
    3. Per ogni gruppo di slot sovrapposti, crea TUTTE le coppie di conflitti
    """
    db: Session = SessionLocal()
    
    try:
        print("🔄 Rimozione conflitti non risolti esistenti...")
        conflitti_rimossi = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == None
        ).delete()
        print(f"   ✓ Rimossi {conflitti_rimossi} conflitti non risolti")
        
        # Carica tutti gli slot attivi, confermati o in attesa
        print("\n📊 Caricamento slot attivi...")
        slot_attivi = (
            db.query(SlotOrario)
            .join(Prenotazione, SlotOrario.prenotazione_id == Prenotazione.id)
            .filter(
                SlotOrario.annullato == False,
                Prenotazione.stato.in_([
                    StatoPrenotazione.CONFERMATA,
                    StatoPrenotazione.IN_ATTESA,
                ])
            )
            .all()
        )
        print(f"   ✓ Trovati {len(slot_attivi)} slot attivi")
        
        # Raggruppa per (aula_id, data)
        print("\n🔍 Raggruppamento per aula e data...")
        gruppi = {}
        for slot in slot_attivi:
            key = (slot.aula_id, slot.data)
            if key not in gruppi:
                gruppi[key] = []
            gruppi[key].append(slot)
        
        print(f"   ✓ Creati {len(gruppi)} gruppi (aula + data)")
        
        # Per ogni gruppo, trova tutte le coppie in conflitto
        print("\n⚔️  Rilevamento conflitti...")
        conflitti_creati = 0
        
        for (aula_id, data), slots in gruppi.items():
            if len(slots) < 2:
                continue  # Nessun conflitto possibile
            
            # Genera tutte le coppie possibili
            for i in range(len(slots)):
                for j in range(i + 1, len(slots)):
                    slot1 = slots[i]
                    slot2 = slots[j]
                    
                    # Verifica sovrapposizione oraria
                    if not check_time_overlap(
                        slot1.ora_inizio, slot1.ora_fine,
                        slot2.ora_inizio, slot2.ora_fine
                    ):
                        continue
                    
                    # Conflitto trovato! Crea record
                    # Ordina per ID slot (minore sempre come slot_id_1)
                    s1 = min(slot1.id, slot2.id)
                    s2 = max(slot1.id, slot2.id)
                    
                    # Ordina per ID prenotazione
                    if slot1.prenotazione_id < slot2.prenotazione_id:
                        p1, p2 = slot1.prenotazione_id, slot2.prenotazione_id
                        sid1, sid2 = slot1.id, slot2.id
                    else:
                        p1, p2 = slot2.prenotazione_id, slot1.prenotazione_id
                        sid1, sid2 = slot2.id, slot1.id
                    
                    conflitto = ConflittoPrenotazione(
                        prenotazione_id_1=p1,
                        prenotazione_id_2=p2,
                        slot_id_1=sid1,
                        slot_id_2=sid2,
                        tipo_conflitto=TipoConflitto.OVERLAP_ORARIO,
                    )
                    db.add(conflitto)
                    conflitti_creati += 1
        
        print(f"   ✓ Creati {conflitti_creati} nuovi conflitti")
        
        # Aggiorna flag ha_conflitti sulle prenotazioni
        print("\n🚩 Aggiornamento flag conflitti sulle prenotazioni...")
        prenotazioni_con_conflitti = set()
        for conflitto in db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == None
        ).all():
            prenotazioni_con_conflitti.add(conflitto.prenotazione_id_1)
            prenotazioni_con_conflitti.add(conflitto.prenotazione_id_2)
        
        # Resetta tutti i flag
        db.query(Prenotazione).update({Prenotazione.ha_conflitti_attivi: False})
        
        # Imposta flag per prenotazioni in conflitto
        if prenotazioni_con_conflitti:
            db.query(Prenotazione).filter(
                Prenotazione.id.in_(prenotazioni_con_conflitti)
            ).update({Prenotazione.ha_conflitti_attivi: True}, synchronize_session=False)
        
        print(f"   ✓ Aggiornate {len(prenotazioni_con_conflitti)} prenotazioni con flag conflitto")
        
        db.commit()
        print("\n✅ Rigenerazione conflitti completata con successo!")
        
        # Statistiche finali
        totale_conflitti = db.query(ConflittoPrenotazione).filter(
            ConflittoPrenotazione.stato_risoluzione == None
        ).count()
        print(f"\n📈 Riepilogo:")
        print(f"   • Conflitti attivi: {totale_conflitti}")
        print(f"   • Prenotazioni coinvolte: {len(prenotazioni_con_conflitti)}")
        
    except Exception as e:
        print(f"\n❌ Errore: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("RIGENERAZIONE CONFLITTI - ICE Planning Aule")
    print("=" * 60)
    rigenera_tutti_i_conflitti()