"""
model.py
--------
Schätzung der Preiselastizität und Nachfrageprognose
mittels log-linearer (log-log) Regression.

Theoretischer Hintergrund:
  log(Q) = α + ε * log(P) + β₁*x₁ + … + βₙ*xₙ + u

  Der Koeffizient ε des log-Preises entspricht direkt der
  Preiselastizität der Nachfrage:
      ε = ∂log(Q) / ∂log(P) = (ΔQ/Q) / (ΔP/P)

  Typischerweise gilt ε < 0 (Nachfrage sinkt bei Preisstieg).

Dokumentation:
  docs/MODELL_DOKUMENTATION.md – Kap. 4 (ML-Modell) und Kap. 5 (Konkrete Berechnungen)
  Studienarbeit Kap. 4: „Entwicklung der Machine-Learning-Modelle zur Preisoptimierung"
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------------------
# Ergebnisdatenklasse für ein einzelnes Produkt
# ---------------------------------------------------------------------------
@dataclass
class ElasticityResult:
    produkt_id: str
    elastizitaet: float          # Preiselastizität (negativ bei normalem Gut)
    r2: float                    # Bestimmtheitsmaß Testset
    mae: float                   # Mean Absolute Error (log-Skala)
    rmse: float                  # Root Mean Squared Error (log-Skala)
    modell: Pipeline = field(repr=False)  # trainiertes sklearn-Pipeline-Objekt
    feature_names: list[str] = field(repr=False)


# ---------------------------------------------------------------------------
# Modelltraining je Produkt
# ---------------------------------------------------------------------------
FEATURE_COLS = [
    "log_preis",
    "monat",
    "quartal",
    "ist_wochenende",
    "preis_relativ_zu_listenpreis",
    "preis_relativ_zu_wettbewerb",
    "rollierender_umsatz_7d",
    "rollierender_preis_7d",
    "kategorie_code",
]


def train_elasticity_model(
    df_produkt: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42,
) -> ElasticityResult:
    """
    Trainiert ein log-log-Regressionsmodell für ein einzelnes Produkt.

    Parameters
    ----------
    df_produkt  : DataFrame mit allen Features für genau ein Produkt
    test_size   : Anteil der Testdaten (Hold-out-Split)
    random_state: Zufalls-Seed für Reproduzierbarkeit

    Returns
    -------
    ElasticityResult mit Elastizität und Güte-Metriken
    """
    produkt_id = df_produkt["produkt_id"].iloc[0]

    # Zeitreihen-Split: ältere Daten trainieren, neuere testen
    df_sorted = df_produkt.sort_values("datum")
    split_idx = int(len(df_sorted) * (1 - test_size))
    train = df_sorted.iloc[:split_idx]
    test = df_sorted.iloc[split_idx:]

    X_train = train[FEATURE_COLS].fillna(0)
    y_train = train["log_menge"]
    X_test = test[FEATURE_COLS].fillna(0)
    y_test = test["log_menge"]

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge",  Ridge(alpha=1.0)),
    ])
    pipeline.fit(X_train, y_train)
    y_pred = pipeline.predict(X_test)

    # Elastizität = Koeffizient von log_preis  (vor Skalierung zurückrechnen)
    scaler: StandardScaler = pipeline.named_steps["scaler"]
    ridge: Ridge = pipeline.named_steps["ridge"]
    log_preis_idx = FEATURE_COLS.index("log_preis")
    # Koeffizient im skalierten Raum → auf Originalskala zurückrechnen
    elastizitaet = ridge.coef_[log_preis_idx] / scaler.scale_[log_preis_idx]

    return ElasticityResult(
        produkt_id=produkt_id,
        elastizitaet=round(float(elastizitaet), 4),
        r2=round(r2_score(y_test, y_pred), 4),
        mae=round(mean_absolute_error(y_test, y_pred), 4),
        rmse=round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
        modell=pipeline,
        feature_names=FEATURE_COLS,
    )


def train_all_products(df: pd.DataFrame) -> Dict[str, ElasticityResult]:
    """
    Trainiert je Produkt ein eigenes Elastizitätsmodell.

    Returns
    -------
    Dict  produkt_id -> ElasticityResult
    """
    results: Dict[str, ElasticityResult] = {}
    for pid, grp in df.groupby("produkt_id"):
        result = train_elasticity_model(grp)
        results[pid] = result
        print(
            f"  {pid}: ε = {result.elastizitaet:+.3f}  "
            f"R² = {result.r2:.3f}  MAE = {result.mae:.3f}"
        )
    return results


if __name__ == "__main__":
    from data_preparation import load_csv_to_db, build_feature_dataframe

    load_csv_to_db()
    df = build_feature_dataframe()
    print("Trainiere Elastizitätsmodelle …")
    results = train_all_products(df)
    print("\nFertig.")
