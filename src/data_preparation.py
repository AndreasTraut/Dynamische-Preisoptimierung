"""
data_preparation.py
-------------------
Lädt die synthetischen CSV-Daten, integriert sie und führt
Feature Engineering durch.

Prototyp-DWH-Simulation:
  Statt SQL Server wird SQLite als lokale Datenbank verwendet,
  damit der Prototyp ohne externe Datenbankinstallation lauffähig ist.
  Die Tabellen- und Spaltenbezeichnungen entsprechen denen in
  sql/create_tables.sql (SQL-Server-kompatibel).
"""

from pathlib import Path

import numpy as np
import pandas as pd
import sqlite3

# ---------------------------------------------------------------------------
# Konfiguration
# ---------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent.parent / "data"
DB_PATH = Path(__file__).parent.parent / "PricingPrototypeDB.sqlite"


# ---------------------------------------------------------------------------
# Hilfsfunktion: Datenbank-Verbindung
# ---------------------------------------------------------------------------
def get_connection() -> sqlite3.Connection:
    """Gibt eine Verbindung zur lokalen SQLite-Datenbank zurück."""
    return sqlite3.connect(DB_PATH)


# ---------------------------------------------------------------------------
# ETL: CSV -> SQLite (simuliert Staging → Core)
# ---------------------------------------------------------------------------
def load_csv_to_db() -> None:
    """
    Lädt die drei CSV-Dateien aus data/ in die lokale SQLite-Datenbank
    (simuliert den BULK-INSERT / SSIS ETL-Prozess).
    """
    df_produkte = pd.read_csv(DATA_DIR / "produkte.csv")
    df_verkaeufe = pd.read_csv(DATA_DIR / "verkaeufe.csv", parse_dates=["datum"])
    df_wettbewerb = pd.read_csv(DATA_DIR / "wettbewerbspreise.csv", parse_dates=["datum"])

    with get_connection() as con:
        df_produkte.to_sql("Produkte", con, if_exists="replace", index=False)
        df_verkaeufe.to_sql("Verkaeufe", con, if_exists="replace", index=False)
        df_wettbewerb.to_sql("Wettbewerbspreise", con, if_exists="replace", index=False)

    print("ETL abgeschlossen: Daten in PricingPrototypeDB.sqlite geladen.")


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------
def build_feature_dataframe() -> pd.DataFrame:
    """
    Liest Verkaufs- und Wettbewerbsdaten aus der DB, ergänzt sie mit
    Feature-Engineering-Merkmalen und gibt einen Modellierungs-DataFrame zurück.

    Features:
      Zeitmerkmale   - monat, tag_des_jahres, ist_wochenende, quartal
      Preis-Features - log_preis, preis_relativ_zu_listenpreis,
                       preis_relativ_zu_wettbewerb
      Rollierende    - rollierender_umsatz_7d, rollierender_umsatz_30d,
                       rollierender_preis_7d
      Zielvariable   - log_menge  (für log-lineare Regression)
    """
    with get_connection() as con:
        df_v = pd.read_sql(
            "SELECT v.*, p.listenpreis, p.einstandspreis, p.kategorie "
            "FROM Verkaeufe v JOIN Produkte p USING(produkt_id)",
            con,
            parse_dates=["datum"],
        )
        df_w = pd.read_sql(
            "SELECT produkt_id, datum, wettbewerbspreis FROM Wettbewerbspreise",
            con,
            parse_dates=["datum"],
        )

    # Wettbewerbspreis: letzten bekannten Wert je Woche vorwärts-füllen
    df_w = df_w.sort_values("datum")
    df_v = df_v.sort_values("datum")

    # Merge: nächster Wettbewerbspreis ≤ Verkaufsdatum
    df = pd.merge_asof(
        df_v,
        df_w,
        on="datum",
        by="produkt_id",
        direction="backward",
    )

    # --- Zeitmerkmale ---
    df["monat"] = df["datum"].dt.month
    df["quartal"] = df["datum"].dt.quarter
    df["tag_des_jahres"] = df["datum"].dt.dayofyear
    df["ist_wochenende"] = (df["datum"].dt.dayofweek >= 5).astype(int)

    # --- Preis-Features ---
    df["log_preis"] = np.log(df["preis"])
    df["preis_relativ_zu_listenpreis"] = df["preis"] / df["listenpreis"]
    df["preis_relativ_zu_wettbewerb"] = np.where(
        df["wettbewerbspreis"].notna(),
        df["preis"] / df["wettbewerbspreis"],
        1.0,
    )

    # --- Rollierende Kennzahlen (je Produkt) ---
    df = df.sort_values(["produkt_id", "datum"])
    for pid, grp in df.groupby("produkt_id"):
        idx = grp.index
        df.loc[idx, "rollierender_umsatz_7d"] = (
            grp["umsatz"].rolling(7, min_periods=1).mean()
        )
        df.loc[idx, "rollierender_umsatz_30d"] = (
            grp["umsatz"].rolling(30, min_periods=1).mean()
        )
        df.loc[idx, "rollierender_preis_7d"] = (
            grp["preis"].rolling(7, min_periods=1).mean()
        )

    # --- Log-Transformation der Zielvariablen ---
    df["log_menge"] = np.log(df["menge"].clip(lower=1))

    # --- Kategorische Kodierung ---
    df["kategorie_code"] = pd.Categorical(df["kategorie"]).codes
    df["produkt_code"] = pd.Categorical(df["produkt_id"]).codes

    return df.reset_index(drop=True)


if __name__ == "__main__":
    load_csv_to_db()
    df = build_feature_dataframe()
    print(f"\nFeature-DataFrame: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")
    print(df[["produkt_id", "datum", "preis", "menge", "log_preis", "log_menge",
              "preis_relativ_zu_wettbewerb"]].head(10).to_string(index=False))
