"""
incrocio_dati.py
================
Incrocia cm_filtrati.xlsx e luca_filtrati.xlsx tramite codice fiscale:
  - cm_filtrati  → Colonna B (CF su Proforma)
  - luca_filtrati → Colonna H (COD FISC DESTINATARI)

Produce destinazione/risultati.xlsx con i match trovati.
"""

import os
import sys
import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURAZIONE PERCORSI
# ---------------------------------------------------------------------------
BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
DESTINAZIONE = os.path.join(BASE_DIR, "destinazione")

FILE_CM   = os.path.join(DESTINAZIONE, "cm_filtrati.xlsx")
FILE_LUCA = os.path.join(DESTINAZIONE, "luca_filtrati.xlsx")
FILE_OUT  = os.path.join(DESTINAZIONE, "risultati.xlsx")

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def leggi_excel(percorso: str) -> pd.DataFrame:
    print(f"  → Leggo: {percorso}")
    try:
        df = pd.read_excel(percorso, engine="openpyxl", dtype=str)
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        print(f"     {len(df)} righe, {len(df.columns)} colonne.")
        return df
    except FileNotFoundError:
        print(f"  [ERRORE] File non trovato: {percorso}")
        sys.exit(1)


def colonna_per_lettera(df: pd.DataFrame, lettera: str) -> str:
    lettera = lettera.upper()
    idx = 0
    for ch in lettera:
        idx = idx * 26 + (ord(ch) - ord('A') + 1)
    idx -= 1
    if idx >= len(df.columns):
        raise IndexError(
            f"Colonna '{lettera}' (indice {idx}) fuori range "
            f"({len(df.columns)} colonne totali)."
        )
    return df.columns[idx]


def normalizza_cf(serie: pd.Series) -> pd.Series:
    """Uppercase + strip per confronto robusto dei codici fiscali."""
    return serie.str.strip().str.upper()


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  INCROCIO DATI — avvio")
    print("=" * 60)

    # -- Caricamento file ----------------------------------------------------
    print("\n[1/4] Caricamento file...")
    df_cm   = leggi_excel(FILE_CM)
    df_luca = leggi_excel(FILE_LUCA)

    # -- Identificazione colonne CF ------------------------------------------
    print("\n[2/4] Identificazione colonne codice fiscale...")
    try:
        col_cf_cm   = colonna_per_lettera(df_cm,   "B")   # CF su Proforma
        col_cf_luca = colonna_per_lettera(df_luca, "H")   # COD FISC DESTINATARI
    except IndexError as e:
        print(f"  [ERRORE] {e}")
        sys.exit(1)

    print(f"     cm_filtrati   colonna B → '{col_cf_cm}'")
    print(f"     luca_filtrati colonna H → '{col_cf_luca}'")

    # -- Normalizzazione CF --------------------------------------------------
    df_cm["_cf_norm"]   = normalizza_cf(df_cm[col_cf_cm])
    df_luca["_cf_norm"] = normalizza_cf(df_luca[col_cf_luca])

    # CF validi (non vuoti) in cm_filtrati
    cf_cm_validi = df_cm[df_cm["_cf_norm"] != ""]["_cf_norm"].unique()
    print(f"\n     CF unici in cm_filtrati:   {len(cf_cm_validi)}")
    print(f"     CF unici in luca_filtrati: {df_luca[df_luca['_cf_norm'] != '']['_cf_norm'].nunique()}")

    # -- Filtro luca_filtrati: solo i CF presenti in cm_filtrati -------------
    print("\n[3/4] Ricerca corrispondenze...")
    mask_match = df_luca["_cf_norm"].isin(cf_cm_validi)
    df_luca_match = df_luca[mask_match].copy()

    cf_trovati = df_luca_match["_cf_norm"].nunique()
    print(f"     CF trovati in entrambi i file: {cf_trovati}")
    print(f"     Righe luca_filtrati con match: {len(df_luca_match)}")

    if df_luca_match.empty:
        print("\n  [ATTENZIONE] Nessuna corrispondenza trovata.")
        sys.exit(0)

    # -- Arricchimento con dati cm (join) ------------------------------------
    # Per ogni CF porta tutte le righe cm corrispondenti → merge many-to-many
    df_cm_match = df_cm[df_cm["_cf_norm"].isin(cf_cm_validi)].copy()

    # Prefisso alle colonne per distinguere le sorgenti nel file finale
    df_luca_match = df_luca_match.rename(
        columns=lambda c: f"LUCA_{c}" if c != "_cf_norm" else c
    )
    df_cm_match = df_cm_match.rename(
        columns=lambda c: f"CM_{c}" if c != "_cf_norm" else c
    )

    df_risultato = pd.merge(
        df_luca_match,
        df_cm_match,
        on="_cf_norm",
        how="inner"
    )

    # Rimuovi colonna di lavoro
    # Una sola riga per CF (prima occorrenza da ciascun file)
    df_risultato = df_risultato.drop_duplicates(subset=["_cf_norm"])
    df_risultato = df_risultato.drop(columns=["_cf_norm"])

    print(f"     Righe totali nel risultato: {len(df_risultato)}")

    # -- Salvataggio ---------------------------------------------------------
    print("\n[4/4] Salvataggio risultati...")
    os.makedirs(DESTINAZIONE, exist_ok=True)

    with pd.ExcelWriter(FILE_OUT, engine="openpyxl") as writer:
        df_risultato.to_excel(writer, sheet_name="Risultati", index=False)

    print(f"  ✔  Salvato: {FILE_OUT}")
    print(f"     • Foglio 'Risultati' → {len(df_risultato)} righe | {len(df_risultato.columns)} colonne")

    print("\n" + "=" * 60)
    print("  Elaborazione completata.")
    print("=" * 60)


if __name__ == "__main__":
    main()