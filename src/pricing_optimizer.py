"""
pricing_optimizer.py
--------------------
Ableitung optimaler Preisempfehlungen aus den geschätzten
Preiselastizitäten.

Ansatz (präskriptive Analytik):
  Gegeben:
    - Preiselastizität ε   (aus dem ML-Modell)
    - Aktueller Preis P₀   (letzter Verkaufspreis)
    - Aktuelle Menge Q₀    (letzte beobachtete Menge, oder Durchschnitt)
    - Einstandspreis C      (aus Produktstamm)
    - Mindestpreis P_min    (untere Preisgrenze)
    - Wettbewerbspreis P_w  (optional)

  Umsatz-maximierender Preis (Amoroso-Robinson-Relation):
    P* = C / (1 + 1/ε)   für |ε| > 1  (elastische Nachfrage)

  Der empfohlene Preis berücksichtigt zusätzlich Wettbewerb und Mindestmarge.

Ausgabe wird in der Tabelle dbo.ModelOutput (SQLite: ModelOutput) gespeichert.

Dokumentation:
  docs/MODELL_DOKUMENTATION.md – Kap. 6 (Preisempfehlung) und Kap. 6.3 (Konkrete Berechnungen)
  Studienarbeit Kap. 4.4: „Ableitung von Preisempfehlungen aus den Modellergebnissen"
  Studienarbeit Kap. 6:   „Operationalisierung und Monitoring im BI-System"
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import numpy as np
import pandas as pd

from src.model import ElasticityResult


# ---------------------------------------------------------------------------
# Business-Regeln (konfigurierbar)
# ---------------------------------------------------------------------------
MIN_MARGIN_RATE: float = 0.10     # Mindestmarge: 10 % auf Einstandspreis
WETTBEWERB_GEWICHT: float = 0.30  # 30 % Gewichtung des Wettbewerbspreises
MAX_PREIS_ÄNDERUNG: float = 0.20  # Max. Preisänderung ±20 % je Empfehlung


# ---------------------------------------------------------------------------
# Ergebnisdatenklasse
# ---------------------------------------------------------------------------
@dataclass
class PriceRecommendation:
    produkt_id: str
    preiselastizitaet: float
    modell_r2: float
    aktueller_preis: float
    wettbewerbspreis: Optional[float]
    empfohlener_preis: float
    erwartete_mengenänderung: float   # relativ in %, positiv = Steigerung
    erwartete_umsatzaenderung: float  # relativ in %
    erwartete_margenänderung: float   # relativ in %


# ---------------------------------------------------------------------------
# Kernfunktion: Preisempfehlung für ein Produkt
# ---------------------------------------------------------------------------
def recommend_price(
    result: ElasticityResult,
    aktueller_preis: float,
    einstandspreis: float,
    mindestpreis: float,
    wettbewerbspreis: Optional[float] = None,
) -> PriceRecommendation:
    """
    Berechnet den optimalen Empfehlungspreis für ein Produkt.

    Parameters
    ----------
    result           : ElasticityResult des ML-Modells für dieses Produkt
    aktueller_preis  : zuletzt erzielter Preis P₀
    einstandspreis   : Einkaufspreis C (Untergrenze für Margenkalkulation)
    mindestpreis     : absoluter Mindestpreis (konfigurierbarer Grenzwert)
    wettbewerbspreis : aktueller Wettbewerbspreis (optional)
    """
    eps = result.elastizitaet  # Preiselastizität

    # --- Umsatz-maximierender Preis (Amoroso-Robinson-Relation) ---
    # Gültig nur bei elastischer Nachfrage (|ε| > 1).
    # Nahe der Einheitselastizität (ε ≈ -1) divergiert die Formel → Fallback.
    if eps >= 0 or abs(eps) < 1.05:
        # Unelastisch oder nahe Einheitselastizität: Preis moderat anheben
        p_optimal = aktueller_preis * 1.05
    else:
        # Elastische Nachfrage: P* = C / (1 + 1/ε)
        p_optimal = einstandspreis / (1.0 + 1.0 / eps)

    # --- Wettbewerbs-Anpassung ---
    if wettbewerbspreis is not None:
        p_optimal = (
            (1 - WETTBEWERB_GEWICHT) * p_optimal
            + WETTBEWERB_GEWICHT * wettbewerbspreis
        )

    # --- Schranken: Mindestpreis, Mindestmarge und Maximaländerung ---
    p_min_marge = einstandspreis * (1 + MIN_MARGIN_RATE)
    p_max = aktueller_preis * (1 + MAX_PREIS_ÄNDERUNG)
    p_min = max(mindestpreis, p_min_marge, aktueller_preis * (1 - MAX_PREIS_ÄNDERUNG))
    p_empfohlen = float(np.clip(p_optimal, p_min, p_max))
    p_empfohlen = round(p_empfohlen, 2)

    # --- Erwartete Auswirkungen (ceteris paribus) ---
    delta_p = (p_empfohlen - aktueller_preis) / aktueller_preis
    delta_q = eps * delta_p                     # Mengenänderung (log-linear)
    delta_umsatz = (1 + delta_p) * (1 + delta_q) - 1
    # Marge: (Preis - Einstandspreis) * Menge
    marge_alt = aktueller_preis - einstandspreis
    marge_neu = p_empfohlen - einstandspreis
    delta_marge = (marge_neu * (1 + delta_q) - marge_alt) / abs(marge_alt) if marge_alt != 0 else 0.0

    return PriceRecommendation(
        produkt_id=result.produkt_id,
        preiselastizitaet=result.elastizitaet,
        modell_r2=result.r2,
        aktueller_preis=round(aktueller_preis, 2),
        wettbewerbspreis=round(wettbewerbspreis, 2) if wettbewerbspreis else None,
        empfohlener_preis=p_empfohlen,
        erwartete_mengenänderung=round(delta_q * 100, 2),
        erwartete_umsatzaenderung=round(delta_umsatz * 100, 2),
        erwartete_margenänderung=round(delta_marge * 100, 2),
    )


# ---------------------------------------------------------------------------
# Speicherung in dbo.ModelOutput
# ---------------------------------------------------------------------------
def save_recommendations(
    recommendations: List[PriceRecommendation],
    con,
) -> None:
    """Speichert Preisempfehlungen in der Tabelle ModelOutput (SQLite/SQL Server)."""
    rows = []
    for rec in recommendations:
        rows.append({
            "produkt_id":               rec.produkt_id,
            "preiselastizitaet":        rec.preiselastizitaet,
            "modell_r2":                rec.modell_r2,
            "aktueller_preis":          rec.aktueller_preis,
            "wettbewerbspreis":         rec.wettbewerbspreis,
            "empfohlener_preis":        rec.empfohlener_preis,
            "erwartete_mengenänderung": rec.erwartete_mengenänderung,
            "erwartete_umsatzaenderung": rec.erwartete_umsatzaenderung,
            "erwartete_margenänderung":  rec.erwartete_margenänderung,
        })
    df = pd.DataFrame(rows)
    df.to_sql("ModelOutput", con, if_exists="replace", index=False)
    print(f"ModelOutput: {len(df)} Empfehlungen gespeichert.")


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(__file__).replace("src/pricing_optimizer.py", ""))

    from src.data_preparation import load_csv_to_db, build_feature_dataframe, get_connection
    from src.model import train_all_products

    load_csv_to_db()
    df = build_feature_dataframe()
    results = train_all_products(df)

    df_produkte = pd.read_csv(
        str(__file__).replace("src/pricing_optimizer.py", "data/produkte.csv")
    ).set_index("produkt_id")

    df_w = df.groupby("produkt_id")["wettbewerbspreis"].last()

    recs = []
    for pid, res in results.items():
        prod = df_produkte.loc[pid]
        last_price = df.loc[df["produkt_id"] == pid, "preis"].iloc[-1]
        recs.append(
            recommend_price(
                res,
                aktueller_preis=last_price,
                einstandspreis=prod["einstandspreis"],
                mindestpreis=prod["mindestpreis"],
                wettbewerbspreis=df_w.get(pid),
            )
        )

    for r in recs:
        print(
            f"{r.produkt_id}: ε={r.preiselastizitaet:+.3f}  "
            f"P₀={r.aktueller_preis:.2f}€  P*={r.empfohlener_preis:.2f}€  "
            f"ΔU={r.erwartete_umsatzaenderung:+.1f}%  ΔM={r.erwartete_margenänderung:+.1f}%"
        )

    with get_connection() as con:
        save_recommendations(recs, con)
