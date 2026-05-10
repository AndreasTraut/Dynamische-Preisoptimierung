# Dynamic Price Optimization Model in eCommerce

Prototype implementation of the machine-learning-based price optimization system
described in the thesis
*“Dynamic Price Optimization Model in eCommerce”* (Andreas Traut).

> 📖 **Detailed model documentation with concrete calculations:**  
> **[docs/MODELL_DOKUMENTATION_EN.md](docs/MODELL_DOKUMENTATION_EN.md)**  
> (formulas, step-by-step calculations, all results with real figures,  
> links to thesis chapters and source code functions)
>
> 📄 **Thesis as Markdown:**  
> **[docs/STUDIENARBEIT_EN.md](docs/STUDIENARBEIT_EN.md)**  
> (complete Markdown conversion of the thesis with links to source code and model documentation)

---

## 👨‍💻 About the Author

**Andreas Traut** is a Senior BI Developer specializing in data warehousing, SQL Server, and the Microsoft BI stack. This project is a private example of how AI-driven development and machine learning can solve real-world challenges in eCommerce pricing.

🔗 [Connect on LinkedIn](https://www.linkedin.com/in/andreas-traut-89340/)

🔗 [Explore additional interesting BI implementations](https://github.com/AndreasTraut)

---

## Table of Contents

- [About the Author](#about-the-author)
- [Actual Model Results (Production Run)](#actual-model-results-production-run)
- [System Overview](#system-overview)
  - [CRISP-DM Phases](#crisp-dm-phases)
- [Directory Structure](#directory-structure)
- [Quick Start](#quick-start)
  - [1. Install Dependencies](#1-install-dependencies)
  - [2. Generate Synthetic Data](#2-generate-synthetic-data)
  - [3. Run the Jupyter Notebook (End-to-End)](#3-run-the-jupyter-notebook-end-to-end)
  - [4. Run Individual Modules](#4-run-individual-modules)
- [Data Model (PricingPrototypeDB)](#data-model-pricingprototypedb)
- [Model – Price Elasticity](#model-price-elasticity)
- [Price Recommendation – Amoroso-Robinson Relation](#price-recommendation-amoroso-robinson-relation)
- [Power BI PBIP – Price Optimization Dashboard](#power-bi-pbip-price-optimization-dashboard)
  - [Tabular Model (`model.bim`)](#tabular-model-modelbim)
  - [Report Pages (IBCS-compliant)](#report-pages-ibcs-compliant)
  - [IBCS Compliance](#ibcs-compliance)
  - [Open the PBIP Project](#open-the-pbip-project)
- [Enhancements (Target System)](#enhancements-target-system)
- [References](#references)

---

## Actual Model Results (Production Run)

```
ETL completed: data loaded into PricingPrototypeDB.sqlite.
  P001: ε = -1.183  R² = 0.609  MAE = 0.111
  P002: ε = -1.047  R² = 0.417  MAE = 0.109
  P003: ε = -1.317  R² = 0.570  MAE = 0.117
  P004: ε = -0.525  R² = 0.499  MAE = 0.116
  P005: ε = -0.656  R² = 0.442  MAE = 0.120
```

**ModelOutput (`dbo.ModelOutput`):**

| Product | ε | R² | Current Price | Competitor Price | Rec. Price | ΔQuantity | ΔRevenue | ΔMargin |
|---|---|---|---|---|---|---|---|---|
| P001 | −1.18 | 0.61 | 63.57 € | 62.67 € | **76.28 €** | −23.6 % | −8.4 % | **+5.3 %** |
| P002 | −1.05 | 0.42 | 102.71 € | 98.27 € | **104.97 €** | −2.3 % | −0.2 % | **+1.9 %** |
| P003 | −1.32 | 0.57 | 24.63 € | 22.99 € | **29.56 €** | −26.4 % | −11.6 % | **−1.6 %** |
| P004 | −0.52 | 0.50 | 30.39 € | 38.72 € | **33.95 €** | −6.2 % | +4.9 % | **+15.6 %** |
| P005 | −0.66 | 0.44 | 45.37 € | 49.96 € | **48.33 €** | −4.3 % | +2.0 % | **+6.9 %** |

**Dashboard Preview:**

![Dashboard](dashboard_preview.png)

---

## System Overview

```
Synthetic CSV data (data/)
        │
        ▼
  SQLite database            ← simulates SQL Server PricingPrototypeDB
  (PricingPrototypeDB.sqlite)
        │
        ▼
  Feature engineering        ← src/data_preparation.py
  (time features, price
   indices, rolling
   metrics)
        │
        ▼
  ML model                   ← src/model.py
  Log-log regression
  (price elasticity ε)
        │
        ▼
  Price recommendation       ← src/pricing_optimizer.py
  (Amoroso-Robinson +
   business rules)
        │
        ▼
  dbo.ModelOutput            ← SQLite / SQL Server
  (result storage)
        │
        ▼
  Dashboard / Power BI       ← notebooks/dynamic_pricing_prototype.ipynb
```

### CRISP-DM Phases

| Phase | Content |
|---|---|
| Business Understanding | Problem statement: limitations of static pricing strategies on Amazon |
| Data Understanding | Data sources: sales, inventory, competitor prices, marketing |
| Data Preparation | ETL simulation, feature engineering (`pandas`/`numpy`) |
| Modeling | Log-log ridge regression to estimate price elasticity |
| Evaluation | R², MAE, RMSE + plausibility check of elasticities |
| Deployment | `dbo.ModelOutput` + notebook dashboard (Power BI prototype) |

---

## Directory Structure

```text
├── data/
│   ├── generate_data.py          # Generate synthetic CSV data
│   ├── produkte.csv              # Product master data (5 products)
│   ├── verkaeufe.csv             # Daily sales data (365 days)
│   └── wettbewerbspreise.csv     # Weekly competitor prices
│
├── powerbi/                      # ← NEW: Power BI PBIP project (IBCS-compliant)
│   ├── Preisoptimierung.pbip     # Project entry point
│   ├── Preisoptimierung.Dataset/
│   │   ├── definition.pbidataset # Dataset metadata
│   │   ├── model.bim             # Tabular model (SSAS-compatible, BIM format)
│   │   └── model.json            # Model documentation as JSON
│   ├── Preisoptimierung.Report/
│   │   ├── definition.pbireport  # Report metadata
│   │   └── report.json           # Report layout (3 pages, IBCS styling)
│   └── screenshots/              # Preview images of the report pages
│       ├── page1_preisoptimierung_dashboard.png
│       ├── page2_umsatz_preisentwicklung.png
│       ├── page3_preisempfehlungs_dashboard.png
│       └── datenmodell_erd.png
│
├── sql/
│   ├── create_tables.sql         # Table structure (SQL Server)
│   └── load_data.sql             # BULK INSERT scripts (SQL Server)
│
├── src/
│   ├── data_preparation.py       # ETL + feature engineering
│   ├── model.py                  # Elasticity model (scikit-learn)
│   └── pricing_optimizer.py      # Price recommendation logic + DB persistence
│
├── notebooks/
│   └── dynamic_pricing_prototype.ipynb  # End-to-end notebook
│
├── docs/
│   ├── DATENMODELL.md            # German data model documentation
│   ├── DATENMODELL_EN.md         # English data model documentation
│   ├── MODELL_DOKUMENTATION.md   # Detailed model documentation (formulas, calculations)
│   ├── MODELL_DOKUMENTATION_EN.md # English model documentation
│   ├── STUDIENARBEIT.md          # Thesis as Markdown (chapter structure, concepts)
│   └── STUDIENARBEIT_EN.md       # English thesis translation as Markdown
│
├── Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx
├── dashboard_preview.png         # Preview: price recommendation dashboard
├── requirements.txt
├── README.md
└── README_EN.md
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Generate Synthetic Data

```bash
python data/generate_data.py
```

### 3. Run the Jupyter Notebook (End-to-End)

```bash
jupyter notebook notebooks/dynamic_pricing_prototype.ipynb
```

The notebook executes all steps:
- ETL: CSV → SQLite database
- Feature engineering
- Model training (price elasticities per product)
- Calculate and save price recommendations
- Dashboard visualizations

### 4. Run Individual Modules

```bash
# ETL + feature engineering
python -m src.data_preparation

# Model training
python -m src.model

# Price recommendations
python -m src.pricing_optimizer
```

---

## Data Model (PricingPrototypeDB)

| Table | Layer | Description |
|---|---|---|
| `dbo.Produkte` | Core | Product master data (including SCD-II fields) |
| `dbo.Verkaeufe` | Core | Daily sales transactions |
| `dbo.Wettbewerbspreise` | Core | Weekly competitor prices |
| `dbo.ModelOutput` | Datamart | ML results and price recommendations |

The prototype uses **SQLite**.  
The scripts in `sql/` are designed for **SQL Server Developer Edition** (local instance)
or **Azure SQL**.

---

## Model – Price Elasticity

Demand is modeled using a **log-log linear regression**:

$$\log(Q) = lpha + arepsilon \cdot \log(P) + eta_1 x_1 + \ldots + eta_n x_n$$

The coefficient $arepsilon$ is directly the **price elasticity of demand**:

$$arepsilon = rac{\partial \log Q}{\partial \log P} = rac{\Delta Q / Q}{\Delta P / P}$$

Typical prototype results:

| Product | Category | ε (estimated) | Type |
|---|---|---|---|
| P001 | Electronics | ≈ −1.2 | elastic |
| P002 | Electronics | ≈ −1.0 | close to unit elasticity |
| P003 | Household | ≈ −1.3 | elastic |
| P004 | Household | ≈ −0.5 | inelastic |
| P005 | Sports | ≈ −0.7 | inelastic |

---

## Price Recommendation – Amoroso-Robinson Relation

For elastic demand (|ε| > 1), the revenue-maximizing price is calculated as:

$$P^* = rac{C}{1 + 1/arepsilon}$$

Additional business rules:
- Maximum price change of **±20%** per recommendation
- **Minimum margin** of 10% on unit cost
- **30% weighting** of the competitor price

---

## Power BI PBIP – Price Optimization Dashboard

The PBIP project (`powerbi/`) contains a complete Power BI Desktop project in
**PBIP format** (Power BI Project) with an SSAS Tabular Model and three report pages.

### Tabular Model (`model.bim`)

The semantic model connects all data layers:

| Table | Layer | Source | Description |
|---|---|---|---|
| `Produkte` | Core / master data | Inline (M query) | 5 products, unit costs, categories |
| `Verkaeufe` | Core / fact data | CSV | 365 days × 5 products, price + revenue |
| `Wettbewerbspreise` | Core / external | CSV | Weekly competitor prices |
| `ModelOutput` | Datamart | Inline (M query) | ML results: ε, R², P*, delta metrics |
| `Datum` | Dimension | DAX `CALENDAR` | Date dimension for 2023 (week, month, quarter) |

**DAX measures (excerpt):**
- `Aktueller Preis Ø` / `Empfohlener Preis Ø` / `Wettbewerbspreis Ø`
- `Preisänderung %` = `DIVIDE([Empfohlener Preis Ø] - [Aktueller Preis Ø], [Aktueller Preis Ø])`
- `ΔMarge % Ø` / `ΔUmsatz % Ø` / `ΔMenge % Ø`
- `Preiselastizität Ø` / `Modell R² Ø` / `Preis-Elastizitäts-Klasse`
- `Gesamtumsatz AC` / `Ø Tagesumsatz`

### Report Pages (IBCS-compliant)

**Page 1: “Price Optimization Dashboard”**
- Black title bar with IBCS legend (AC / PL / Competitor)
- 4 KPI cards: Avg. current price, avg. recommended price, avg. Δmargin, model R²
- Clustered bar chart: price comparison AC vs. PL vs. competitor by product
- Clustered bar chart: expected delta changes (margin / revenue / quantity) by product
- Bar chart: price elasticity ε by product
- Detail table: all `ModelOutput` metrics with IBCS column formatting

**Page 2: “Revenue & Price Development”**
- Filter slicers: product & month
- Time series: daily revenue AC by product (2023)
- Time series: daily selling price AC by product (basis for ε estimation)

**Page 3: “Price Recommendation Dashboard”**
- Black title bar with subtitle (Current vs. Recommended Price | Expected Revenue Change | Expected Margin Change)
- Clustered column chart: current vs. recommended price by product
- Clustered column chart: expected revenue change (%) – positive/negative by product
- Clustered column chart: expected margin change (%) – positive/negative by product

### IBCS Compliance

| IBCS Principle | Implementation |
|---|---|
| Uniform notation | AC = actual value, PL = recommendation (ML model), Δ = deviation |
| Scaling & colors | Black (`#000000`) for AC, dark gray (`#404040`) for PL, green for positive Δ |
| Chart types | Bars only (no pie/donut charts), lines for time series |
| Font | Segoe UI throughout, 10–18 pt |
| Background | White (`#FFFFFF`), no background fill colors |
| Data source transparency | Footer with source note on every page |

### Open the PBIP Project

```bash
# In Power BI Desktop (from version 2.113 / October 2023):
# File → Open → Browse → powerbi/Preisoptimierung.pbip
```

> **Data source configuration:** For the CSV tables (`Verkaeufe`, `Wettbewerbspreise`)
> the parameter `DataPath` in Power BI Desktop must be set to the project's `data/`
> directory (Power Query Editor → Manage Parameters).

---

## Enhancements (Target System)

The following enhancements are planned for the production system:

- **ETL:** SQL Server Integration Services (SSIS) + Azure Data Factory
- **DWH:** Multi-layer architecture (Staging → Cleanse → Core → Bizcore → Datamart)
- **Data sources:** Connection to ERP (SAP), Pacvue API, competitor scraping
- **Models:** Advanced models (XGBoost, Prophet for time series, A/B testing)
- **Frontend:** Power BI Desktop with SSAS Tabular Model (DAX measures)
- **Automation:** Nightly runs via SQL Server Agent / Azure Data Factory

---

## References

- IBCS Association, *International Business Communication Standards (IBCS)*, Version 1.2
- Microsoft Learn, *Data Types (Transact-SQL)*
- Microsoft Learn, *Power BI usage scenarios*
- Python Software Foundation, *The Python Standard Library*, https://docs.python.org/3/library/
- scikit-learn developers, *scikit-learn: Machine Learning in Python – User Guide*, https://scikit-learn.org/stable/user_guide.html
- scikit-learn developers, *sklearn.linear_model.Ridge*, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html
- The pandas development team, *pandas documentation*, https://pandas.pydata.org/docs/
- NumPy developers, *NumPy Documentation*, https://numpy.org/doc/stable/
- Matplotlib development team, *Matplotlib Documentation*, https://matplotlib.org/stable/index.html
- SciPy developers, *SciPy Documentation*, https://docs.scipy.org/doc/scipy/
