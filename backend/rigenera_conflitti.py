"""
Script da eseguire UNA VOLTA dopo fix_conflitti_mancanti.sql.
Rianalizza tutte le prenotazioni attive e rigenera i conflitti con la nuova logica slot-level.

Uso:
  cd backend
  python rigenera_conflitti.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models.prenotazione import Prenotazione
from backend.models.enums import StatoPrenotazione
from backend.services.conflitti_service import ConflittoService
from sqlalchemy.orm import joinedload

def main():
    db = SessionLocal()
    try:
        prenotazioni = (
            db.query(Prenotazione)
            .options(joinedload(Prenotazione.slots))
            .filter(Prenotazione.stato == StatoPrenotazione.CONFERMATA)
            .all()
        )
        print(f"Prenotazioni da analizzare: {len(prenotazioni)}")

        totale_conflitti = 0
        for p in prenotazioni:
            conflitti = ConflittoService.detect_and_record_conflicts(db, p)
            if conflitti:
                print(f"  Prenotazione #{p.id}: {len(conflitti)} conflitti rilevati")
                totale_conflitti += len(conflitti)

        db.commit()
        print(f"\nTotale conflitti generati: {totale_conflitti}")
    finally:
        db.close()

if __name__ == "__main__":
    main()