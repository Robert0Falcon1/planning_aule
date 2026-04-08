"""
filtra_dati.py
==============
Filtra dati da file Excel nelle cartelle origine/luca e origine/silp
e produce i file luca_filtrati.xlsx e cm_filtrati.xlsx in cartella destinazione.

Struttura attesa:
    origine/
        luca/
            estrazione.xls
            estrazione2.xls
        silp/
            DB_2023.xlsx
            DB_2024.xlsx
            DB_2025.xlsx
            DB_2026.xlsx
    destinazione/
        luca_filtrati.xlsx   <-- output
        cm_filtrati.xlsx     <-- output
"""

import os
import sys
import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURAZIONE PERCORSI
# ---------------------------------------------------------------------------
BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
ORIGINE_LUCA   = os.path.join(BASE_DIR, "origine", "luca")
ORIGINE_SILP   = os.path.join(BASE_DIR, "origine", "silp")
DESTINAZIONE   = os.path.join(BASE_DIR, "destinazione")

# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def leggi_file(percorso: str, foglio=0) -> pd.DataFrame:
    """Legge un file .xls o .xlsx in un DataFrame."""
    ext = os.path.splitext(percorso)[1].lower()
    print(f"  → Leggo: {percorso}")
    try:
        if ext == ".xls":
            df = pd.read_excel(percorso, sheet_name=foglio, engine="xlrd", dtype=str)
        else:
            df = pd.read_excel(percorso, sheet_name=foglio, engine="openpyxl", dtype=str)
        df.columns = df.columns.str.strip()
        df = df.fillna("")
        print(f"     {len(df)} righe lette.")
        return df
    except FileNotFoundError:
        print(f"  [ATTENZIONE] File non trovato: {percorso}. Salto.")
        return pd.DataFrame()
    except Exception as e:
        print(f"  [ERRORE] {percorso}: {e}")
        return pd.DataFrame()


def colonna_per_lettera(df: pd.DataFrame, lettera: str) -> str:
    """
    Restituisce il nome reale della colonna corrispondente alla lettera Excel
    (A=0, B=1, ..., Z=25, AA=26, ...).
    Utile se le intestazioni non corrispondono al nome atteso.
    """
    lettera = lettera.upper()
    idx = 0
    for ch in lettera:
        idx = idx * 26 + (ord(ch) - ord('A') + 1)
    idx -= 1  # 0-based
    if idx >= len(df.columns):
        raise IndexError(
            f"La colonna '{lettera}' (indice {idx}) è fuori range "
            f"({len(df.columns)} colonne totali)."
        )
    return df.columns[idx]


def normalizza(valore: str) -> str:
    return valore.strip().upper()


def salva_excel(df: pd.DataFrame, percorso: str, nome_foglio: str = "Dati") -> None:
    os.makedirs(os.path.dirname(percorso), exist_ok=True)
    with pd.ExcelWriter(percorso, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name=nome_foglio, index=False)
    print(f"  ✔  Salvato: {percorso}  ({len(df)} righe)")


# ---------------------------------------------------------------------------
# BLOCCO 1 — LUCA
# ---------------------------------------------------------------------------

def processa_luca() -> None:
    print("\n=== BLOCCO 1: origine/luca ===")

    file_luca = [
        os.path.join(ORIGINE_LUCA, "estrazione.xls"),
        os.path.join(ORIGINE_LUCA, "estrazione2.xls"),
    ]

    # Colonna M = indice 12, Colonna X = indice 23
    COL_M_LETTERA = "M"   # RENDICONTATO
    COL_X_LETTERA = "X"   # INTERVENTO CORSO RENDICONTABILE

    frames = []

    for filepath in file_luca:
        df = leggi_file(filepath)
        if df.empty:
            continue

        try:
            col_m = colonna_per_lettera(df, COL_M_LETTERA)
            col_x = colonna_per_lettera(df, COL_X_LETTERA)
        except IndexError as e:
            print(f"  [ERRORE] {filepath}: {e}")
            continue

        print(f"     Colonna M → '{col_m}' | Colonna X → '{col_x}'")

        mask = (
            df[col_m].apply(normalizza) == "NO"
        ) | (
            df[col_x].apply(normalizza) == "NO"
        )

        filtrato = df[mask].copy()
        # Aggiungi colonna sorgente per tracciabilità
        filtrato.insert(0, "_sorgente", os.path.basename(filepath))
        print(f"     Righe filtrate: {len(filtrato)}")
        frames.append(filtrato)

    if frames:
        risultato = pd.concat(frames, ignore_index=True)
        output_path = os.path.join(DESTINAZIONE, "luca_filtrati.xlsx")
        salva_excel(risultato, output_path, nome_foglio="Luca_filtrati")
    else:
        print("  [ATTENZIONE] Nessun dato trovato per luca_filtrati.")


# ---------------------------------------------------------------------------
# BLOCCO 2 — SILP
# ---------------------------------------------------------------------------

def processa_silp() -> None:
    print("\n=== BLOCCO 2: origine/silp ===")

    FOGLIO_SILP = "exp_SILP"
    ADDETTI     = {"FALCONE SERENA", "MAINERO CLAUDIA"}

    # DB_2023/2024/2025 → Colonna Y (indice 24)
    # DB_2026           → Colonna V (indice 21)
    file_silp = [
        ("DB_2023.xlsx", "Y"),
        ("DB_2024.xlsx", "Y"),
        ("DB_2025.xlsx", "Y"),
        ("DB_2026.xlsx", "V"),
    ]

    frames = []

    for nome_file, col_lettera in file_silp:
        filepath = os.path.join(ORIGINE_SILP, nome_file)
        df = leggi_file(filepath, foglio=FOGLIO_SILP)
        if df.empty:
            continue

        try:
            col_addetto = colonna_per_lettera(df, col_lettera)
        except IndexError as e:
            print(f"  [ERRORE] {filepath}: {e}")
            continue

        print(f"     Colonna {col_lettera} → '{col_addetto}'")

        mask = df[col_addetto].apply(normalizza).isin(ADDETTI)
        filtrato = df[mask].copy()
        filtrato.insert(0, "_sorgente", nome_file)
        print(f"     Righe filtrate: {len(filtrato)}")
        frames.append(filtrato)

    if frames:
        risultato = pd.concat(frames, ignore_index=True)
        output_path = os.path.join(DESTINAZIONE, "cm_filtrati.xlsx")
        salva_excel(risultato, output_path, nome_foglio="CM_filtrati")
    else:
        print("  [ATTENZIONE] Nessun dato trovato per cm_filtrati.")


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  FILTRA DATI — avvio")
    print("=" * 60)

    # Controlla dipendenze
    for lib in ("pandas", "openpyxl", "xlrd"):
        try:
            __import__(lib)
        except ImportError:
            print(f"[ERRORE] Libreria mancante: {lib}")
            print(f"         Installa con:  pip install {lib}")
            sys.exit(1)

    processa_luca()
    processa_silp()

    print("\n" + "=" * 60)
    print("  Elaborazione completata.")
    print("=" * 60)


if __name__ == "__main__":
    main()