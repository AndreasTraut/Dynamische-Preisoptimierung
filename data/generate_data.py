"""
Generierung synthetischer Beispieldaten für den Preisoptimierungs-Prototyp.

Erstellt drei CSV-Dateien:
  - produkte.csv        (Produktstammdaten)
  - verkaeufe.csv       (historische Verkaufsdaten)
  - wettbewerbspreise.csv (Wettbewerbspreise)
"""

import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
np.random.seed(SEED)

OUTPUT_DIR = Path(__file__).parent


# ---------------------------------------------------------------------------
# 1. Produktstammdaten
# ---------------------------------------------------------------------------
PRODUCTS = [
    {"produkt_id": "P001", "name": "Produkt A", "kategorie": "Elektronik",  "einstandspreis": 30.0, "mindestpreis": 35.0, "listenpreis": 59.99},
    {"produkt_id": "P002", "name": "Produkt B", "kategorie": "Elektronik",  "einstandspreis": 50.0, "mindestpreis": 60.0, "listenpreis": 99.99},
    {"produkt_id": "P003", "name": "Produkt C", "kategorie": "Haushalt",    "einstandspreis": 10.0, "mindestpreis": 14.0, "listenpreis": 24.99},
    {"produkt_id": "P004", "name": "Produkt D", "kategorie": "Haushalt",    "einstandspreis": 15.0, "mindestpreis": 19.0, "listenpreis": 34.99},
    {"produkt_id": "P005", "name": "Produkt E", "kategorie": "Sport",       "einstandspreis": 20.0, "mindestpreis": 25.0, "listenpreis": 44.99},
]

df_produkte = pd.DataFrame(PRODUCTS)
df_produkte.to_csv(OUTPUT_DIR / "produkte.csv", index=False)
print(f"produkte.csv: {len(df_produkte)} Zeilen")


# ---------------------------------------------------------------------------
# 2. Verkaufsdaten  (365 Tage, jedes Produkt täglich)
# ---------------------------------------------------------------------------
DATE_RANGE = pd.date_range("2023-01-01", "2023-12-31", freq="D")

records = []
sale_id = 1
for produkt in PRODUCTS:
    pid = produkt["produkt_id"]
    base_price = produkt["listenpreis"]
    elasticity = np.random.uniform(-2.5, -0.8)   # wahre (versteckte) Elastizität

    for date in DATE_RANGE:
        # Preis variiert täglich leicht um den Listenpreis
        price = base_price * np.random.uniform(0.85, 1.10)
        price = round(max(price, produkt["mindestpreis"]), 2)

        # Nachfrage: log-linear mit Preis + Saisonalität + Rauschen
        month = date.month
        season_effect = 0.15 * np.sin(2 * np.pi * (month - 3) / 12)   # Frühlings-Peak
        log_demand = (
            np.log(50)
            + elasticity * np.log(price / base_price)
            + season_effect
            + np.random.normal(0, 0.15)
        )
        quantity = max(1, int(np.round(np.exp(log_demand))))
        revenue = round(price * quantity, 2)

        records.append({
            "verkauf_id": sale_id,
            "produkt_id": pid,
            "datum": date.date(),
            "menge": quantity,
            "preis": price,
            "umsatz": revenue,
        })
        sale_id += 1

df_verkaeufe = pd.DataFrame(records)
df_verkaeufe.to_csv(OUTPUT_DIR / "verkaeufe.csv", index=False)
print(f"verkaeufe.csv: {len(df_verkaeufe)} Zeilen")


# ---------------------------------------------------------------------------
# 3. Wettbewerbspreise (wöchentlich je Produkt)
# ---------------------------------------------------------------------------
WEEK_RANGE = pd.date_range("2023-01-01", "2023-12-31", freq="W-MON")

comp_records = []
for produkt in PRODUCTS:
    pid = produkt["produkt_id"]
    base_price = produkt["listenpreis"]

    for date in WEEK_RANGE:
        comp_price = base_price * np.random.uniform(0.90, 1.15)
        comp_records.append({
            "produkt_id": pid,
            "datum": date.date(),
            "wettbewerbspreis": round(comp_price, 2),
        })

df_wettbewerb = pd.DataFrame(comp_records)
df_wettbewerb.to_csv(OUTPUT_DIR / "wettbewerbspreise.csv", index=False)
print(f"wettbewerbspreise.csv: {len(df_wettbewerb)} Zeilen")

print("\nDatengenerierung abgeschlossen.")
