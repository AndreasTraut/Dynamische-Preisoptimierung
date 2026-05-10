# Model Documentation: Dynamic Price Optimization Model in eCommerce

> **Reference:** *Thesis “Dynamic Price Optimization Model in eCommerce” – Andreas Traut*  
> This documentation follows the chapter structure of the thesis and links  
> each section to the corresponding source code.
>
> 📄 **Thesis as Markdown:** [`docs/STUDIENARBEIT_EN.md`](STUDIENARBEIT_EN.md)  
> 📄 **Original document (Word):** [`Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx`](../Studienarbeit%20Dynamisches%20Preisoptimierungsmodell%20im%20eCommerce-%20Andreas%20Traut.docx)

---

## Table of Contents

1. [System Architecture and Data Flow](#1-system-architecture-and-data-flow)
2. [Data and ETL](#2-data-and-etl)
3. [Feature Engineering](#3-feature-engineering)
4. [ML Model: Price Elasticity](#4-ml-model-price-elasticity)
5. [Concrete Step-by-Step Calculations](#5-concrete-step-by-step-calculations)
6. [Price Recommendation: Prescriptive Analytics](#6-price-recommendation-prescriptive-analytics)
7. [Results and Evaluation](#7-results-and-evaluation)
8. [Deployment: ModelOutput and Reporting](#8-deployment-modeloutput-and-reporting)
9. [CRISP-DM Classification](#9-crisp-dm-classification)
10. [Quick Start](#10-quick-start)

---

## 1. System Architecture and Data Flow

The prototype implements the end-to-end process described in the thesis —  
from synthetic raw data to the final price recommendation in the datamart.

```text
┌─────────────────────────────────────────────────────────────────────────┐
│  Source systems (prototype: synthetic CSV files)                       │
│  data/produkte.csv  ·  data/verkaeufe.csv  ·  data/wettbewerbspreise.csv│
└────────────────────────────┬────────────────────────────────────────────┘
                             │  ETL (simulated SSIS / BULK INSERT)
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  DWH – PricingPrototypeDB (SQLite / SQL Server)                        │
│  Core:    Produkte · Verkaeufe · Wettbewerbspreise                     │
│  Datamart: ModelOutput                                                 │
│  ← sql/create_tables.sql · sql/load_data.sql                           │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/data_preparation.py → build_feature_dataframe()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Feature DataFrame (pandas)                                            │
│  log_preis · monat · preis_relativ_zu_wettbewerb · rolling KPIs …      │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/model.py → train_all_products()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Price elasticity models (ridge regression, one per product)           │
│  Output: ε, R², MAE, RMSE                                              │
└────────────────────────────┬────────────────────────────────────────────┘
                             │  src/pricing_optimizer.py → recommend_price()
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Price recommendations → dbo.ModelOutput                               │
│  P* · ΔRevenue · ΔMargin · ΔQuantity                                   │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
                  notebooks/dynamic_pricing_prototype.ipynb
                  (Dashboard · Price Sensitivity · EDA)
```

**Code entry points:**

| Component | File | Main function |
|---|---|---|
| ETL | [`src/data_preparation.py`](../src/data_preparation.py) | `load_csv_to_db()` |
| Feature Engineering | [`src/data_preparation.py`](../src/data_preparation.py) | `build_feature_dataframe()` |
| ML Model | [`src/model.py`](../src/model.py) | `train_all_products()` |
| Price Recommendation | [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) | `recommend_price()` |
| End-to-end demo | [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb) | — |

---

## 2. Data and ETL

*Thesis chapter 3*

> *“Design of ETL pipelines for data acquisition and integration”*  
> *“Construction and extension of the data warehouse using a layered model (Core, Bizcore, Datamart)”*

### 2.1 Product Master Data

**Source:** [`data/produkte.csv`](../data/produkte.csv)  
**Code:** [`data/generate_data.py`](../data/generate_data.py)

| produkt_id | name | category | unit cost | minimum price | list price |
|---|---|---|---|---|---|
| P001 | Product A | Electronics | 30.00 € | 35.00 € | 59.99 € |
| P002 | Product B | Electronics | 50.00 € | 60.00 € | 99.99 € |
| P003 | Product C | Household | 10.00 € | 14.00 € | 24.99 € |
| P004 | Product D | Household | 15.00 € | 19.00 € | 34.99 € |
| P005 | Product E | Sports | 20.00 € | 25.00 € | 44.99 € |

### 2.2 Sales Data (Historical)

**Source:** [`data/verkaeufe.csv`](../data/verkaeufe.csv) — 1,825 rows (5 products × 365 days)

| produkt_id | Avg. price | Min price | Max price | Avg. qty/day | Annual revenue |
|---|---|---|---|---|---|
| P001 | 58.80 € | 51.07 € | 65.84 € | 54 units | 1,142,918 € |
| P002 | 97.86 € | 85.11 € | 109.97 € | 53 units | 1,865,296 € |
| P003 | 24.31 € | 21.26 € | 27.46 € | 56 units | 490,705 € |
| P004 | 34.00 € | 29.82 € | 38.32 € | 54 units | 659,015 € |
| P005 | 43.90 € | 38.25 € | 49.48 € | 54 units | 853,143 € |

**Data generation logic** (from [`data/generate_data.py`](../data/generate_data.py), lines 46–62):

```python
elasticity = np.random.uniform(-2.5, -0.8)   # true (hidden) elasticity
# Demand: log-linear with price + seasonality + noise
season_effect = 0.15 * np.sin(2 * np.pi * (month - 3) / 12)
log_demand = (
    np.log(50)
    + elasticity * np.log(price / base_price)
    + season_effect
    + np.random.normal(0, 0.15)
)
quantity = max(1, int(np.round(np.exp(log_demand))))
```

The true elasticity is “hidden” inside the data — the model is supposed to estimate it.

### 2.3 ETL Process

**Code:** [`src/data_preparation.py → load_csv_to_db()`](../src/data_preparation.py#L38)

```text
CSV files (data/)  →  pandas.read_csv()  →  df.to_sql()  →  SQLite
                                               (simulates BULK INSERT / SSIS)
```

In the target system (thesis chapter 3.1):
- **Power Query / SSIS** for data extraction from ERP and Pacvue
- **Azure Data Factory** for orchestration of nightly runs
- **SQL Server Developer Edition** instead of SQLite

SQL equivalent: [`sql/create_tables.sql`](../sql/create_tables.sql) · [`sql/load_data.sql`](../sql/load_data.sql)

---

## 3. Feature Engineering

*Thesis chapter 3.3*

> *“Feature engineering using Python (`pandas`, `numpy`) and SQL”*  
> *“Creation of relevant features (e.g. time features, price indices, marketing effects, rolling metrics)”*

**Code:** [`src/data_preparation.py → build_feature_dataframe()`](../src/data_preparation.py#L58)

### Generated Features

| Feature | Calculation | Purpose |
|---|---|---|
| `log_preis` | `ln(price)` | Linearizes the price-quantity relationship for log-log regression |
| `log_menge` | `ln(quantity)` | Target variable (log-transformed) |
| `monat` | `datum.month` | Seasonality (spring peak in the data) |
| `quartal` | `datum.quarter` | Coarse seasonality |
| `ist_wochenende` | `1 if Sat/Sun` | Weekend effect on purchasing behavior |
| `preis_relativ_zu_listenpreis` | `price / list price` | Detects promotional pricing |
| `preis_relativ_zu_wettbewerb` | `price / competitor price` | Competitive positioning |
| `rollierender_umsatz_7d` | 7-day rolling mean | Short-term trend indicator |
| `rollierender_preis_7d` | 7-day rolling mean | Smoothed price indicator |
| `kategorie_code` | Label encoding | Product-group effect |

### Concrete Example (Product P001, First Three Trading Days)

| Date | Price | Quantity | log_preis | log_menge | Month | P/List price | P/Competitor | Rolling price 7d |
|---|---|---|---|---|---|---|---|---|
| 2023-01-01 | 65.25 € | 41 | 4.178 | 3.714 | 1 | 1.088 | 1.000 | 65.25 € |
| 2023-01-02 | 53.33 € | 69 | 3.976 | 4.234 | 1 | 0.889 | 0.821 | 59.29 € |
| 2023-01-03 | 53.33 € | 69 | 3.976 | 4.234 | 1 | 0.889 | 0.821 | 57.30 € |

**Interpretation:** On 2023-01-02 the price was 18% below list price and 18% below  
the competitor price → quantity increased from 41 to 69 units (+68%).

---

## 4. ML Model: Price Elasticity

*Thesis chapter 4*

> *“Selection of suitable modeling approaches – models for estimating price elasticity (e.g. regression models)”*  
> *“Implementation of the models in Python – using libraries (`scikit-learn`, `pandas`, `numpy`)”*

**Code:** [`src/model.py`](../src/model.py)

### 4.1 Theoretical Background

The **log-log linear regression** (also called a **double-log model** or **constant-elasticity model**) models demand as:

$$\log(Q) = \alpha + \varepsilon \cdot \log(P) + \beta_1 x_1 + \ldots + \beta_n x_n + u$$

The coefficient $\varepsilon$ of the log price is directly the **price elasticity of demand**:

$$\varepsilon = \frac{\partial \log Q}{\partial \log P} = \frac{\Delta Q / Q}{\Delta P / P}$$

**Meaning:** If price increases by 1%, quantity changes by $\varepsilon$ percent.  
Typically, $\varepsilon < 0$ (demand falls when price rises).

### 4.2 Implementation

**Code:** [`src/model.py → train_elasticity_model()`](../src/model.py#L61)

```python
pipeline = Pipeline([
    ("scaler", StandardScaler()),   # standardization for numerical stability
    ("ridge",  Ridge(alpha=1.0)),   # ridge regression (L2 regularization)
])
pipeline.fit(X_train, y_train)

# Elasticity: convert the coefficient of log_preis back to the original scale
elastizitaet = ridge.coef_[log_preis_idx] / scaler.scale_[log_preis_idx]
```

**Time-series split** (no random split):  
- 80% of the oldest data → **training set**  
- 20% of the newest data → **test set** (simulation of live operation)

### 4.3 Estimated Model Coefficients (Concrete Values)

Coefficients on the original scale (converted back from ridge coefficient / `StandardScaler`):

**P001 (Electronics “Product A”) – Intercept = 3.997:**

| Feature | Coefficient | Interpretation |
|---|---|---|
| **log_preis** | **−1.182** | **Price elasticity: −1.18** |
| monat | +0.005 | Slight seasonal effect |
| quartal | −0.020 | Opposing quarter effect |
| ist_wochenende | −0.029 | −2.9% less demand on weekends |
| preis_relativ_zu_listenpreis | −0.480 | Discounting has a self-reinforcing effect |
| preis_relativ_zu_wettbewerb | −0.095 | Sensitivity to competitor price |
| rollierender_umsatz_7d | +0.000 | Weak trend effect |
| rollierender_preis_7d | +0.018 | Price smoothing effect |

---

## 5. Concrete Step-by-Step Calculations

This section shows how the model calculates internally — transparently and with real numbers.

### 5.1 Forecast: log(quantity) for P001 on 2023-10-20

**Input values (test set):**
- Price P = 58.97 €  →  log(P) = 4.077
- Month = 10, quarter = 4, weekend = 0
- Price / list price = 58.97 / 59.99 = 0.983
- Price / competitor ≈ 0.97
- Rolling price 7d ≈ 59.12 €

**Model equation for P001 (simplified – main effects):**

```text
log(Q̂) ≈ 3.997
        + (−1.182) × 4.077   [log_preis]
        + (−0.020) × 4       [quartal]
        + (+0.018) × 59.12   [rollierender_preis_7d]
        + ...
       ≈ 3.978

→  Q̂ = e^3.978 ≈ 53 units
```

**Actually sold:** 60 units  →  deviation: 7 units (≈ 12%)

### 5.2 Forecast vs. Actual (Test Set P001, October–December 2023)

| Date | Actual quantity | Predicted quantity | Deviation |
|---|---|---|---|
| 2023-10-20 | 60 | 53 | −12 % |
| 2023-10-21 | 69 | 52 | −25 % |
| 2023-10-22 | 32 | 38 | +19 % |
| 2023-10-23 | 65 | 58 | −11 % |
| 2023-10-24 | 52 | 57 | +10 % |
| 2023-10-25 | 53 | 56 | +6 % |
| 2023-10-26 | 54 | 54 | 0 % |
| 2023-10-27 | 45 | 49 | +9 % |
| 2023-10-28 | 38 | 36 | −5 % |
| 2023-10-29 | 34 | 36 | +6 % |

The model reliably captures the correct order of magnitude; remaining noise is caused by the stochastic demand component.

### 5.3 Interpreting Elasticity with Numerical Examples

**P001, ε = −1.18:**

| Price increase | Expected quantity change | Expected revenue change |
|---|---|---|
| +5 % | −5.9 % | −1.2 % |
| +10 % | −11.8 % | −3.0 % |
| +20 % | −23.6 % | −8.3 % |
| −10 % | +11.8 % | +4.7 % |

**P004, ε = −0.52 (inelastic):**

| Price increase | Expected quantity change | Expected revenue change |
|---|---|---|
| +5 % | −2.6 % | +2.3 % |
| +10 % | −5.2 % | +4.3 % |
| +20 % | −10.5 % | +7.4 % |

> For P004, a price increase is worthwhile because demand reacts only weakly (|ε| < 1).

---

## 6. Price Recommendation: Prescriptive Analytics

*Thesis chapter 4.4*

> *“Derivation of price recommendations from the model results”*  
> *“Conceptual considerations: how can elasticities and forecasts be converted into concrete price suggestions?”*

**Code:** [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py#L62)

### 6.1 Amoroso-Robinson Relation

For **elastic demand** (|ε| > 1.05), the **revenue-maximizing price** is calculated as:

$$P^* = \frac{C}{1 + 1/\varepsilon}$$

Where $C$ = unit cost (marginal cost in the model).

### 6.2 Business Rules (Configurable)

Defined in [`src/pricing_optimizer.py`](../src/pricing_optimizer.py#L37):

```python
MIN_MARGIN_RATE   = 0.10   # minimum margin: 10% on unit cost
WETTBEWERB_GEWICHT = 0.30  # 30% weighting of competitor price
MAX_PREIS_ÄNDERUNG = 0.20  # maximum price change: ±20% per recommendation
```

**Final result:**

```python
p_empfohlen = clip(
    (0.70 × P*_Amoroso) + (0.30 × Wettbewerbspreis),
    min = max(Mindestpreis, C × 1.10, P₀ × 0.80),
    max = P₀ × 1.20
)
```

### 6.3 Concrete Calculation for All Products as of 31.12.2023

**P001 – Electronics “Product A”** (elastic, ε = −1.18):

```text
Unit cost C          =  30.00 €
Current price P₀     =  63.57 €   (last sales day)
Competitor price Pw  =  62.67 €

Amoroso-Robinson:
  P*_AR = 30.00 / (1 + 1/(−1.1825))
        = 30.00 / (1 − 0.8456)
        = 30.00 / 0.1544
        = 194.30 €   ← capped by the ±20% boundary

Competitive adjustment:
  P*_blend = 0.70 × 194.30 + 0.30 × 62.67 = 154.80 €   ← still > P₀ × 1.20

Upper boundary: P₀ × 1.20 = 63.57 × 1.20 = 76.28 €  ← applies!

Recommended price P* = 76.28 €   (+20%)
```

**Impact on KPIs (ceteris paribus):**

```text
ΔP = (76.28 − 63.57) / 63.57 = +20.0%
ΔQ = ε × ΔP = −1.1825 × 0.200 = −23.6%
ΔRevenue = (1 + 0.200) × (1 − 0.236) − 1 = −8.4%
ΔMargin = (76.28 − 30.00) × (1 − 0.236) − (63.57 − 30.00)
         = 46.28 × 0.764 − 33.57
         = 35.36 − 33.57 = +5.3%
```

**P004 – Household “Product D”** (inelastic, ε = −0.52):

```text
Unit cost C          =  15.00 €
Current price P₀     =  30.39 €
Competitor price Pw  =  38.72 €

Inelastic (|ε| < 1.05) → fallback: P* = P₀ × 1.05 = 31.91 €

Competitive adjustment:
  P*_blend = 0.70 × 31.91 + 0.30 × 38.72 = 33.95 €

Boundaries: min=max(19.00; 16.50; 24.31)=24.31 €  max=36.47 € → 33.95 € ✓

Recommended price P* = 33.95 €   (+11.7%)
ΔQuantity = −0.52 × 0.117 = −6.1%
ΔRevenue = +4.9%
ΔMargin  = +15.6%
```

### 6.4 Overall Results for All Products (ModelOutput)

| Product | ε | R² | Current Price | Competitor Price | **Rec. Price** | ΔQuantity | **ΔRevenue** | **ΔMargin** |
|---|---|---|---|---|---|---|---|---|
| P001 | −1.18 | 0.61 | 63.57 € | 62.67 € | **76.28 €** | −23.6 % | **−8.4 %** | **+5.3 %** |
| P002 | −1.05 | 0.42 | 102.71 € | 98.27 € | **104.97 €** | −2.3 % | **−0.2 %** | **+1.9 %** |
| P003 | −1.32 | 0.57 | 24.63 € | 22.99 € | **29.56 €** | −26.4 % | **−11.6 %** | **−1.6 %** |
| P004 | −0.52 | 0.50 | 30.39 € | 38.72 € | **33.95 €** | −6.2 % | **+4.9 %** | **+15.6 %** |
| P005 | −0.66 | 0.44 | 45.37 € | 49.96 € | **48.33 €** | −4.3 % | **+2.0 %** | **+6.9 %** |

> **Strategic interpretation:**  
> - P001 / P003 (elastic): a price increase causes a drop in quantity → margin rises slightly, revenue falls → useful in a margin-optimization strategy  
> - P004 / P005 (inelastic): a price increase clearly pays off → both revenue and margin improve

---

## 7. Results and Evaluation

*Thesis chapter 5*

> *“Technical evaluation of the model results and elasticities”*  
> *“Plausibility check of the calculated elasticities (sign, magnitude)”*

### 7.1 Model Quality Metrics (Test Set, Time-Series Split 80/20)

| Product | R² | MAE | RMSE | Assessment |
|---|---|---|---|---|
| P001 | **0.61** | 0.111 | 0.138 | good |
| P002 | 0.42 | 0.109 | 0.138 | moderate |
| P003 | 0.57 | 0.117 | 0.147 | good |
| P004 | 0.50 | 0.116 | 0.146 | moderate |
| P005 | 0.44 | 0.120 | 0.151 | moderate |

*MAE/RMSE are measured on the log scale → on the quantity scale, MAE ≈ 0.11 means an average  
deviation of approx. e^0.11 − 1 ≈ 12% from actual sales quantity.*

### 7.2 Plausibility Check of the Elasticities

| Criterion | Expected value | Result | ✓/✗ |
|---|---|---|---|
| Sign | negative (law of demand) | all ε < 0 | ✓ |
| Magnitude | typically −0.3 to −3.0 in eCommerce | −0.52 to −1.32 | ✓ |
| Electronics more elastic than household | |ε_electronics| > |ε_household| expected | P001: −1.18 > P004: −0.52 | ✓ |
| Stability check | repeated values with same seed | deterministic due to `SEED=42` | ✓ |

### 7.3 A/B Test Concept

The model can be validated using A/B tests (conceptual only in the prototype):

```text
Group A (control): current price P₀
Group B (test):    recommended price P*
Measurement after 4 weeks:
  ΔRevenue = Revenue_B / Revenue_A − 1
  ΔMargin  = Margin_B  / Margin_A  − 1
If ΔMargin > 0 → the model is rolled out for all products
```

---

## 8. Deployment: ModelOutput and Reporting

*Thesis chapter 6*

> *“Provision of model results (e.g. storage in DWH, provision via API)”*  
> *“Development of Power BI dashboards and reports”*

### 8.1 dbo.ModelOutput

**Code:** [`src/pricing_optimizer.py → save_recommendations()`](../src/pricing_optimizer.py#L131)

The results are written to the `ModelOutput` table (SQLite prototype,  
SQL Server schema in [`sql/create_tables.sql`](../sql/create_tables.sql#L72)):

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

### 8.2 Dashboard (Power BI Prototype)

The notebook [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)
creates visualizations corresponding to the Power BI dashboard:

![Dashboard Preview](../dashboard_preview.png)

**Included report pages:**

| Page | Content | DAX equivalent |
|---|---|---|
| Price comparison | Current vs. recommended by product | `[Empfohlener Preis]` |
| KPI impact | ΔRevenue and ΔMargin by product | `[Erwarteter Umsatzeffekt]` |
| Price Sensitivity | Revenue / margin as a function of price | — |
| EDA | Time series, log price vs. log quantity | — |

---

## 9. CRISP-DM Classification

> *Thesis chapter 1.5: “Cross Industry Standard Process for Data Mining (CRISP-DM)”*

| CRISP-DM phase | Code / artifact | Thesis chapter |
|---|---|---|
| **Business Understanding** | — (problem definition, goals) | Ch. 1.2 |
| **Data Understanding** | [`data/generate_data.py`](../data/generate_data.py), CSV analyses in notebook | Ch. 2 |
| **Data Preparation** | [`src/data_preparation.py`](../src/data_preparation.py) | Ch. 3 |
| **Modeling** | [`src/model.py`](../src/model.py) | Ch. 4.1–4.3 |
| **Evaluation** | Metrics R²/MAE/RMSE, plausibility check | Ch. 5.1 |
| **Deployment** | [`src/pricing_optimizer.py`](../src/pricing_optimizer.py), `ModelOutput`, notebook | Ch. 6 |

---

## 10. Quick Start

### Requirements

```bash
pip install -r requirements.txt
```

### Step 1 – Generate Data

```bash
python data/generate_data.py
```

Creates `data/produkte.csv`, `data/verkaeufe.csv`, and `data/wettbewerbspreise.csv`.

### Step 2 – Run the Pipeline

```bash
# ETL + feature engineering
python -m src.data_preparation

# model training
python -m src.model

# price recommendations + ModelOutput
python -m src.pricing_optimizer
```

### Step 3 – Notebook (End-to-End + Visualizations)

```bash
jupyter notebook notebooks/dynamic_pricing_prototype.ipynb
```

### Expected Console Output

```text
ETL completed: data loaded into PricingPrototypeDB.sqlite.
  P001: ε = -1.183  R² = 0.609  MAE = 0.111
  P002: ε = -1.047  R² = 0.417  MAE = 0.109
  P003: ε = -1.317  R² = 0.570  MAE = 0.117
  P004: ε = -0.525  R² = 0.499  MAE = 0.116
  P005: ε = -0.656  R² = 0.442  MAE = 0.120
ModelOutput: 5 recommendations saved.
```

---

*Last update of the calculations: data from the production run with `SEED=42`,  
sales year 2023, time-series split 80/20.*
