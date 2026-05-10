# DYNAMIC PRICE OPTIMIZATION MODEL IN E-COMMERCE

---

**Thesis**

*Development and implementation of a dynamic price optimization model for the e-commerce assortment using the example of an internationally active market leader*

---

**Author:** Andreas Traut

---

> 📄 **Original document (Word):**  
> [`Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx`](../Studienarbeit%20Dynamisches%20Preisoptimierungsmodell%20im%20eCommerce-%20Andreas%20Traut.docx)
>
> 📖 **Detailed model documentation with concrete calculations and source-code links:**  
> [`docs/MODELL_DOKUMENTATION_EN.md`](MODELL_DOKUMENTATION_EN.md)
>
> 🚀 **Project overview and quick start:**  
> [`README_EN.md`](../README_EN.md)

---

## Table of Contents

1. [Project Abstract](#project-abstract)
2. [Outline](#outline)
3. [1. Introduction](#1-introduction)
   - [1.1 Problem Statement](#11-problem-statement)
   - [1.2 Objective](#12-objective)
   - [1.3 Relevance and Context](#13-relevance-and-context)
   - [1.4 Why This Goes Beyond a Data Analyst Role](#14-why-this-goes-beyond-a-data-analyst-role)
   - [1.5 Theoretical Classification: Predictive and Prescriptive Analytics](#15-theoretical-classification-predictive-and-prescriptive-analytics)
   - [1.6 Cross Industry Standard Process for Data Mining (CRISP-DM)](#16-cross-industry-standard-process-for-data-mining-crisp-dm)
4. [2. Analysis of the Initial Situation and Data Requirements](#2-analysis-of-the-initial-situation-and-data-requirements)
   - [2.1 Existing Pricing Processes and Challenges](#21-existing-pricing-processes-and-challenges)
   - [2.2 Identification and Assessment of Required Data Sources](#22-identification-and-assessment-of-required-data-sources)
   - [2.3 Requirements for Data Quality, Granularity, and Availability](#23-requirements-for-data-quality-granularity-and-availability)
5. [3. Data Integration and Preparation for Price Modeling](#3-data-integration-and-preparation-for-price-modeling)
   - [3.1 ETL Design for Data Acquisition and Integration](#31-etl-design-for-data-acquisition-and-integration)
   - [3.2 Building and Extending the Data Warehouse Layer Model for Pricing Data](#32-building-and-extending-the-data-warehouse-layer-model-for-pricing-data)
   - [3.3 Feature Engineering with Python and SQL](#33-feature-engineering-with-python-and-sql)
6. [4. Development of the Machine Learning Models for Price Optimization](#4-development-of-the-machine-learning-models-for-price-optimization)
   - [4.1 Selecting Suitable Modeling Approaches](#41-selecting-suitable-modeling-approaches)
   - [4.2 Implementing the Models in Python](#42-implementing-the-models-in-python)
   - [4.3 Training, Validation, and Model Selection](#43-training-validation-and-model-selection)
   - [4.4 Deriving Price Recommendations from Model Results](#44-deriving-price-recommendations-from-model-results)
7. [5. Evaluation and Validation of the Pricing Strategy](#5-evaluation-and-validation-of-the-pricing-strategy)
   - [5.1 Technical Evaluation of the Model Results and Elasticities](#51-technical-evaluation-of-the-model-results-and-elasticities)
   - [5.2 Design and Simulation of A/B Tests in an E-Commerce Context](#52-design-and-simulation-of-ab-tests-in-an-e-commerce-context)
   - [5.3 Assessing the Impact on Business Goals (Revenue, Margin)](#53-assessing-the-impact-on-business-goals-revenue-margin)
   - [5.4 Iterative Improvement of the Models Based on Evaluation Results](#54-iterative-improvement-of-the-models-based-on-evaluation-results)
8. [6. Operationalization and Monitoring in the BI System](#6-operationalization-and-monitoring-in-the-bi-system)
   - [6.1 Provision of Model Results](#61-provision-of-model-results)
   - [6.2 Building an Analytical Data Model (Tabular Model in SSAS) for the Front End](#62-building-an-analytical-data-model-tabular-model-in-ssas-for-the-front-end)
   - [6.3 Development of Power BI Dashboards and Reports](#63-development-of-power-bi-dashboards-and-reports)
   - [6.4 Considerations for Automating the End-to-End Process](#64-considerations-for-automating-the-end-to-end-process)
9. [7. Summary and Results](#7-summary-and-results)
   - [7.1 Presentation of the Developed System](#71-presentation-of-the-developed-system)
   - [7.2 Summary of the Key Results](#72-summary-of-the-key-results)
   - [7.3 Contribution to Data-Driven Decision-Making and Strategic Goals](#73-contribution-to-data-driven-decision-making-and-strategic-goals)
   - [7.4 Outlook on Future Enhancements and Limitations](#74-outlook-on-future-enhancements-and-limitations)
10. [List of Figures](#list-of-figures)
11. [References](#references)

---

## Project Abstract

In a highly dynamic e-commerce environment, especially on platforms such as Amazon, an agile and data-driven pricing strategy is essential for maximizing revenue and margin while maintaining competitiveness. Static pricing models or manual adjustments often fail to keep pace with rapid market changes, competitive actions, and demand fluctuations. To unlock the full potential of the e-commerce business of an internationally active mid-sized market leader, this thesis examines the design, development, and implementation of a machine-learning-based system for dynamic price optimization. The goal is to automatically generate price recommendations that incorporate product-level price elasticities and contribute to improving KPIs such as revenue (turnover) and net margin.

The core challenge lies in integrating and processing heterogeneous data sources as well as in the complexity of the underlying models. Relevant inputs include sales data, inventory information, competitor prices (e.g. via APIs or scraping), marketing activity data (e.g. from Pacvue), and potentially external market data. Using robust ETL processes — including Power Query and SQL Server Integration Services (SSIS) — these data sources must be loaded into the existing data warehouse and prepared according to a layered architecture (Core, Bizcore, Datamart). High data quality is essential, for example through reconciliation between Pacvue and internal data.

At the heart of the project is the development of machine-learning models for calculating price elasticities and predicting optimal price points. Python with libraries such as `scikit-learn`, `pandas`, and `numpy` is used for this purpose. Different algorithms (e.g. regression models and time-series analyses) are evaluated and trained on historical data. The model results must then be validated, for example by A/B testing methodologies in an e-commerce context.

Another focus is the operationalization of the results and the enablement of the Amazon team as well as controlling. The price recommendations must either be integrated directly into systems or made available through meaningful dashboards. To achieve this, interactive Power BI reporting is built on top of suitable Tabular Models in SQL Server Analysis Services (SSAS). Through intensive use of DAX calculations, these visualizations enable not only monitoring of the pricing strategy and its effects on turnover and net margin, but also analysis of model quality and sensitivity to different influencing factors (e.g. price sensitivity analyses). SQL expertise (T-SQL, stored procedures, views) is indispensable for data preparation and provisioning in the backend.

This thesis goes beyond pure data analysis (“data analyst” role) by using predictive and prescriptive analytics (see [Section 1.5](#15-theoretical-classification-predictive-and-prescriptive-analytics)) to actively influence business steering. It demonstrates the construction of a complex data-science solution from data integration to model development, operational implementation, and monitoring through modern BI tools. The result is an intelligent price optimization system that elevates decision-making in e-commerce to a new level and makes a measurable contribution toward achieving the strategic goals of an internationally active mid-sized market leader.

---

## Outline

1. **Introduction** (1 page)
   - Problem statement: limitations of static pricing strategies in a dynamic e-commerce environment (especially Amazon)
   - Objective: maximize revenue (turnover) and margin (net margin) through an ML-based price optimization system
   - Relevance and context for an internationally active mid-sized market leader
   - Theoretical classification: predictive and prescriptive analytics in the project context
   - Cross Industry Standard Process for Data Mining (CRISP-DM)

2. **Analysis of the initial situation and data requirements** (approx. 1.5 pages) *[Business Understanding / Data Understanding]*
   - Existing pricing processes and challenges in the e-commerce team (especially Amazon)
   - Identification and assessment of required data sources
     - Internal data (sales, inventory, product data, ERP data)
     - External data (competitor prices, marketing-platform data such as Pacvue, market data)
   - Requirements for data quality, granularity, and availability

3. **Data integration and preparation for price modeling** (approx. 2.5 pages) *[Data Understanding / Data Preparation]*
   - Design of ETL pipelines for data acquisition and integration
     - Use of Power Query and SQL Server Integration Services (SSIS)
     - Integration of APIs or scraping solutions (for competitor data)
   - Building and extending the data warehouse layered model (Core, Bizcore, Datamart) for pricing data
     - Backend data modeling (SQL)
     - Measures to ensure data quality (e.g. reconciliation of Pacvue vs. internal data)
   - Feature engineering with Python (`pandas`, `numpy`) and SQL
     - Creation of relevant features (e.g. time features, price indices, marketing effects, rolling metrics)
     - Data transformations for modeling purposes (e.g. log transformation)

4. **Development of the machine-learning models for price optimization** (approx. 3–4 pages) *[Modeling]*
   - Selecting suitable modeling approaches
     - Models for estimating price elasticity (e.g. regression models)
     - Models for demand forecasting (e.g. time-series analysis, additional regression models)
   - Implementing the models in Python
     - Use of libraries (`scikit-learn`, `pandas`, `numpy`, etc.)
     - Handling product- or category-specific differences
   - Training, validation, and model selection
     - Splitting into training, validation, and test data
     - Metrics for assessing model quality
   - Deriving price recommendations from the model results

5. **Evaluation and validation of the pricing strategy** (approx. 2 pages) *[Evaluation]*
   - Technical evaluation of the model results and elasticities
   - Design and simulation of A/B tests in an e-commerce context
   - Assessing the impact on business goals (revenue, margin)
   - Iterative improvement of the models based on evaluation results

6. **Operationalization and monitoring in the BI system** (approx. 3 pages) *[Deployment]*
   - Provision of model results (e.g. storage in DWH, provision via API)
   - Building an analytical data model (Tabular Model in SSAS) for the front end
     - Definition of dimensions, facts, and hierarchies for pricing analyses
     - Implementation of relevant KPIs using DAX (turnover, net margin, price sensitivity indicators)
   - Development of Power BI dashboards and reports
     - Visualization of price recommendations and their influencing factors
     - Monitoring price development and model performance
     - Provision of analysis tools for the Amazon team and controlling
   - Considerations for automating the end-to-end process (data refresh, model retraining, reporting)

7. **Summary and results** (approx. 1 page) *[Evaluation / Deployment Context]*
   - Presentation of the developed dynamic price optimization system
   - Summary of the key results (e.g. estimated elasticities, system performance)
   - Contribution to data-driven decision-making and strategic goals
   - Outlook on future enhancements and limitations

---

## 1. Introduction

### 1.1 Problem Statement

E-commerce, especially on dominant platforms such as Amazon, is characterized by extraordinary dynamism. Competitor prices change frequently, customer reactions are immediately visible, marketing campaigns affect demand, and the product portfolio changes continuously. This high volatility and complexity require companies to maintain a highly agile pricing strategy in order to remain competitive and to exploit profit potential effectively.

Traditional pricing strategies based on static price lists, periodic manual adjustments, or simple rule-based approaches are increasingly inadequate in this environment. Their main limitations are:

- **Response speed:** Manual processes or lengthy coordination rounds are too slow to react quickly to short-term market changes or competitor actions. Opportunities to increase revenue or optimize margin remain unused, or companies react too late to aggressive undercutting.

- **Complexity and scalability:** The number of products (SKUs), relevant competitors, and demand drivers (seasonality, marketing, inventory, customer reviews, etc.) is often very high. Considering all of these factors manually for each product is hardly feasible and highly error-prone.

- **Use of data:** The abundance of available data from sales transactions, web tracking, marketing platforms (such as Pacvue), and competitor monitoring is not used at all or only insufficiently in static approaches. Valuable insights into price sensitivity and demand patterns remain hidden.

- **Suboptimality:** Without systematic analysis of price elasticity and demand effects, manual or purely cost-based pricing decisions often produce suboptimal results — either potential margins are left unrealized or sales potential is not captured because prices are too high.

These shortcomings mean that companies relying on static pricing strategies systematically underperform in a dynamic e-commerce environment and expose themselves to unnecessary competitive pressure.

> 📖 *Concrete figures illustrating the problems of static pricing strategies and their effects can be found in the model results: [MODELL_DOKUMENTATION_EN.md → Section 7](MODELL_DOKUMENTATION_EN.md#7-results-and-evaluation)*

---

### 1.2 Objective

Given the limitations of static approaches described in [Section 1.1](#11-problem-statement), the primary business objective pursued by implementing a dynamic price optimization system is to maximize revenue (turnover) and net margin in the e-commerce business. The aim is to make a measurable contribution to profitability and business volume through more intelligent pricing.

To achieve this higher-level business goal, this thesis pursues the specific technical and conceptual objective of designing and prototypically implementing a machine-learning-based system for dynamic price optimization. This system is intended to generate data-driven and automated price recommendations for products in the e-commerce assortment.

The core capabilities of this system are:

- **Estimating price elasticities:** ML models are used to calculate price sensitivities for individual products or product groups based on historical sales, price, marketing, and competitive data. *(Prototype: [`src/model.py`](../src/model.py))*

- **Forecasting demand:** The models learn how price changes — while accounting for other relevant factors such as seasonality or marketing activities — affect the quantity sold. *(Prototype: [`src/model.py → train_elasticity_model()`](../src/model.py))*

- **Deriving automated price recommendations:** Based on the estimated elasticities, demand forecasts, and definable business rules (e.g. minimum margins, price ceilings, competitive orientation), the system generates concrete optimized price proposals. *(Prototype: [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py))*

The prototype implementation presented in this thesis serves to demonstrate technical feasibility, validate the methodology, and make the potential value of such a system tangible. It lays the foundation for later full-scale implementation in the company’s production environment.

> 📖 *Concrete results of the prototype implementation: [MODELL_DOKUMENTATION_EN.md → Section 6.4](MODELL_DOKUMENTATION_EN.md#64-overall-results-for-all-products-modeloutput)*

---

### 1.3 Relevance and Context

The problem statement around static pricing and the objective of developing a dynamic, machine-learning-based price optimization system have high strategic relevance for an internationally active mid-sized market leader. As an established company in multiple product segments, this organization operates in a market environment increasingly shaped by online retail and especially by large platforms such as Amazon. In order not only to survive in this highly dynamic setting but also to unlock growth potential and secure long-term competitiveness, advanced data-driven approaches are indispensable.

Implementing an intelligent price optimization system such as the one designed and prototypically implemented in this thesis offers concrete advantages:

**Maximization of revenue and margin:** The core purpose of the system is to positively influence central business KPIs such as revenue (turnover) and net margin. By taking price elasticities and demand patterns at product level into account, prices can be adjusted so that they either maximize sales volume or improve profitability depending on the market situation and product lifecycle.

**Improved competitiveness:** In e-commerce, especially on platforms with high price transparency such as Amazon, the ability to respond quickly and soundly to competitor actions and market changes is decisive. An automated system enables a faster and more effective response than manual or static pricing processes and therefore helps protect or expand market share.

**Higher efficiency and better use of resources:** Automating price determination reduces manual effort in the e-commerce team (especially the Amazon team) and frees up resources for more strategic tasks.

**Promotion of a data-driven decision culture:** The development and use of such a system foster the understanding and application of analytics within the company. It provides not only price recommendations but also valuable insights into customer behavior (e.g. price sensitivity), which are useful for marketing, product management, and controlling. The project therefore elevates decision-making in e-commerce to a new level.

---

### 1.4 Why This Goes Beyond a Data Analyst Role

The design and prototypical implementation of this price optimization system also serves as a concrete justification for the need to establish a dedicated data-science environment. The complexity of the undertaking — from integrating heterogeneous data sources to sophisticated modeling of price elasticities using machine learning and finally to operationalization and visualization in a BI system — clearly exceeds the scope of traditional data analyst roles.

The project requires the following competencies:

- **Machine learning:** Practical experience in building ML models (e.g. with Python and libraries such as `scikit-learn`) to solve specific business problems such as price optimization and elasticity estimation.

- **Data management and modeling:** Deep knowledge of ETL processes (Power Query, SSIS), SQL, DWH layer models, and analytical data modeling (SSAS Tabular) in order to provide a robust data foundation.

- **Business intelligence:** Comprehensive experience with visualization tools such as Power BI and DAX to create meaningful dashboards and reports for business users such as the Amazon team and controlling.

- **E-commerce understanding:** Strong understanding of the specific processes and KPIs relevant in e-commerce.

This project can be clearly distinguished from a classic data analyst task for the following reasons:

- **Complexity:** It requires not only reports, but the development of predictive models and optimization algorithms.

- **Technologies:** It explicitly uses advanced tools and methods (Python/`scikit-learn` for ML, SSAS for complex models, SSIS for ETL) that go beyond typical analyst tooling.

- **Focus:** The emphasis lies on predictive (“What will happen?”) and prescriptive (“What should be done?”) analytics rather than primarily descriptive (“What happened?”) analytics.

- **Automation and system design:** The objective is to build an automated system, not merely ad hoc analyses or manual reports. This includes aspects of data engineering and software development (model deployment).

- **Statistical depth:** The work requires a deep understanding of statistical methods and machine-learning concepts (price elasticity, model validation, A/B testing).

The project therefore acts as a “lighthouse project” that exemplifies both the need for and the immediate value of a dedicated data-science setup in the important growth field of e-commerce. It demonstrates how advanced analytics (predictive and prescriptive) can optimize operational processes and support strategic decision-making well beyond the specific project topic of dynamic price optimization in e-commerce.

---

### 1.5 Theoretical Classification: Predictive and Prescriptive Analytics

Using **predictive analytics** in this project means applying machine-learning models to forecast future outcomes — for example how sales quantity will change after a price adjustment (estimation of price elasticity) or how high demand may be in the next period. It answers the question: *“What is likely to happen?”*

**Prescriptive analytics** goes one decisive step further and forms the core of this price optimization project. It uses the results of the predictive models (e.g. elasticity) together with defined business objectives (such as maximizing revenue or margin) and constraints (such as competitor prices) to derive concrete action recommendations — in this case, optimal price proposals. It answers the question: *“What should we do to achieve our objective?”* By linking these two levels, the developed system actively intervenes in business steering.

*(Prototype implementation: [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) — see [MODELL_DOKUMENTATION_EN.md Section 6](MODELL_DOKUMENTATION_EN.md#6-price-recommendation-prescriptive-analytics))*

These advanced analysis levels build on more fundamental levels that are also relevant for business understanding:

**Descriptive analytics** summarizes and visualizes past events in order to provide an overview of business development. A typical example would be a self-service BI system in Power BI that transparently provides sales, product management, and controlling with KPIs such as revenue, contribution margin, or units sold for different products and customers. It answers the question: *“What happened?”*

**Diagnostic analytics** builds on descriptive analysis and seeks to understand the causes of observed outcomes. Users of the above Power BI system could, for example, investigate via drill-downs, filters, or comparative analyses why the contribution margin of a product group declined or which factors led to revenue growth in specific customer segments. It answers the question: *“Why did it happen?”*

While descriptive and diagnostic analyses are essential for general business understanding and contextualization, the clear focus of this thesis is the development of predictive models and, in particular, prescriptive recommendations in order to optimize pricing proactively and in a data-driven way.

---

### 1.6 Cross Industry Standard Process for Data Mining (CRISP-DM)

The Cross Industry Standard Process for Data Mining (CRISP-DM) is a standard for data-analysis processes that provides a structured framework for conducting data-mining projects. It enables an iterative approach and allows movement between different phases.

*Figure 1-1: Cross Industry Standard Process for Data Mining (CRISP-DM), source: Wikipedia, CC BY-SA 3.0*

The six phases can be summarized as follows:

- **Business Understanding:** Requirements and goal definition are determined, and the business problem is described.
- **Data Understanding:** This phase includes data collection, data description, and examining and evaluating the data.
- **Data Preparation:** In this phase, the data are cleaned and transformed into a target format.
- **Modeling:** The modeling phase deals with modeling procedures. In this thesis, it refers to the method used to build the predictive data model.
- **Evaluation:** During this phase, the implementations and processes are assessed.
- **Deployment:** This phase describes the transfer of the implementation from the development environment to the production environment.

After each chapter, the corresponding classification within the CRISP-DM framework is discussed.

> 📖 *Classification of the prototype within CRISP-DM: [MODELL_DOKUMENTATION_EN.md → Section 9](MODELL_DOKUMENTATION_EN.md#9-crisp-dm-classification)*

---

## 2. Analysis of the Initial Situation and Data Requirements

*[Business Understanding / Data Understanding]*

### 2.1 Existing Pricing Processes and Challenges

At an internationally active mid-sized market leader in e-commerce, pricing processes are typically carried out manually or on the basis of heuristic rule sets. Responsible members of the Amazon team often maintain prices based on experience, occasional competitor observations, and internal minimum-margin guidelines — a process that is neither systematic nor scalable. Platform tools such as Pacvue can automate parts of bid management, but they do not replace a data-driven and dynamic pricing logic.

The resulting challenges are diverse: maintaining prices for a broad product portfolio requires significant human effort. At the same time, inconsistencies arise when different employees use different criteria or when price adjustments are not made quickly enough. Missed optimization opportunities are the consequence: price-increase potential for inelastic products remains unused, while prices that are too high in highly elastic product groups lead to lost market share. The transition to a data-driven, model-based price optimization system is therefore not only desirable but strategically necessary.

---

### 2.2 Identification and Assessment of Required Data Sources

#### 2.2.1 Internal Data (Sales, Inventory, Product Data, ERP Data)

A high-performing price optimization model first requires extensive internal data pools. These include historical sales data (quantity, price, date) at item level, inventory information, product master data (product name, category, unit cost), and ERP data on cost structures and lead times. In real systems, these data usually reside in multiple source systems — for example SAP for ERP and a dedicated e-commerce platform — and must be integrated into the data warehouse via defined ETL processes.

Within the prototype developed for this thesis, the internal data were simulated using synthetic CSV datasets. The file [`data/produkte.csv`](../data/produkte.csv) contains product master data with product ID, description, category, and unit cost; the file [`data/verkaeufe.csv`](../data/verkaeufe.csv) represents historical daily sales including date, product ID, quantity sold, and realized selling price. These synthetic data were generated by the Python script [`data/generate_data.py`](../data/generate_data.py), which creates realistic price-quantity relationships with a controllable random component.

> 📂 *Prototype data: [`data/produkte.csv`](../data/produkte.csv), [`data/verkaeufe.csv`](../data/verkaeufe.csv)*  
> 📄 *Data generation: [`data/generate_data.py`](../data/generate_data.py)*  
> 📖 *Details: [MODELL_DOKUMENTATION_EN.md → Section 2.1](MODELL_DOKUMENTATION_EN.md#21-product-master-data)*

#### 2.2.2 External Data (Competitor Prices, Marketing Platform Data such as Pacvue, Market Data)

In addition to internal data, external data sources are indispensable for competitive pricing. The most important sources include competitor prices on Amazon and other relevant marketplaces, data from marketing platforms such as Pacvue (e.g. click-through rates, advertising costs, organic ranking positions), and higher-level market data about demand trends and seasonality. These data can be obtained through official APIs (e.g. the Amazon Selling Partner API), specialized providers, or — where legally and technically permissible — controlled web-scraping solutions. Their integration into the data warehouse requires reliable ETL pipelines that ensure regular refreshes.

In the prototype, external data are represented by the synthetic file [`data/wettbewerbspreise.csv`](../data/wettbewerbspreise.csv). It contains one simulated competitor price per observation date and product, generated as a slightly varying reference value around the company’s own list price. This simplification makes it possible to model the conceptual integration of external pricing data without depending on real third-party systems.

> 📂 *Prototype data: [`data/wettbewerbspreise.csv`](../data/wettbewerbspreise.csv)*

---

### 2.3 Requirements for Data Quality, Granularity, and Availability

The quality, granularity, and temporal availability of input data are decisive success factors for any data-driven price optimization model. With respect to data quality, consistent reconciliation between internal sales data and external platform data (e.g. Pacvue reporting versus Amazon Vendor Central) is particularly important, because discrepancies can lead to incorrect elasticity estimates. It is therefore advisable to incorporate systematic validation steps directly into the ETL process in order to identify and log inconsistencies.

Regarding granularity, a daily item-level data basis has proven appropriate for operational price optimization systems. This level of detail makes it possible to capture short-term price effects and seasonal patterns reliably without overloading the process with overly fine-grained intraday fluctuations. For operational use, timely data availability is also required: ideally, the previous day’s data are fully consolidated and available at a defined point in time on the following day so that current price recommendations can be generated.

Within the prototype, data quality and availability were simplistically assumed to be given due to the use of synthetic datasets. The generated CSV files are consistent, complete, and available at the required daily granularity, allowing the focus of the prototype to remain on modeling methodology rather than data cleansing.

---

## 3. Data Integration and Preparation for Price Modeling

*[Data Understanding / Data Preparation]*

### 3.1 ETL Design for Data Acquisition and Integration

#### 3.1.1 Use of Power Query and SQL Server Integration Services (SSIS)

In the target system, ETL pipelines for internal data are planned as a combination of **Power Query** and **SQL Server Integration Services (SSIS)**. Power Query is especially suitable for exploratory transformations and the quick connection of heterogeneous source formats (Excel, CSV, OData), while SSIS serves as a production-grade tool for automated, monitored, and schedulable execution of complex data pipelines. SSIS packages enable a structured sequence of extraction, transformation, and loading steps, including error handling and logging, as required for reliable operation in a data warehouse.

#### 3.1.2 API or Scraping Integration for Competitive Data

For acquiring external competitive data, the target system foresees API connections or scraping solutions. Official interfaces such as the Amazon Selling Partner API provide structured data at defined intervals and are preferred because they are more reliable and legally less problematic than scraping. Where no official APIs are available, controlled scraping solutions can be used, integrated either into SSIS pipelines or into standalone Python services.

In the prototype, the ETL pipeline was implemented in a significantly simplified form. Loading the synthetic CSV data into the Python processing layer was performed directly via `pandas` (`load_csv_to_db()` in [`src/data_preparation.py`](../src/data_preparation.py)). In addition, Power Query transformations within Power BI Desktop were used to prepare the data for the reporting model. The prepared data were then loaded into the local SQL Server Developer Edition database. SSIS was deliberately not used in the prototype; it is intended for the target system and described conceptually in [Section 3.1.1](#311-use-of-power-query-and-sql-server-integration-services-ssis).

> 🐍 *Prototype code: [`src/data_preparation.py → load_csv_to_db()`](../src/data_preparation.py)*  
> ��️ *SQL scripts: [`sql/create_tables.sql`](../sql/create_tables.sql) · [`sql/load_data.sql`](../sql/load_data.sql)*  
> 📖 *Details: [MODELL_DOKUMENTATION_EN.md → Section 2.3](MODELL_DOKUMENTATION_EN.md#23-etl-process)*

---

### 3.2 Building and Extending the Data Warehouse Layer Model for Pricing Data

#### 3.2.1 Backend Data Modeling (SQL)

A robust and well-structured data warehouse (DWH) is a central building block for advanced analytics such as dynamic price optimization. It serves as the central hub for integrating data from different source systems, storing them long-term, and preparing them for analytical use. Unlike transactional source systems (OLTP), such as ERP systems, which are optimized for fast read/write access to individual records, DWH systems are designed for complex queries and analyses across large data volumes.

For the data warehouse — based on a Microsoft Azure cloud SQL database — an established multi-layer architecture is used. This structure improves traceability, maintainability, and flexibility. The data flow follows an ELT process (Extract-Load-Transform), in which data are first extracted, then loaded into the DWH, and only transformed there. The most important layers are:

- **Staging layer:** The first landing zone for data from source systems (e.g. ERP). Raw data are stored unchanged.
- **Cleanse layer:** Initial data cleansing and validation take place here. Erroneous or incomplete data are identified and treated. Techniques such as lookup-based foreign-key resolution and error logging are used here, often controlled by SSIS pipelines.
- **Core layer:** This layer forms the foundation of the DWH. Cleaned data from multiple sources are integrated and stored in a stable, consistent model. One major task is historization of data changes, typically according to Slowly Changing Dimensions Type 2 (SCD II). Validity ranges and statuses are maintained so that changes can be traced. This is often implemented through stored procedures in the SQL database. Relationships between data are also defined here via primary and foreign keys.
- **Bizcore layer (Business Core):** This layer contains the actual business logic. Data from different upstream systems are unified into one business view (e.g. a consolidated customer master) and application-specific calculations are performed. For example, contribution margins can be calculated by referencing historized cost components from the Core layer. Transformations in this layer are also often implemented through stored procedures.
- **Datamart layer:** The top layer provides specific data views for defined use cases or user groups (e.g. a pricing datamart). Data are often prepared in a dimensional model (e.g. star schema) optimized for tools such as Power BI or SSAS Tabular Models. This layer forms the direct basis for reports and dashboards.

The entire ELT process is supported technically by Microsoft SQL Server Integration Services (SSIS) for transformation logic (partly directly in SSIS, partly through stored procedure calls in the database) and by Azure Data Factory for orchestration (timing and sequencing of loads and transformations, e.g. nightly runs).

Knowledge of this layered model and its underlying processes is essential for establishing a productive data-science environment.

> 🗄️ *SQL table structure (prototype): [`sql/create_tables.sql`](../sql/create_tables.sql)*

#### 3.2.2 Measures to Ensure Data Quality

Within this thesis and the prototype implementation, the full depth of the described target architecture could not be reproduced because there was no access to the production source systems of the internationally active mid-sized market leader and because simplification was necessary. Instead, the DWH concept was simulated as follows:

- **Database:** A single database (`PricingPrototypeDB`) was created on a local SQL Server Developer Edition instance. It served as the container for all prototype tables.
- **Sources and Staging/Cleanse:** Synthetic sample data were created as CSV files. Loading these files into SQL tables (e.g. `dbo.Produkte`, `dbo.Verkaeufe`, `dbo.Wettbewerbspreise`) through simple SQL scripts (`BULK INSERT`) or the SSMS Import/Export Wizard simulated the staging process and basic cleansing, given the assumed quality of the synthetic data.
- **Core/Bizcore:** Data integration was performed by defining table structures and relationships directly in the SQL database and later in the Power BI data model. More complex transformations and calculations that would typically take place in the Bizcore layer (e.g. feature engineering) were implemented primarily in Python in the prototype (see [Section 3.3](#33-feature-engineering-with-python-and-sql)). Explicit historization (SCD II) was not implemented in the SQL part of the prototype.
- **Datamart:** The tables used in Power BI analysis, including the table with model outputs (`dbo.ModelOutput`), can be understood as a simulation of the datamart layer because they provide the prepared analytical basis for the specific use case of pricing analysis and modeling.
- **ELT tools:** Instead of SSIS and Azure Data Factory, the prototype used Python (`pandas`) for data preparation and loading, along with the SSMS Import/Export Wizard. Execution was manual.

This simulation still made it possible to reproduce the conceptual data flow from the source, through a simplified central storage and transformation layer, to final analysis — even though the technical implementation of the individual DWH layers was strongly simplified.

---

### 3.3 Feature Engineering with Python and SQL

#### 3.3.1 Creating Relevant Features

Feature engineering is a central step in data preparation for price modeling. Informative variables are derived from raw data so that the model receives relevant information about price-quantity relationships and their drivers. The most important feature groups include **time features** (weekday, month, quarter, season, holiday flags), which capture seasonal demand patterns; **price indices**, which relate the company’s own price to the competitor price (relative price index); **marketing effects**, which incorporate advertising activity and click-price information into the explanatory framework; and **rolling metrics**, such as moving averages of sales quantity or price over defined windows, which capture short-term trend components.

In the prototype, feature engineering was implemented in **Python** using `pandas` and `numpy` on the loaded data frames. The function `build_feature_dataframe()` in [`src/data_preparation.py`](../src/data_preparation.py) consolidates data from the different sources and calculates the features required for modeling, in particular the log-transformed price and time-based components that enable more robust estimation of price elasticity.

> 🐍 *Prototype code: [`src/data_preparation.py → build_feature_dataframe()`](../src/data_preparation.py)*  
> 📖 *Feature table with all variables: [MODELL_DOKUMENTATION_EN.md → Section 3](MODELL_DOKUMENTATION_EN.md#3-feature-engineering)*

#### 3.3.2 Transforming Data for Modeling Purposes

Certain data transformations are required for stable and interpretable regression modeling. Of particular importance is the **log transformation** of price and sales quantity: by using a double-log (log-log) model specification, the regression coefficient of price becomes directly interpretable as price elasticity — it indicates by what percentage demand changes when price changes by one percent. This transformation also linearizes the typically multiplicative price-quantity relationship and improves model fit. In addition, scaling measures (e.g. standardization of numeric features) and the encoding of categorical variables (e.g. one-hot encoding for product categories) may be required.

In the prototype, these transformations were carried out directly in Python. Converting date columns, calculating logarithmic values, and deriving simple variables such as relative price indices were implemented in the feature-engineering module before the data were passed into the modeling workflow.

> 📖 *Theoretical background on log transformation: [MODELL_DOKUMENTATION_EN.md → Section 4.1](MODELL_DOKUMENTATION_EN.md#41-theoretical-background)*

---

## 4. Development of the Machine Learning Models for Price Optimization

*[Modeling]*

### 4.1 Selecting Suitable Modeling Approaches

In principle, two classes of approaches are suitable for dynamic price optimization. **Models for estimating price elasticity** — especially regression models with a log-log specification — quantify the direct relationship between price changes and the resulting demand response and therefore provide the theoretical basis for optimal pricing according to the Amoroso-Robinson relation. **Demand forecasting models**, such as time-series models (ARIMA, Prophet) or gradient-based ensemble methods (e.g. Random Forest, XGBoost), complement this approach by predicting absolute demand under given market conditions, which is particularly useful when available price variation is insufficient for elasticity estimation.

For the prototype in this thesis, the focus was deliberately placed on estimating price elasticity using a simplified linear regression in log-log specification. This approach is methodologically transparent, directly interpretable, and makes it possible to cover the entire modeling process — from data preparation to training and the derivation of price recommendations — entirely with Python and `scikit-learn`, as described in the following sections.

> 📖 *Chosen approach in the prototype: [MODELL_DOKUMENTATION_EN.md → Section 4](MODELL_DOKUMENTATION_EN.md#4-ml-model-price-elasticity)*

---

### 4.2 Implementing the Models in Python

#### 4.2.1 Use of Libraries

Implementation of the prototype is based on the established Python ecosystem for data science and machine learning. **`scikit-learn`** was used for the actual modeling: it provides regression classes (e.g. `LinearRegression`), methods for data splitting, and functions for evaluation metrics such as `r2_score`, `mean_absolute_error`, and `mean_squared_error`. Data storage, manipulation, and feature engineering were performed with **`pandas`** (data frames, merging, aggregation), while **`numpy`** was used for numerical operations such as logarithms and matrix calculations.

The development environment was **Jupyter Notebook** (provided through the Anaconda distribution), which supports an iterative and interactive workflow — especially for exploratory analysis and step-by-step development and visualization of the modeling process. The complete end-to-end notebook is available in [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb). The modeling logic was also transferred into [`src/model.py`](../src/model.py), which provides a reproducible and modular implementation.

> 🐍 *Prototype code: [`src/model.py`](../src/model.py)*  
> 📓 *End-to-end notebook: [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)*  
> 📖 *Implementation details: [MODELL_DOKUMENTATION_EN.md → Section 4.2](MODELL_DOKUMENTATION_EN.md#42-implementation)*

#### 4.2.2 Handling Product- and Category-Specific Differences

Accounting for product- or category-specific differences in price elasticity is a key modeling decision. In principle, two strategies are available: **separate models** for each product or category provide maximum flexibility with respect to the specific price-quantity characteristics of each segment, but require enough observations per segment and increase administration effort. Alternatively, a **single shared model** with product ID or category as a categorical feature can be trained; this captures elasticity differences implicitly through estimated coefficients and may work better with limited data.

In the prototype, a pragmatic approach was chosen: because the synthetic data provided a sufficient number of observations for each of the five products, **separate models per product** were trained. This allows direct product-level interpretation of estimated elasticity coefficients and avoids distortions that could arise from overly strong pooling across heterogeneous product categories.

---

### 4.3 Training, Validation, and Model Selection

#### 4.3.1 Split into Training, Validation, and Test Data

A methodologically correct split of the data into training and test sets is a basic prerequisite for reliable model evaluation. With time-series data — and sales data are inherently time-ordered — the classic random holdout split is unsuitable because it violates temporal dependencies and can lead to unrealistically optimistic model evaluation (data leakage). Instead, a **time-series split** is used: chronologically earlier observations form the training set, while the newest observations are used for evaluation. This procedure simulates real conditions in which the model is trained on past data and then generates forecasts for future periods.

In the prototype, the data were split into 80% training data and 20% test data according to the time-series principle. The implementation in Python (`scikit-learn`) ensured that the temporal order of data points remained intact for every product dataset.

> 📖 *Time-series split used (80/20): [MODELL_DOKUMENTATION_EN.md → Section 4.2](MODELL_DOKUMENTATION_EN.md#42-implementation)*

#### 4.3.2 Metrics for Evaluating Model Quality

To evaluate model quality, the prototype uses metrics established in the literature for regression models. The **coefficient of determination R²** indicates which share of the variance in the target variable (log sales quantity) is explained by the model; a value close to 1 indicates a high quality of fit. The **Mean Absolute Error (MAE)** measures the average absolute prediction error in the unit of the target variable and is robust to outliers. The **Root Mean Squared Error (RMSE)** penalizes large individual errors more strongly and therefore allows a more differentiated assessment of model stability.

All three metrics were calculated on the respective test sets using the functions `r2_score`, `mean_absolute_error`, and `mean_squared_error` from `sklearn.metrics`. The concrete metric values for all five products in the prototype are documented in [MODELL_DOKUMENTATION_EN.md → Section 7.1](MODELL_DOKUMENTATION_EN.md#71-model-quality-metrics-test-set-time-series-split-8020).

> 📖 *Concrete metric values (R², MAE, RMSE): [MODELL_DOKUMENTATION_EN.md → Section 7.1](MODELL_DOKUMENTATION_EN.md#71-model-quality-metrics-test-set-time-series-split-8020)*

---

### 4.4 Deriving Price Recommendations from Model Results

Converting model outputs into operational price recommendations is the actual prescriptive step in the optimization process. Conceptually, the **Amoroso-Robinson relation** provides the theoretical basis: the profit-maximizing price can be derived as a function of estimated price elasticity and marginal cost. In practical implementation, however, additional constraints must be considered, including minimum and maximum prices (e.g. due to margin targets or contractual agreements), competitor prices as a reference, and platform-specific restrictions on Amazon. These business rules ensure that algorithmically derived prices remain economically meaningful and market-compliant.

In the prototype, a simplified price-recommendation approach was implemented: the estimated regression coefficient for log-transformed price is interpreted as price elasticity ε. Based on this value and on the current competitor price, the function `recommend_price()` in [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) calculates a price suggestion. For highly elastic demand (|ε| > 1), a closer alignment to the competitor price is recommended, whereas inelastic demand permits a markup. The resulting outputs — elasticity, current price, competitor price, and recommended price per product — are then stored in the SQL database table `dbo.ModelOutput` and are thus available for reporting in Power BI.

> 🐍 *Prototype code: [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py)*  
> 📖 *Amoroso-Robinson relation and business rules: [MODELL_DOKUMENTATION_EN.md → Section 6](MODELL_DOKUMENTATION_EN.md#6-price-recommendation-prescriptive-analytics)*

---

## 5. Evaluation and Validation of the Pricing Strategy

*[Evaluation]*

### 5.1 Technical Evaluation of the Model Results and Elasticities

The technical evaluation of the model begins with analysis of the quality metrics defined in [Section 4.3.2](#432-metrics-for-evaluating-model-quality) on the test set. The R² values of the product-specific models indicate how strongly log-transformed price, as an important explanatory factor, describes the variance in quantity sold; MAE and RMSE quantify the typical prediction quality in the log-transformed scale. The concrete values achieved in the prototype are documented in [MODELL_DOKUMENTATION_EN.md → Section 7](MODELL_DOKUMENTATION_EN.md#7-results-and-evaluation).

In addition to quantitative model evaluation, a qualitative **plausibility check** of the estimated elasticities is essential. Economically sound expectations are: price elasticities should be negative (higher prices lead to lower demand), their magnitude should fall within the range typically observed for consumer goods (usually −0.5 to −2.0), and products under stronger competitive pressure should show higher elasticities than niche products. Deviations from these expectations would point to modeling problems, data errors, or missing explanatory variables and would require critical investigation of their causes.

> 📖 *Model quality and plausibility check: [MODELL_DOKUMENTATION_EN.md → Section 7](MODELL_DOKUMENTATION_EN.md#7-results-and-evaluation)*

---

### 5.2 Design and Simulation of A/B Tests in an E-Commerce Context

A/B tests — also referred to as controlled field experiments — are the most methodologically robust instrument for validating price changes in a real market environment. While model metrics only describe how well a model reproduces historical patterns, A/B tests provide causal evidence of whether a price change actually produces the expected effects on quantity, revenue, and margin. For an internationally active mid-sized market leader on Amazon, such a test design could look as follows: a randomly selected subset of products (test group) receives the model-recommended price, while a comparable control group keeps the current price. After a defined test period, the KPIs of both groups are compared statistically in order to isolate the causal effect of the price change.

Results from such tests can be used to improve the model on several levels: first, they provide real response data that calibrate the model against actually observed elasticities; second, they reveal product segments in which the model systematically over- or underestimates reactions; third, they enable continuous verification of model assumptions under changing market conditions. Within the present prototype, a real A/B test could only be addressed conceptually due to the absence of real sales data and missing platform access; the methodological basis is documented in [MODELL_DOKUMENTATION_EN.md → Section 7.3](MODELL_DOKUMENTATION_EN.md#73-ab-test-concept).

> 📖 *A/B test concept: [MODELL_DOKUMENTATION_EN.md → Section 7.3](MODELL_DOKUMENTATION_EN.md#73-ab-test-concept)*

---

### 5.3 Assessing the Impact on Business Goals (Revenue, Margin)

Measuring the business impact of an operational price optimization system requires methods that go beyond purely technical model evaluation. In live operation, the **comparison of test and control groups** (parallel A/B tests) and **time-series comparisons** (before/after analyses with statistical control of confounders) are particularly suitable. Relevant KPIs include revenue change (ΔRevenue), margin change (ΔMargin), and change in quantity sold (ΔQuantity) relative to a baseline period or a control group.

In the prototype, this impact analysis was simulated using synthetic data in Power BI via **DAX** measures. For each product, expected changes in revenue and margin were calculated on the basis of the model outputs in `dbo.ModelOutput`, assuming that the recommended price is used instead of the current price. The concrete formulas and the resulting ΔRevenue and ΔMargin values for all products are documented in detail in [MODELL_DOKUMENTATION_EN.md → Section 6.3](MODELL_DOKUMENTATION_EN.md#63-concrete-calculation-for-all-products-as-of-31122023).

> 📖 *Concrete ΔRevenue and ΔMargin calculations: [MODELL_DOKUMENTATION_EN.md → Section 6.3](MODELL_DOKUMENTATION_EN.md#63-concrete-calculation-for-all-products-as-of-31122023)*

---

### 5.4 Iterative Improvement of the Models Based on Evaluation Results

A data-driven price optimization model is not a static artifact but requires a **continuous improvement process** in order to deliver valid recommendations over time. Market conditions, competitor behavior, and demand structures change continuously; therefore, a model trained exclusively on historical data gradually loses predictive accuracy (concept drift). To counter this, regular **monitoring** of model quality (e.g. weekly reviews of MAE and R² on new data), defined triggers for **retraining** (e.g. if R² falls below a threshold), and periodic **feature adjustments** to changing drivers are necessary. This principle corresponds to the CRISP-DM process model described in [Chapter 1](#1-introduction) and emphasizes the iterative nature of data-mining projects.

---

## 6. Operationalization and Monitoring in the BI System

*[Deployment]*

### 6.1 Provision of Model Results

Providing model results for operational reporting and decision support is a central step in the deployment process. In the target system, the plan is to write the calculated elasticities and price recommendations into the data warehouse, from where they become accessible through the datamart layer for tools such as Power BI or SSAS Tabular Models. This architecture enables a clean separation between the modeling process (Python/`scikit-learn`) and the reporting front end (Power BI), because both layers are decoupled via the SQL database.

In the prototype, this approach was implemented by directly storing the model results in the table `dbo.ModelOutput` of the local SQL Server Developer Edition database. The function `save_recommendations()` in [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) writes the calculated KPIs for each product (elasticity, current price, competitor price, recommended price, expected quantity change, and expected revenue change) to this table, which then serves as the data source for the Power BI dashboard.

> 🐍 *Prototype code: [`src/pricing_optimizer.py → save_recommendations()`](../src/pricing_optimizer.py)*  
> 📖 *`dbo.ModelOutput` schema: [MODELL_DOKUMENTATION_EN.md → Section 8.1](MODELL_DOKUMENTATION_EN.md#81-dbomodeloutput)*

---

### 6.2 Building an Analytical Data Model (Tabular Model in SSAS) for the Front End

#### 6.2.1 Definition of Dimensions, Facts, and Hierarchies for Pricing Analyses

In the target system, **SQL Server Analysis Services (SSAS) Tabular** is planned as the analytical database layer. SSAS Tabular models provide highly performant analytics over large data volumes through the underlying **VertiPaq** compression technology, a central and versioned data model with consistent business metrics, and seamless integration with Power BI and Excel. Knowledge of SSAS Tabular and DAX is therefore a valuable competency in enterprise business intelligence, as Tabular models often serve as the single source of truth for reporting needs in larger organizations.

Since Power BI Desktop uses the same VertiPaq engine internally as SSAS Tabular, the Power BI data model built in the prototype served as a functionally equivalent simulation of a Tabular Model. The model follows a **star-schema** structure: fact tables (sales, competitor prices, model results) are linked to dimension tables (products, date) via defined relationships. This model structure enables efficient filtering and aggregation across multiple dimensions and forms the basis for all DAX calculations in the prototype.

#### 6.2.2 Implementation of Relevant KPIs with DAX

The usefulness of a Power BI dashboard depends heavily on the quality and correctness of the defined **DAX measures**. In the prototype, core KPIs for pricing reporting were implemented. The measure **Turnover** calculates total revenue as the sum of quantity sold multiplied by selling price. **Net Margin (simulated)** is derived from the difference between revenue and simulated unit costs relative to revenue and indicates the gross margin percentage. **Average Price** calculates the quantity-weighted mean of realized selling prices over a selected period. Additional measures expose the model-calculated **price elasticity** and the **recommended price** from `dbo.ModelOutput` depending on the selected product, thereby allowing a direct comparison between the current situation and the model recommendation in the dashboard. Correct implementation of these measures requires a sound understanding of DAX evaluation context and filter logic and illustrates the importance of BI development skills within such a project.

---

### 6.3 Development of Power BI Dashboards and Reports

#### 6.3.1 Visualization of Price Recommendations and Their Drivers

The Power BI prototype includes several report pages that visualize different aspects of dynamic price optimization. An **overview page** shows the development of revenue and quantity sold over time, broken down by products and categories, and provides a quick understanding of business development. A dedicated **pricing analysis page** presents the calculated price elasticities per product — for example as a bar chart — shows the current price compared with the competitor price, and displays the model-recommended price as well as the expected effects on quantity, revenue, and margin. A **competitor price page** visualizes the time-based development of own prices versus simulated market prices and identifies periods in which price adjustments would be especially relevant. These visualizations make the abstract model outputs immediately understandable and actionable for management and the e-commerce team.

> 📓 *Dashboard implementation: [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)*  
> 📖 *Dashboard pages: [MODELL_DOKUMENTATION_EN.md → Section 8.2](MODELL_DOKUMENTATION_EN.md#82-dashboard-power-bi-prototype)*

![Dashboard Preview](../dashboard_preview.png)

#### 6.3.2 Monitoring Price Development and Model Performance

The prototype dashboard also functions as a **monitoring instrument** for operational steering of KPIs and model outputs. By integrating the table `dbo.ModelOutput` into the Power BI data model, elasticities, price recommendations, and simulated outcome metrics are always available and can be compared across products. Members of the Amazon team can see at a glance for which products the model recommends a price adjustment, what effects are expected, and whether actual price development is aligned with the model’s recommendations.

#### 6.3.3 Providing Analysis Tools for the Amazon Team and Controlling

The Power BI prototype positions itself as a concrete example of a self-service-capable **analysis tool** that supports both the Amazon team in operational pricing decisions and controlling in strategic performance steering. Through its intuitive user interface and its ability to integrate a wide variety of data sources, Power BI offers low-threshold access to complex analytical results without requiring end users to have deep technical knowledge. In a productive deployment, the dashboard would be published through the Power BI Service so that all authorized employees could always access up-to-date data.

---

### 6.4 Considerations for Automating the End-to-End Process

Automation of the overall process is a necessary prerequisite for operational use of the price optimization system. In the target system, several measures are envisaged for this purpose: **data refresh** (nightly ETL runs) can be orchestrated by **SQL Server Agent** or **Azure Data Factory**. Regular **model retraining** can be implemented as a scheduled **Python job** that recalibrates the model on new data and writes updated results into `dbo.ModelOutput`. Refresh of the Power BI dashboard would take place in the target system through **Power BI Scheduled Refresh**, ensuring that end users always see current model outputs.

In the thesis prototype, however, the entire process — from data generation through Python modeling to manual refresh of the Power BI report — was carried out entirely **manually**. Full automation was not required to prove methodological feasibility, but it is conceptually planned as the logical next stage of development for the target system.

> 📖 *Planned target-system enhancements: [README_EN.md → Enhancements (Target System)](../README_EN.md#enhancements-target-system)*

---

## 7. Summary and Results

### 7.1 Presentation of the Developed System

The prototype developed within this thesis implements a complete **end-to-end data flow** for a dynamic price optimization model. Starting from synthetic product master, sales, and competitor-price data generated in Python and provided as CSV files, the data are first loaded into a local **SQL Server** Developer Edition database. From this relational database, the data are retrieved by a **Python**-based modeling module (`pandas`, `numpy`, `scikit-learn`), feature-engineered, and used to train product-specific elasticity regression models. The calculated price recommendations are then written back into SQL Server (table `dbo.ModelOutput`). Finally, **Power BI** Desktop connects to the SQL Server database, reads the `ModelOutput` table along with the base tables, and presents the results in interactive dashboards. This process reproduces the key architectural components of a productive system and demonstrates the technical feasibility of the overall concept.

> 📖 *System architecture overview: [MODELL_DOKUMENTATION_EN.md → Section 1](MODELL_DOKUMENTATION_EN.md#1-system-architecture-and-data-flow) and [README_EN.md → System Overview](../README_EN.md#system-overview)*

---

### 7.2 Summary of the Key Results

The most important findings of the prototype can be summarized using the calculated price elasticities and the resulting price recommendations. For the five simulated products, elasticities between −0.52 (product P004, inelastic demand) and −1.32 (product P003, highly elastic demand) were estimated. These values exhibit both economically plausible signs and realistic magnitudes for consumer goods. The R² values of the product-specific regression models range between 0.42 and 0.61, which represents acceptable model quality given the simulated nature of the data and illustrates the potential of this approach on real production data. The complete result table for all products, including simulated KPI effects (ΔQuantity, ΔRevenue, ΔMargin), is documented in [MODELL_DOKUMENTATION_EN.md → Section 6.4](MODELL_DOKUMENTATION_EN.md#64-overall-results-for-all-products-modeloutput) and summarized again below.

> 📖 *Full result table (`ModelOutput`): [MODELL_DOKUMENTATION_EN.md → Section 6.4](MODELL_DOKUMENTATION_EN.md#64-overall-results-for-all-products-modeloutput)*

The key prototype results (production run with `SEED=42`, sales year 2023):

| Product | ε | R² | Current Price | Competitor Price | Rec. Price | ΔQuantity | ΔRevenue | ΔMargin |
|---|---|---|---|---|---|---|---|---|
| P001 | −1.18 | 0.61 | 63.57 € | 62.67 € | **76.28 €** | −23.6 % | −8.4 % | **+5.3 %** |
| P002 | −1.05 | 0.42 | 102.71 € | 98.27 € | **104.97 €** | −2.3 % | −0.2 % | **+1.9 %** |
| P003 | −1.32 | 0.57 | 24.63 € | 22.99 € | **29.56 €** | −26.4 % | −11.6 % | **−1.6 %** |
| P004 | −0.52 | 0.50 | 30.39 € | 38.72 € | **33.95 €** | −6.2 % | +4.9 % | **+15.6 %** |
| P005 | −0.66 | 0.44 | 45.37 € | 49.96 € | **48.33 €** | −4.3 % | +2.0 % | **+6.9 %** |

---

### 7.3 Contribution to Data-Driven Decision-Making and Strategic Goals

The developed system demonstrates clearly how data-driven decision-making in e-commerce pricing can be operationalized. Instead of intuitive one-off decisions or rigid pricing rules, the model-based approach enables systematic, scalable, and traceable pricing that simultaneously considers competitive dynamics, demand elasticities, and margin targets. For an internationally active mid-sized market leader, this means in concrete terms: the Amazon team receives a data-based price recommendation for each product, together with quantified expected effects on revenue and margin, which can serve as a well-founded decision basis and replace or at least substantially support previous manual processes. The prototype also shows that the required technologies and methods can already be implemented prototypically with a manageable level of effort.

---

### 7.4 Outlook on Future Enhancements and Limitations

As a prototype, the present thesis is naturally subject to several limitations that must be stated openly. First, the entire modeling approach is based on **synthetic data**, which simulate realistic price-quantity relationships but cannot reflect the full complexity and heterogeneity of real production data. Second, intentionally **simple regression models** were used; in practice, nonlinear approaches (Random Forest, XGBoost) or time-series models (Prophet, ARIMA) could potentially deliver significantly better predictive quality. Third, **no real A/B tests** were conducted, which means that causal validation of the price recommendations is still outstanding. Fourth, the prototype is executed **manually** and is not embedded in a productive automation infrastructure.

Accordingly, the opportunities for further development are substantial. A top priority is the transition to **real sales and competitor data** from the productive source systems. Beyond that, implementing **A/B test frameworks** on Amazon, using more advanced modeling approaches, fully automating the pipelines (Azure Data Factory, SQL Server Agent, Power BI Scheduled Refresh), and leveraging cloud services such as Azure Machine Learning are all concrete next steps. Implementing these steps necessarily requires a dedicated **data-science environment** with the corresponding data access, technical infrastructure, and interdisciplinary collaboration between e-commerce, IT, and controlling.

> 📖 *Planned target-system enhancements: [README_EN.md → Enhancements (Target System)](../README_EN.md#enhancements-target-system)*

---

## List of Figures

*Figure 1-1: Cross Industry Standard Process for Data Mining (CRISP-DM), source: Wikipedia, CC BY-SA 3.0 — page 8*

---

## References

1. IBCS Association, *International Business Communication Standards (IBCS)*, Version 1.2

2. Microsoft Learn Portal, *Data Types (Transact-SQL)*, <https://learn.microsoft.com/de-de/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver16> (accessed 2024-03-04)

3. Microsoft Learn Portal, *“Power BI usage scenarios”*, <https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-overview> (accessed 2024-03-04)

4. Microsoft Learn Portal, *“Power BI usage scenarios: Customizable managed self-service BI”*, <https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-customizable-managed-self-service-bi> (accessed 2024-03-04)

---

*Last update: Markdown conversion of the original document ([`Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx`](../Studienarbeit%20Dynamisches%20Preisoptimierungsmodell%20im%20eCommerce-%20Andreas%20Traut.docx))*
