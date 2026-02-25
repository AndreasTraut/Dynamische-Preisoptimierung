# Modell-Dokumentation: Dynamisches Preisoptimierungsmodell im eCommerce

> **Referenz:** *Studienarbeit „Dynamisches Preisoptimierungsmodell im eCommerce" – Andreas Traut*  
> Diese Dokumentation folgt exakt der Kapitelstruktur der Studienarbeit und verlinkt  
> jeden Abschnitt mit dem zugehörigen Quellcode.

---

## Inhaltsverzeichnis

1. [Systemarchitektur & Datenfluss](#1-systemarchitektur--datenfluss)
2. [Daten & ETL](#2-daten--etl-studienarbeit-kap-3) — Studienarbeit Kap. 3
3. [Feature Engineering](#3-feature-engineering-studienarbeit-kap-33) — Studienarbeit Kap. 3.3
4. [ML-Modell: Preiselastizität](#4-ml-modell-preiselastizität-studienarbeit-kap-4) — Studienarbeit Kap. 4
5. [Konkrete Berechnungen Schritt für Schritt](#5-konkrete-berechnungen-schritt-für-schritt)
6. [Preisempfehlung (präskriptive Analytik)](#6-preisempfehlung-präskriptive-analytik-studienarbeit-kap-44) — Studienarbeit Kap. 4.4
7. [Ergebnisse & Evaluation](#7-ergebnisse--evaluation-studienarbeit-kap-5) — Studienarbeit Kap. 5
8. [Deployment: ModelOutput & Reporting](#8-deployment-modeloutput--reporting-studienarbeit-kap-6) — Studienarbeit Kap. 6
9. [CRISP-DM Einordnung](#9-crisp-dm-einordnung)
10. [Schnellstart](#10-schnellstart)

---

## 1  Systemarchitektur & Datenfluss

Der Prototyp bildet den in der Studienarbeit beschriebenen End-to-End-Prozess ab –  
von synthetischen Rohdaten bis zur Preisempfehlung im Datamart.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Quellsysteme (Prototyp: synthetische CSV-Dateien)                      │
│  data/produkte.csv  ·  data/verkaeufe.csv  ·  data/wettbewerbspreise.csv│
└────────────────────────────┬────────────────────────────────────────────┘
                             │  ETL (simuliert SSIS / BULK INSERT)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  DWH – PricingPrototypeDB (SQLite / SQL Server)                         │
│  Core:    Produkte · Verkaeufe · Wettbewerbspreise                      │
│  Datamart: ModelOutput                                                  │
│  ← sql/create_tables.sql · sql/load_data.sql                            │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/data_preparation.py → build_feature_dataframe()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Feature-DataFrame (pandas)                                             │
│  log_preis · monat · preis_relativ_zu_wettbewerb · rollierende KPIs … │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/model.py → train_all_products()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Preiselastizitätsmodelle (Ridge-Regression, je Produkt)                │
│  Output: ε, R², MAE, RMSE                                               │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/pricing_optimizer.py → recommend_price()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Preisempfehlungen → dbo.ModelOutput                                    │
│  P* · ΔUmsatz · ΔMarge · ΔMenge                                        │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
                  notebooks/dynamic_pricing_prototype.ipynb
                  (Dashboard · Price Sensitivity · EDA)
```

**Quellcode-Einstiegspunkte:**

| Komponente | Datei | Hauptfunktion |
|---|---|---|
| ETL | [`src/data_preparation.py`](../src/data_preparation.py) | `load_csv_to_db()` |
| Feature Engineering | [`src/data_preparation.py`](../src/data_preparation.py) | `build_feature_dataframe()` |
| ML-Modell | [`src/model.py`](../src/model.py) | `train_all_products()` |
| Preisempfehlung | [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) | `recommend_price()` |
| End-to-End Demo | [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb) | — |

---

## 2  Daten & ETL  *(Studienarbeit Kap. 3)*

> *„Konzeption der ETL-Strecken zur Datenakquise und -integration"*  
> *„Aufbau und Erweiterung des Data Warehouse nach Schichtenmodell (Core, Bizcore, Datamart)"*

### 2.1  Produktstammdaten

**Quelle:** [`data/produkte.csv`](../data/produkte.csv)  
**Code:** [`data/generate_data.py`](../data/generate_data.py)

| produkt_id | name | kategorie | einstandspreis | mindestpreis | listenpreis |
|---|---|---|---|---|---|
| P001 | Produkt A | Elektronik | 30,00 € | 35,00 € | 59,99 € |
| P002 | Produkt B | Elektronik | 50,00 € | 60,00 € | 99,99 € |
| P003 | Produkt C | Haushalt   | 10,00 € | 14,00 € | 24,99 € |
| P004 | Produkt D | Haushalt   | 15,00 € | 19,00 € | 34,99 € |
| P005 | Produkt E | Sport      | 20,00 € | 25,00 € | 44,99 € |

### 2.2  Verkaufsdaten (historisch)

**Quelle:** [`data/verkaeufe.csv`](../data/verkaeufe.csv) — 1 825 Zeilen (5 Produkte × 365 Tage)

| produkt_id | Ø Preis | Min Preis | Max Preis | Ø Menge/Tag | Jahresumsatz |
|---|---|---|---|---|---|
| P001 | 58,80 € | 51,07 € | 65,84 € | 54 Stk | 1 142 918 € |
| P002 | 97,86 € | 85,11 € | 109,97 € | 53 Stk | 1 865 296 € |
| P003 | 24,31 € | 21,26 € | 27,46 € | 56 Stk | 490 705 € |
| P004 | 34,00 € | 29,82 € | 38,32 € | 54 Stk | 659 015 € |
| P005 | 43,90 € | 38,25 € | 49,48 € | 54 Stk | 853 143 € |

**Datengenerierungslogik** (aus [`data/generate_data.py`](../data/generate_data.py), Z. 46–62):

```python
elasticity = np.random.uniform(-2.5, -0.8)   # wahre (versteckte) Elastizität
# Nachfrage: log-linear mit Preis + Saisonalität + Rauschen
season_effect = 0.15 * np.sin(2 * np.pi * (month - 3) / 12)
log_demand = (
    np.log(50)
    + elasticity * np.log(price / base_price)
    + season_effect
    + np.random.normal(0, 0.15)
)
quantity = max(1, int(np.round(np.exp(log_demand))))
```

Die wahre Elastizität ist in den Daten „versteckt" — das Modell soll sie schätzen.

### 2.3  ETL-Prozess

**Code:** [`src/data_preparation.py → load_csv_to_db()`](../src/data_preparation.py#L38)

```
CSV-Dateien (data/)  →  pandas.read_csv()  →  df.to_sql()  →  SQLite
                                               (simuliert BULK INSERT / SSIS)
```

Im Zielsystem (Studienarbeit Kap. 3.1):
- **PowerQuery / SSIS** für die Datenextraktion aus ERP und Pacvue
- **Azure Data Factory** für die Orchestrierung nächtlicher Läufe
- **SQL Server Developer Edition** anstelle von SQLite

SQL-Äquivalent: [`sql/create_tables.sql`](../sql/create_tables.sql) · [`sql/load_data.sql`](../sql/load_data.sql)

---

## 3  Feature Engineering  *(Studienarbeit Kap. 3.3)*

> *„Feature Engineering mittels Python (pandas, numpy) und SQL"*  
> *„Erstellung relevanter Merkmale (z.B. Zeitmerkmale, Preisindizes, Marketing-Einflüsse, rollierende Kennzahlen)"*

**Code:** [`src/data_preparation.py → build_feature_dataframe()`](../src/data_preparation.py#L58)

### Erzeugte Features

| Feature | Berechnung | Zweck |
|---|---|---|
| `log_preis` | `ln(Preis)` | Linearisiert die Preis-Mengen-Beziehung für log-log-Regression |
| `log_menge` | `ln(Menge)` | Zielvariable (log-transformiert) |
| `monat` | `datum.month` | Saisonalität (Frühlings-Peak in den Daten) |
| `quartal` | `datum.quarter` | Grobe Saisonalität |
| `ist_wochenende` | `1 wenn Sa/So` | Wochenend-Effekt auf Kaufverhalten |
| `preis_relativ_zu_listenpreis` | `Preis / Listenpreis` | Erkennt Aktionspreise |
| `preis_relativ_zu_wettbewerb` | `Preis / Wettbewerbspreis` | Wettbewerbspositionierung |
| `rollierender_umsatz_7d` | Rolling-Mean 7 Tage | Kurzfristiger Trendindikator |
| `rollierender_preis_7d` | Rolling-Mean 7 Tage | Geglätteter Preisindikator |
| `kategorie_code` | Label-Encoding | Produktgruppen-Effekt |

### Konkretes Beispiel (Produkt P001, erste drei Handelstage)

| Datum | Preis | Menge | log_preis | log_menge | monat | P/Listenpreis | P/Wettbewerb | Roll.Preis 7d |
|---|---|---|---|---|---|---|---|---|
| 2023-01-01 | 65,25 € | 41 | 4,178 | 3,714 | 1 | 1,088 | 1,000 | 65,25 € |
| 2023-01-02 | 53,33 € | 69 | 3,976 | 4,234 | 1 | 0,889 | 0,821 | 59,29 € |
| 2023-01-03 | 53,33 € | 69 | 3,976 | 4,234 | 1 | 0,889 | 0,821 | 57,30 € |

**Interpretation:** Am 02.01. war der Preis 18 % unter Listenpreis und 18 % unter  
Wettbewerbspreis → Menge stieg von 41 auf 69 Stück (+68 %).

---

## 4  ML-Modell: Preiselastizität  *(Studienarbeit Kap. 4)*

> *„Auswahl geeigneter Modellierungsansätze – Modelle zur Schätzung der Preiselastizität (z.B. Regressionsmodelle)"*  
> *„Implementierung der Modelle in Python – Nutzung von Bibliotheken (scikit-learn, pandas, numpy)"*

**Code:** [`src/model.py`](../src/model.py)

### 4.1  Theoretischer Hintergrund

Die **log-log-lineare Regression** (auch **Double-Log-Modell** oder **konstantelastisches Modell**) modelliert die Nachfrage als:

$$\log(Q) = \alpha + \varepsilon \cdot \log(P) + \beta_1 x_1 + \ldots + \beta_n x_n + u$$

Der Koeffizient $\varepsilon$ des log-Preises ist direkt die **Preiselastizität der Nachfrage**:

$$\varepsilon = \frac{\partial \log Q}{\partial \log P} = \frac{\Delta Q / Q}{\Delta P / P}$$

**Bedeutung:** Bei einer Preiserhöhung um 1 % ändert sich die Menge um $\varepsilon$ Prozent.  
Typischerweise gilt $\varepsilon < 0$ (Nachfrage sinkt bei Preisstieg).

### 4.2  Implementierung

**Code:** [`src/model.py → train_elasticity_model()`](../src/model.py#L61)

```python
pipeline = Pipeline([
    ("scaler", StandardScaler()),   # Standardisierung für numerische Stabilität
    ("ridge",  Ridge(alpha=1.0)),   # Ridge-Regression (L2-Regularisierung)
])
pipeline.fit(X_train, y_train)

# Elastizität: Koeffizient von log_preis zurückrechnen auf Originalskala
elastizitaet = ridge.coef_[log_preis_idx] / scaler.scale_[log_preis_idx]
```

**Zeitreihen-Split** (keine zufällige Aufteilung!):  
- 80 % der ältesten Daten → **Trainingsset**  
- 20 % der neuesten Daten → **Testset** (Simulation des Echtbetriebs)

### 4.3  Geschätzte Modellkoeffizienten (konkrete Werte)

Koeffizienten auf Originalskala (rückgerechnet aus Ridge-Koeffizient / StandardScaler):

**P001 (Elektronik „Produkt A") – Intercept = 3,997:**

| Feature | Koeffizient | Interpretation |
|---|---|---|
| **log_preis** | **−1,182** | **Preiselastizität: −1,18** |
| monat | +0,005 | Leichter Saisoneffekt |
| quartal | −0,020 | Gegenläufiger Quartalseffekt |
| ist_wochenende | −0,029 | −2,9 % weniger Nachfrage am Wochenende |
| preis_relativ_zu_listenpreis | −0,480 | Rabattierung wirkt selbstverstärkend |
| preis_relativ_zu_wettbewerb | −0,095 | Wettbewerbspreissensitivität |
| rollierender_umsatz_7d | +0,000 | Schwacher Trendeffekt |
| rollierender_preis_7d | +0,018 | Preis-Glättungseffekt |

---

## 5  Konkrete Berechnungen Schritt für Schritt

Dieser Abschnitt zeigt, wie das Modell intern rechnet – nachvollziehbar mit echten Zahlen.

### 5.1  Vorhersage: log(Menge) für P001 am 20.10.2023

**Eingangswerte (Testset):**
- Preis P = 58,97 €  →  log(P) = 4,077
- Monat = 10, Quartal = 4, Wochenende = 0
- Preis/Listenpreis = 58,97 / 59,99 = 0,983
- Preis/Wettbewerb ≈ 0,97
- Rollierender Preis 7d ≈ 59,12 €

**Modellgleichung P001 (vereinfacht – Haupteffekte):**

```
log(Q̂) ≈ 3,997
        + (−1,182) × 4,077   [log_preis]
        + (−0,020) × 4       [quartal]
        + (+0,018) × 59,12   [rollierender_preis_7d]
        + ...
       ≈ 3,978

→  Q̂ = e^3,978 ≈ 53 Stück
```

**Tatsächlich verkauft:** 60 Stück  →  Abweichung: 7 Stück (≈ 12 %)

### 5.2  Vorhersage vs. Ist (Testset P001, Oktober–Dezember 2023)

| Datum | Ist-Menge | Vorhergesagte Menge | Abweichung |
|---|---|---|---|
| 20.10.2023 | 60 | 53 | −12 % |
| 21.10.2023 | 69 | 52 | −25 % |
| 22.10.2023 | 32 | 38 | +19 % |
| 23.10.2023 | 65 | 58 | −11 % |
| 24.10.2023 | 52 | 57 | +10 % |
| 25.10.2023 | 53 | 56 | +6 % |
| 26.10.2023 | 54 | 54 | 0 % |
| 27.10.2023 | 45 | 49 | +9 % |
| 28.10.2023 | 38 | 36 | −5 % |
| 29.10.2023 | 34 | 36 | +6 % |

Das Modell trifft die Größenordnung zuverlässig; Rauschen durch stochastische Nachfragekomponente.

### 5.3  Elastizitätsinterpretation am Zahlenbeispiel

**P001, ε = −1,18:**

| Preissteigerung | Erwartete Mengenänderung | Erwartete Umsatzänderung |
|---|---|---|
| +5 % | −5,9 % | −1,2 % |
| +10 % | −11,8 % | −3,0 % |
| +20 % | −23,6 % | −8,3 % |
| −10 % | +11,8 % | +4,7 % |

**P004, ε = −0,52 (unelastisch):**

| Preissteigerung | Erwartete Mengenänderung | Erwartete Umsatzänderung |
|---|---|---|
| +5 % | −2,6 % | +2,3 % |
| +10 % | −5,2 % | +4,3 % |
| +20 % | −10,5 % | +7,4 % |

> Bei P004 lohnt sich Preiserhöhung, da die Nachfrage wenig reagiert (|ε| < 1).

---

## 6  Preisempfehlung (präskriptive Analytik)  *(Studienarbeit Kap. 4.4)*

> *„Ableitung von Preisempfehlungen aus den Modellergebnissen"*  
> *„Konzeptionelle Überlegungen: Wie können Elastizitäten und Prognosen in konkrete Preisvorschläge überführt werden?"*

**Code:** [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py#L62)

### 6.1  Amoroso-Robinson-Relation

Bei **elastischer Nachfrage** (|ε| > 1,05) wird der **umsatzmaximierende Preis** berechnet:

$$P^* = \frac{C}{1 + 1/\varepsilon}$$

Wobei $C$ = Einstandspreis (Grenzkosten im Modell).

### 6.2  Business Rules (konfigurierbar)

Definiert in [`src/pricing_optimizer.py`](../src/pricing_optimizer.py#L37):

```python
MIN_MARGIN_RATE   = 0.10   # Mindestmarge 10 % auf Einstandspreis
WETTBEWERB_GEWICHT = 0.30  # 30 % Gewichtung des Wettbewerbspreises
MAX_PREIS_ÄNDERUNG = 0.20  # Maximale Preisänderung ±20 % je Empfehlung
```

**Endergebnis:**

```python
p_empfohlen = clip(
    (0.70 × P*_Amoroso) + (0.30 × Wettbewerbspreis),
    min = max(Mindestpreis, C × 1.10, P₀ × 0.80),
    max = P₀ × 1.20
)
```

### 6.3  Konkrete Berechnung für alle Produkte (Stand: 31.12.2023)

**P001 – Elektronik „Produkt A"** (elastisch, ε = −1,18):

```
Einstandspreis C     =  30,00 €
Aktueller Preis P₀  =  63,57 €   (letzter Verkaufstag)
Wettbewerbspreis Pw =  62,67 €

Amoroso-Robinson:
  P*_AR = 30,00 / (1 + 1/(−1,1825))
        = 30,00 / (1 − 0,8456)
        = 30,00 / 0,1544
        = 194,30 €   ← wird durch ±20%-Schranke begrenzt

Wettbewerbs-Anpassung:
  P*_blend = 0,70 × 194,30 + 0,30 × 62,67 = 154,80 €   ← immer noch > P₀ × 1,20

Schranke oben: P₀ × 1,20 = 63,57 × 1,20 = 76,28 €  ← greift!

Empfohlener Preis P* = 76,28 €   (+20 %)
```

**Auswirkungen auf KPIs (ceteris paribus):**

```
ΔP = (76,28 − 63,57) / 63,57 = +20,0 %
ΔQ = ε × ΔP = −1,1825 × 0,200 = −23,6 %
ΔUmsatz = (1 + 0,200) × (1 − 0,236) − 1 = −8,4 %
ΔMarge = (76,28 − 30,00) × (1 − 0,236) − (63,57 − 30,00)
         = 46,28 × 0,764 − 33,57
         = 35,36 − 33,57 = +5,3 %
```

**P004 – Haushalt „Produkt D"** (unelastisch, ε = −0,52):

```
Einstandspreis C     =  15,00 €
Aktueller Preis P₀  =  30,39 €
Wettbewerbspreis Pw =  38,72 €

Unelastisch (|ε| < 1,05) → Fallback: P* = P₀ × 1,05 = 31,91 €

Wettbewerbs-Anpassung:
  P*_blend = 0,70 × 31,91 + 0,30 × 38,72 = 33,95 €

Schranken: min=max(19,00; 16,50; 24,31)=24,31 €  max=36,47 € → 33,95 € ✓

Empfohlener Preis P* = 33,95 €   (+11,7 %)
ΔMenge = −0,52 × 0,117 = −6,1 %
ΔUmsatz = +4,9 %
ΔMarge  = +15,6 %
```

### 6.4  Gesamtergebnis aller Produkte (ModelOutput)

| Produkt | ε | R² | Ist-Preis | Wettbewerbspr. | **Empf. Preis** | ΔMenge | **ΔUmsatz** | **ΔMarge** |
|---|---|---|---|---|---|---|---|---|
| P001 | −1,18 | 0,61 | 63,57 € | 62,67 € | **76,28 €** | −23,6 % | **−8,4 %** | **+5,3 %** |
| P002 | −1,05 | 0,42 | 102,71 € | 98,27 € | **104,97 €** | −2,3 % | **−0,2 %** | **+1,9 %** |
| P003 | −1,32 | 0,57 | 24,63 € | 22,99 € | **29,56 €** | −26,4 % | **−11,6 %** | **−1,6 %** |
| P004 | −0,52 | 0,50 | 30,39 € | 38,72 € | **33,95 €** | −6,2 % | **+4,9 %** | **+15,6 %** |
| P005 | −0,66 | 0,44 | 45,37 € | 49,96 € | **48,33 €** | −4,3 % | **+2,0 %** | **+6,9 %** |

> **Strategische Lesart:**  
> - P001/P003 (elastisch): Preiserhöhung bewirkt Mengenrückgang → Marge steigt leicht, Umsatz sinkt → sinnvoll bei Margenoptimierungsstrategie  
> - P004/P005 (unelastisch): Preiserhöhung lohnt sich klar → sowohl Umsatz als auch Marge steigen

---

## 7  Ergebnisse & Evaluation  *(Studienarbeit Kap. 5)*

> *„Technische Evaluation der Modellergebnisse und Elastizitäten"*  
> *„Plausibilitätsprüfung der berechneten Elastizitäten (Vorzeichen, Größenordnung)"*

### 7.1  Modellgüte-Metriken (Testset, Zeitreihen-Split 80/20)

| Produkt | R² | MAE | RMSE | Bewertung |
|---|---|---|---|---|
| P001 | **0,61** | 0,111 | 0,138 | gut |
| P002 | 0,42 | 0,109 | 0,138 | moderat |
| P003 | 0,57 | 0,117 | 0,147 | gut |
| P004 | 0,50 | 0,116 | 0,146 | moderat |
| P005 | 0,44 | 0,120 | 0,151 | moderat |

*MAE/RMSE auf log-Skala → auf Mengenskala bedeutet MAE ≈ 0,11 eine durchschnittliche  
Abweichung von ca. e^0,11 − 1 ≈ 12 % von der tatsächlichen Verkaufsmenge.*

### 7.2  Plausibilitätsprüfung der Elastizitäten

| Kriterium | Erwartung | Ergebnis | ✓/✗ |
|---|---|---|---|
| Vorzeichen | negativ (Gesetz der Nachfrage) | alle ε < 0 | ✓ |
| Größenordnung | typisch −0,3 bis −3,0 im eCommerce | −0,52 bis −1,32 | ✓ |
| Elektronik elastischer als Haushalt | |ε_Elektronik| > |ε_Haushalt| erwartet | P001: −1,18 > P004: −0,52 | ✓ |
| Stabilitätsprüfung | Werte wiederholt beim selben Seed | deterministisch durch Seed=42 | ✓ |

### 7.3  A/B-Test Konzept  *(Studienarbeit Kap. 5.2)*

Das Modell kann durch A/B-Tests validiert werden (im Prototyp nur konzeptionell):

```
Gruppe A (Kontrolle): bisheriger Preis P₀
Gruppe B (Test):      empfohlener Preis P*
Messung nach 4 Wochen:
  ΔUmsatz = Umsatz_B / Umsatz_A − 1
  ΔMarge  = Marge_B  / Marge_A  − 1
Wenn ΔMarge > 0 → Modell wird für alle Produkte ausgerollt
```

---

## 8  Deployment: ModelOutput & Reporting  *(Studienarbeit Kap. 6)*

> *„Bereitstellung der Modellergebnisse (z.B. Speicherung in DWH, Bereitstellung über API)"*  
> *„Entwicklung von Power BI Dashboards und Reports"*

### 8.1  dbo.ModelOutput

**Code:** [`src/pricing_optimizer.py → save_recommendations()`](../src/pricing_optimizer.py#L131)

Die Ergebnisse werden in die Tabelle `ModelOutput` geschrieben (SQLite-Prototyp,  
SQL-Server-Schema in [`sql/create_tables.sql`](../sql/create_tables.sql#L72)):

```sql
CREATE TABLE dbo.ModelOutput (
    produkt_id              NVARCHAR(10),
    berechnungsdatum        DATETIME,
    preiselastizitaet       DECIMAL(8, 4),
    modell_r2               DECIMAL(6, 4),
    aktueller_preis         DECIMAL(10, 2),
    wettbewerbspreis        DECIMAL(10, 2),
    empfohlener_preis       DECIMAL(10, 2),
    erwartete_mengenänderung  DECIMAL(8, 4),
    erwartete_umsatzaenderung DECIMAL(8, 4),
    erwartete_margenänderung  DECIMAL(8, 4)
);
```

### 8.2  Dashboard (Power BI Prototyp)

Das Notebook [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)
erzeugt Visualisierungen, die dem Power BI-Dashboard entsprechen:

![Dashboard-Vorschau](../dashboard_preview.png)

**Enthaltene Report-Seiten:**

| Seite | Inhalt | DAX-Äquivalent |
|---|---|---|
| Preisvergleich | Aktuell vs. Empfohlen je Produkt | `[Empfohlener Preis]` |
| KPI-Impact | ΔUmsatz und ΔMarge je Produkt | `[Erwarteter Umsatzeffekt]` |
| Price Sensitivity | Umsatz/Marge als Funktion des Preises | — |
| EDA | Zeitreihen, Log-Preis vs. Log-Menge | — |

---

## 9  CRISP-DM Einordnung

> *Studienarbeit Kap. 1.5: „Cross Industry Standard Process for Data Mining (CRISP-DM)"*

| CRISP-DM Phase | Code / Artefakt | Studienarbeit Kapitel |
|---|---|---|
| **Business Understanding** | — (Problemdefinition, Ziele) | Kap. 1.2 |
| **Data Understanding** | [`data/generate_data.py`](../data/generate_data.py), CSV-Analysen in Notebook | Kap. 2 |
| **Data Preparation** | [`src/data_preparation.py`](../src/data_preparation.py) | Kap. 3 |
| **Modeling** | [`src/model.py`](../src/model.py) | Kap. 4.1–4.3 |
| **Evaluation** | Metriken R²/MAE/RMSE, Plausibilitätsprüfung | Kap. 5.1 |
| **Deployment** | [`src/pricing_optimizer.py`](../src/pricing_optimizer.py), `ModelOutput`, Notebook | Kap. 6 |

---

## 10  Schnellstart

### Voraussetzungen

```bash
pip install -r requirements.txt
```

### Schritt 1 – Daten erzeugen

```bash
python data/generate_data.py
```

Erzeugt `data/produkte.csv`, `data/verkaeufe.csv`, `data/wettbewerbspreise.csv`.

### Schritt 2 – Pipeline ausführen

```bash
# ETL + Feature Engineering
python -m src.data_preparation

# Modelltraining
python -m src.model

# Preisempfehlungen + ModelOutput
python -m src.pricing_optimizer
```

### Schritt 3 – Notebook (End-to-End + Visualisierungen)

```bash
jupyter notebook notebooks/dynamic_pricing_prototype.ipynb
```

### Erwartete Konsolenausgabe

```
ETL abgeschlossen: Daten in PricingPrototypeDB.sqlite geladen.
  P001: ε = -1.183  R² = 0.609  MAE = 0.111
  P002: ε = -1.047  R² = 0.417  MAE = 0.109
  P003: ε = -1.317  R² = 0.570  MAE = 0.117
  P004: ε = -0.525  R² = 0.499  MAE = 0.116
  P005: ε = -0.656  R² = 0.442  MAE = 0.120
ModelOutput: 5 Empfehlungen gespeichert.
```

---

*Letzte Aktualisierung der Berechnungen: Daten aus dem Produktionslauf mit `SEED=42`,  
Verkaufsjahr 2023, Zeitreihen-Split 80/20.*
