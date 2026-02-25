# DYNAMISCHES PREISOPTIMIERUNGSMODELL IM E-COMMERCE

---

**Studienarbeit**

*Entwicklung und Implementierung eines dynamischen Preisoptimierungs-Modells für das E-Commerce-Sortiment am Beispiel eines international tätigen Branchenführers*

---

**Autor:** Andreas Traut

---

> 📄 **Original-Dokument (Word):**  
> [`Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx`](../Studienarbeit%20Dynamisches%20Preisoptimierungsmodell%20im%20eCommerce-%20Andreas%20Traut.docx)
>
> 📖 **Detaillierte Modell-Dokumentation mit konkreten Berechnungen und Quellcode-Verlinkungen:**  
> [`docs/MODELL_DOKUMENTATION.md`](MODELL_DOKUMENTATION.md)
>
> 🚀 **Projektübersicht und Schnellstart:**  
> [`README.md`](../README.md)

---

## Inhaltsverzeichnis

1. [Exposé](#exposé)
2. [Gliederung](#gliederung)
3. [1. Einleitung](#1-einleitung)
   - [1.1 Problemstellung](#11-problemstellung-limitierungen-statischer-preisstrategien-im-dynamischen-e-commerce-umfeld-insb-amazon)
   - [1.2 Zielsetzung](#12-zielsetzung-maximierung-von-umsatz-turnover-und-marge-net-margin-durch-ein-ml-basiertes-preisoptimierungssystem)
   - [1.3 Relevanz und Kontext](#13-relevanz-und-kontext-für-einen-international-tätigen-mittelständischen-weltmarktführer)
   - [1.4 Begründung der Abgrenzung zum Data Analysten](#14-begründung-der-abgrenzung-zum-data-analysten)
   - [1.5 Theoretische Einordnung: Prädiktive und Präskriptive Analytik](#15-theoretische-einordnung-prädiktive-und-präskriptive-analytik-im-projektkontext)
   - [1.6 Cross Industry Standard Process for Data Mining (CRISP-DM)](#16-cross-industry-standard-process-for-data-mining-crisp-dm)
4. [2. Analyse der Ausgangslage und Datenanforderungen](#2-analyse-der-ausgangslage-und-datenanforderungen)
   - [2.1 Bestehende Preisprozesse und Herausforderungen](#21-bestehende-preisprozesse-und-herausforderungen-im-e-commerce-team-insb-amazon)
   - [2.2 Identifikation und Bewertung benötigter Datenquellen](#22-identifikation-und-bewertung-benötigter-datenquellen)
   - [2.3 Anforderungen an Datenqualität, Granularität und Verfügbarkeit](#23-anforderungen-an-datenqualität-granularität-und-verfügbarkeit)
5. [3. Datenintegration und -aufbereitung für die Preismodellierung](#3-datenintegration-und--aufbereitung-für-die-preismodellierung-data-understanding--data-preparation)
   - [3.1 Konzeption der ETL-Strecken](#31-konzeption-der-etl-strecken-zur-datenakquise-und--integration)
   - [3.2 Aufbau und Erweiterung des Data Warehouse nach Schichtenmodell](#32-aufbau-und-erweiterung-des-data-warehouse-nach-schichtenmodell-core-bizcore-datamart-für-pricing-daten)
   - [3.3 Feature Engineering mittels Python (pandas, numpy) und SQL](#33-feature-engineering-mittels-python-pandas-numpy-und-sql)
6. [4. Entwicklung der Machine-Learning-Modelle zur Preisoptimierung](#4-entwicklung-der-machine-learning-modelle-zur-preisoptimierung-modeling)
   - [4.1 Auswahl geeigneter Modellierungsansätze](#41-auswahl-geeigneter-modellierungsansätze)
   - [4.2 Implementierung der Modelle in Python](#42-implementierung-der-modelle-in-python)
   - [4.3 Training, Validierung und Auswahl der Modelle](#43-training-validierung-und-auswahl-der-modelle)
   - [4.4 Ableitung von Preisempfehlungen aus den Modellergebnissen](#44-ableitung-von-preisempfehlungen-aus-den-modellergebnissen)
7. [5. Evaluation und Validierung der Preisstrategie](#5-evaluation-und-validierung-der-preisstrategie-evaluation)
   - [5.1 Technische Evaluation der Modellergebnisse und Elastizitäten](#51-technische-evaluation-der-modellergebnisse-und-elastizitäten)
   - [5.2 Konzeption und Simulation von A/B-Tests im E-Commerce Kontext](#52-konzeption-und-simulation-von-ab-tests-im-e-commerce-kontext)
   - [5.3 Bewertung der Auswirkungen auf die Geschäftsziele (Umsatz, Marge)](#53-bewertung-der-auswirkungen-auf-die-geschäftsziele-umsatz-marge)
   - [5.4 Iterative Verbesserung der Modelle basierend auf Evaluationsergebnissen](#54-iterative-verbesserung-der-modelle-basierend-auf-evaluationsergebnissen)
8. [6. Operationalisierung und Monitoring im BI-System](#6-operationalisierung-und-monitoring-im-bi-system-deployment)
   - [6.1 Bereitstellung der Modellergebnisse](#61-bereitstellung-der-modellergebnisse)
   - [6.2 Aufbau eines analytischen Datenmodells (Tabular Model in SSAS) für das Frontend](#62-aufbau-eines-analytischen-datenmodells-tabular-model-in-ssas-für-das-frontend)
   - [6.3 Entwicklung von Power BI Dashboards und Reports](#63-entwicklung-von-power-bi-dashboards-und-reports)
   - [6.4 Überlegungen zur Automatisierung des Gesamtprozesses](#64-überlegungen-zur-automatisierung-des-gesamtprozesses)
9. [7. Zusammenfassung und Ergebnisse](#7-zusammenfassung-und-ergebnisse)
   - [7.1 Darstellung des entwickelten Systems](#71-darstellung-des-entwickelten-systems)
   - [7.2 Zusammenfassung der Kernergebnisse](#72-zusammenfassung-der-kernergebnisse)
   - [7.3 Beitrag zur datengesteuerten Entscheidungsfindung und Erreichung strategischer Ziele](#73-beitrag-zur-datengesteuerten-entscheidungsfindung-und-erreichung-strategischer-ziele)
   - [7.4 Ausblick auf mögliche Weiterentwicklungen und Limitationen](#74-ausblick-auf-mögliche-weiterentwicklungen-und-limitationen)
10. [Abbildungsverzeichnis](#abbildungsverzeichnis)
11. [Literaturverzeichnis](#literaturverzeichnis)

---

## Exposé

In einem hochdynamischen E-Commerce-Umfeld, insbesondere auf Plattformen wie Amazon, ist eine agile und datengesteuerte Preisstrategie entscheidend für die Maximierung von Umsatz und Marge sowie die Sicherung der Wettbewerbsfähigkeit. Statische Preismodelle oder manuelle Anpassungen können den schnellen Marktveränderungen, Wettbewerbsaktionen und Nachfrageschwankungen oft nicht gerecht werden. Um das volle Potenzial des E-Commerce-Geschäfts eines international tätigen, mittelständischen Branchenführers auszuschöpfen, wird in dieser Arbeit die Konzeption, Entwicklung und Implementierung eines Machine-Learning-basierten Systems zur dynamischen Preisoptimierung untersucht. Ziel ist es, Preisempfehlungen automatisiert zu generieren, die Preiselastizitäten auf Produktebene berücksichtigen und zur Steigerung von Kennzahlen wie Umsatz (Turnover) und Nettomarge (Net Margin) beitragen.

Die zentrale Herausforderung liegt in der Integration und Verarbeitung heterogener Datenquellen sowie der Komplexität der zugrundeliegenden Modelle. Benötigt werden Verkaufsdaten, Lagerbestandsinformationen, Wettbewerbspreise (z.B. über APIs oder Scraping), Marketingaktivitätsdaten (z.B. aus Pacvue) und potenziell externe Marktdaten. Diese Daten müssen mittels robuster ETL-Prozesse, unter Nutzung von PowerQuery und SQL Server Integration Services (SSIS), in das bestehende Datawarehouse überführt und im Schichtenmodell (Core, Bizcore, Datamart) aufbereitet werden. Eine hohe Datenqualität, beispielsweise durch Abgleich von Pacvue- und internen Daten, ist hierbei essenziell.

Im Kern des Projekts steht die Entwicklung von Machine-Learning-Modellen zur Berechnung von Preiselastizitäten und zur Vorhersage optimaler Preispunkte. Hierfür kommen Python mit Bibliotheken wie scikit-learn, pandas und numpy zum Einsatz. Verschiedene Algorithmen (z.B. Regressionsmodelle, Zeitreihenanalysen) werden evaluiert und mittels historischer Daten trainiert. Die Modellergebnisse müssen validiert werden, beispielsweise durch A/B-Testing-Methodiken im E-Commerce-Kontext.

Ein weiterer Schwerpunkt ist die Operationalisierung der Ergebnisse und die Befähigung des Amazon-Teams sowie des Controllings. Die Preisempfehlungen müssen entweder direkt in Systeme integriert oder über aussagekräftige Dashboards bereitgestellt werden. Hierfür werden auf Basis geeigneter Tabular Modelle im SQL Server Analysis Service (SSAS) interaktive Power BI Reportings erstellt. Diese Visualisierungen, unter intensiver Nutzung von DAX-Berechnungen, ermöglichen nicht nur die Überwachung der Preisstrategie und deren Auswirkungen auf Turnover und Net Margin, sondern auch die Analyse der Modellgüte und der Sensitivität auf verschiedene Einflussfaktoren (z.B. Price Sensitivity Analysen). Die SQL-Expertise (T-SQL, Stored Procedures, Views) ist dabei für die Datenaufbereitung und -bereitstellung im Backend unerlässlich.

Diese Arbeit geht über die reine Datenanalyse („Data Analyst" Rolle) hinaus, indem sie prädiktive und präskriptive Analytik (siehe [Kapitel 1.5](#15-theoretische-einordnung-prädiktive-und-präskriptive-analytik-im-projektkontext)) nutzt, um aktiv in die Geschäftssteuerung einzugreifen. Sie demonstriert den Aufbau einer komplexen Data-Science-Lösung von der Datenintegration über die Modellentwicklung bis zur operativen Implementierung und dem Monitoring mittels moderner BI-Tools. Das Ergebnis ist ein intelligentes Preisoptimierungssystem, das die Entscheidungsfindung im E-Commerce auf eine neue Stufe hebt und einen messbaren Beitrag zur Erreichung der strategischen Ziele eines international tätigen, mittelständischen Branchenführers leistet.

---

## Gliederung

1. **Einleitung** (1 Seite)
   - Problemstellung: Limitierungen statischer Preisstrategien im dynamischen E-Commerce Umfeld (insb. Amazon)
   - Zielsetzung: Maximierung von Umsatz (Turnover) und Marge (Net Margin) durch ein ML-basiertes Preisoptimierungssystem
   - Relevanz und Kontext für einen international tätigen, mittelständischen Branchenführer
   - Theoretische Einordnung: Prädiktive und Präskriptive Analytik im Projektkontext
   - Cross Industry Standard Process for Data Mining (CRISP-DM)

2. **Analyse der Ausgangslage und Datenanforderungen** (ca. 1,5 Seiten) *[Business Understanding / Data Understanding]*
   - Bestehende Preisprozesse und Herausforderungen im E-Commerce Team (insb. Amazon)
   - Identifikation und Bewertung benötigter Datenquellen
     - Interne Daten (Verkäufe, Lagerbestand, Produktdaten, ERP-Daten)
     - Externe Daten (Wettbewerbspreise, Marketing-Plattformdaten z.B. Pacvue, Marktdaten)
   - Anforderungen an Datenqualität, Granularität und Verfügbarkeit

3. **Datenintegration und -aufbereitung für die Preismodellierung** (ca. 2,5 Seiten) *[Data Understanding / Data Preparation]*
   - Konzeption der ETL-Strecken zur Datenakquise und -integration
     - Nutzung von PowerQuery und SQL Server Integration Services (SSIS)
     - Anbindung von APIs oder Scraping-Lösungen (für Wettbewerbsdaten)
   - Aufbau und Erweiterung des Data Warehouse nach Schichtenmodell (Core, Bizcore, Datamart) für Pricing-Daten
     - Datenmodellierung im Backend (SQL)
     - Maßnahmen zur Sicherstellung der Datenqualität (z.B. Abgleich Pacvue vs. interne Daten)
   - Feature Engineering mittels Python (pandas, numpy) und SQL
     - Erstellung relevanter Merkmale (z.B. Zeitmerkmale, Preisindizes, Marketing-Einflüsse, rollierende Kennzahlen)
     - Transformation von Daten für Modellierungszwecke (z.B. Log-Transformation)

4. **Entwicklung der Machine-Learning-Modelle zur Preisoptimierung** (ca. 3–4 Seiten) *[Modeling]*
   - Auswahl geeigneter Modellierungsansätze
     - Modelle zur Schätzung der Preiselastizität (z.B. Regressionsmodelle)
     - Modelle zur Nachfrageprognose (z.B. Zeitreihenanalyse, weitere Regressionsmodelle)
   - Implementierung der Modelle in Python
     - Nutzung von Bibliotheken (scikit-learn, pandas, numpy etc.)
     - Umgang mit produkt- oder kategoriespezifischen Unterschieden
   - Training, Validierung und Auswahl der Modelle
     - Aufteilung in Trainings-, Validierungs- und Testdaten
     - Metriken zur Bewertung der Modellgüte
   - Ableitung von Preisempfehlungen aus den Modellergebnissen

5. **Evaluation und Validierung der Preisstrategie** (ca. 2 Seiten) *[Evaluation]*
   - Technische Evaluation der Modellergebnisse und Elastizitäten
   - Konzeption und Simulation von A/B-Tests im E-Commerce Kontext
   - Bewertung der Auswirkungen auf die Geschäftsziele (Umsatz, Marge)
   - Iterative Verbesserung der Modelle basierend auf Evaluationsergebnissen

6. **Operationalisierung und Monitoring im BI-System** (ca. 3 Seiten) *[Deployment]*
   - Bereitstellung der Modellergebnisse (z.B. Speicherung in DWH, Bereitstellung über API)
   - Aufbau eines analytischen Datenmodells (Tabular Model in SSAS) für das Frontend
     - Definition von Dimensionen, Fakten und Hierarchien für Pricing-Analysen
     - Implementierung relevanter Kennzahlen mittels DAX (Turnover, Net Margin, Price Sensitivity Indikatoren)
   - Entwicklung von Power BI Dashboards und Reports
     - Visualisierung von Preisempfehlungen und deren Einflussfaktoren
     - Monitoring der Preisentwicklung und Modell-Performance
     - Bereitstellung von Analysewerkzeugen für das Amazon-Team und Controlling
   - Überlegungen zur Automatisierung des Gesamtprozesses (Datenaktualisierung, Modell-Retraining, Reporting)

7. **Zusammenfassung und Ergebnisse** (ca. 1 Seite) *[Evaluation / Deployment Context]*
   - Darstellung des entwickelten Systems zur dynamischen Preisoptimierung
   - Zusammenfassung der Kernergebnisse (z.B. ermittelte Elastizitäten, Performance des Systems)
   - Beitrag zur datengesteuerten Entscheidungsfindung und Erreichung strategischer Ziele
   - Ausblick auf mögliche Weiterentwicklungen und Limitationen

---

## 1. Einleitung

### 1.1 Problemstellung: Limitierungen statischer Preisstrategien im dynamischen E-Commerce Umfeld (insb. Amazon)

Der E-Commerce, insbesondere auf dominanten Plattformen wie Amazon, ist durch eine außerordentliche Dynamik gekennzeichnet. Preise von Wettbewerbern ändern sich häufig, Kundenreaktionen sind unmittelbar sichtbar, Marketingkampagnen beeinflussen die Nachfrage und das Produktangebot wird ständig angepasst. Diese hohe Volatilität und Komplexität erfordern von Unternehmen eine hohe Agilität in ihrer Preisstrategie, um wettbewerbsfähig zu bleiben und Ertragspotenziale optimal auszuschöpfen.

Traditionelle Preisstrategien, die auf statischen Preislisten, periodischen manuellen Anpassungen oder einfachen, regelbasierten Ansätzen beruhen, erweisen sich in diesem Umfeld zunehmend als unzureichend. Ihre wesentlichen Limitierungen sind:

- **Reaktionsgeschwindigkeit:** Manuelle Prozesse oder langwierige Abstimmungsrunden sind zu träge, um zeitnah auf kurzfristige Marktveränderungen oder Aktionen von Wettbewerbern reagieren zu können. Chancen zur Umsatzsteigerung oder Margenoptimierung bleiben ungenutzt, oder es wird zu spät auf aggressive Preisunterbietungen reagiert.

- **Komplexität und Skalierbarkeit:** Die Anzahl der Produkte (SKUs), der relevanten Wettbewerber und der Einflussfaktoren auf die Nachfrage (Saisonalität, Marketing, Lagerbestand, Kundenbewertungen etc.) ist oft sehr groß. Eine manuelle Berücksichtigung all dieser Faktoren für jedes Produkt ist kaum leistbar und extrem fehleranfällig.

- **Datennutzung:** Die Fülle an verfügbaren Daten aus Verkaufstransaktionen, Webseiten-Tracking, Marketingplattformen (wie Pacvue) und Wettbewerbsbeobachtung wird bei statischen Ansätzen nicht oder nur unzureichend genutzt. Wertvolle Informationen über Preissensitivitäten und Nachfragemuster bleiben verborgen.

- **Suboptimalität:** Ohne eine systematische Analyse der Preiselastizität und der Nachfrageeffekte führen manuelle oder rein kostenbasierte Preisentscheidungen häufig zu suboptimalen Ergebnissen – entweder werden mögliche Margen verschenkt oder Absatzpotenziale durch zu hohe Preise nicht realisiert.

Diese Unzulänglichkeiten führen dazu, dass Unternehmen mit statischen Preisstrategien im dynamischen E-Commerce-Umfeld systematisch hinter ihren Möglichkeiten zurückbleiben und einem unnötigen Wettbewerbsdruck ausgesetzt sind.

> 📖 *Konkrete Zahlen zur Problematik statischer Preisstrategien und deren Auswirkungen finden sich in den Modellergebnissen: [MODELL_DOKUMENTATION.md → Kap. 7](MODELL_DOKUMENTATION.md#7--ergebnisse--evaluation-studienarbeit-kap-5)*

---

### 1.2 Zielsetzung: Maximierung von Umsatz (Turnover) und Marge (Net Margin) durch ein ML-basiertes Preisoptimierungssystem

Angesichts der in [Kapitel 1.1](#11-problemstellung-limitierungen-statischer-preisstrategien-im-dynamischen-e-commerce-umfeld-insb-amazon) beschriebenen Limitierungen statischer Ansätze ist das primäre betriebswirtschaftliche Ziel, das mit der Implementierung eines dynamischen Preisoptimierungssystems verfolgt wird, die Maximierung von Umsatz (Turnover) und Nettomarge (Net Margin) im E-Commerce-Geschäft. Es geht darum, durch intelligentere Preisgestaltung einen messbaren Beitrag zur Steigerung der Profitabilität und des Geschäftsvolumens zu leisten.

Um dieses übergeordnete Geschäftsziel zu erreichen, verfolgt diese Arbeit das spezifische technische und konzeptionelle Ziel, ein Machine-Learning-(ML)-basiertes System zur dynamischen Preisoptimierung zu konzipieren und prototypisch zu implementieren. Dieses System soll datengestützt und automatisiert Preisempfehlungen für Produkte im E-Commerce-Sortiment generieren.

Der Kern dieses Systems liegt in der Fähigkeit:

- **Preiselastizitäten zu ermitteln:** Mittels ML-Modellen sollen die Preissensitivitäten für einzelne Produkte oder Produktgruppen auf Basis historischer Verkaufs-, Preis-, Marketing- und Wettbewerbsdaten berechnet werden. *(Prototyp: [`src/model.py`](../src/model.py))*

- **Nachfrage zu prognostizieren:** Die Modelle sollen lernen, wie sich Preisänderungen unter Berücksichtigung anderer relevanter Faktoren (z.B. Saisonalität, Marketingaktivitäten) auf die verkaufte Menge auswirken. *(Prototyp: [`src/model.py → train_elasticity_model()`](../src/model.py))*

- **Automatisierte Preisempfehlungen abzuleiten:** Basierend auf den ermittelten Elastizitäten, Nachfrageprognosen sowie definierbaren Geschäftsregeln (z.B. Mindestmargen, Preisobergrenzen, Wettbewerbsorientierung) soll das System konkrete, optimierte Preisvorschläge generieren. *(Prototyp: [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py))*

Die prototypische Umsetzung in dieser Arbeit dient dazu, die technische Machbarkeit aufzuzeigen, die Methodik zu validieren und den potenziellen Nutzen eines solchen Systems greifbar zu machen. Sie legt den Grundstein für eine spätere, vollumfängliche Implementierung im produktiven Umfeld des Unternehmens.

> 📖 *Konkrete Ergebnisse der prototypischen Umsetzung: [MODELL_DOKUMENTATION.md → Kap. 6.4](MODELL_DOKUMENTATION.md#64-gesamtergebnis-aller-produkte-modeloutput)*

---

### 1.3 Relevanz und Kontext für einen international tätigen, mittelständischen Weltmarktführer

Die in den vorangegangenen Abschnitten skizzierte Problemstellung statischer Preisstrategien und die Zielsetzung der Entwicklung eines dynamischen, Machine-Learning-basierten Preisoptimierungssystems besitzen eine hohe strategische Relevanz für einen international tätigen, mittelständischen Weltmarktführer. Als etabliertes Unternehmen in verschiedenen Produkt-Bereichen agiert dieses Unternehmen in einem Marktumfeld, das zunehmend durch den Online-Handel und insbesondere durch große Plattformen wie Amazon geprägt wird. Um in diesem hochdynamischen Umfeld nicht nur zu bestehen, sondern auch Wachstumspotenziale voll auszuschöpfen und die Wettbewerbsfähigkeit langfristig zu sichern, sind fortschrittliche, datengesteuerte Ansätze unerlässlich.

Die Implementierung eines intelligenten Preisoptimierungssystems, wie es in dieser Arbeit konzipiert und prototypisch umgesetzt wird, bietet dem international tätigen, mittelständischen Branchenführer konkrete Vorteile:

**Maximierung von Umsatz und Marge:** Das Kernziel des Systems ist die direkte positive Beeinflussung zentraler betriebswirtschaftlicher Kennzahlen wie Umsatz (Turnover) und Nettomarge (Net Margin). Durch die Berücksichtigung von Preiselastizitäten und Nachfragemustern auf Produktebene können Preise so angepasst werden, dass sie je nach Marktsituation und Produktlebenszyklus entweder den Absatz maximieren oder die Profitabilität steigern.

**Steigerung der Wettbewerbsfähigkeit:** Im E-Commerce, speziell auf Plattformen mit hoher Preistransparenz wie Amazon, ist die Fähigkeit zur schnellen und fundierten Reaktion auf Wettbewerbsaktionen und Marktveränderungen entscheidend. Ein automatisiertes System ermöglicht es dem international tätigen, mittelständischen Branchenführer, agiler zu agieren als bei manuellen oder statischen Preisprozessen und somit Marktanteile zu sichern oder auszubauen.

**Effizienzsteigerung und Ressourcenschonung:** Die Automatisierung der Preisfindung reduziert den manuellen Aufwand im E-Commerce-Team (insbesondere dem Amazon-Team) und setzt Ressourcen frei, die für strategischere Aufgaben genutzt werden können.

**Förderung einer datengesteuerten Entscheidungskultur:** Die Entwicklung und Nutzung eines solchen Systems fördert das Verständnis und die Anwendung von Datenanalysen innerhalb des Unternehmens. Es liefert nicht nur Preisempfehlungen, sondern auch wertvolle Einblicke in das Kundenverhalten (z.B. Preissensitivität), die für Marketing, Produktmanagement und Controlling von Nutzen sind. Das Projekt hebt die Entscheidungsfindung im E-Commerce auf eine neue Stufe.

---

### 1.4 Begründung der Abgrenzung zum Data Analysten

Die Konzeption und prototypische Umsetzung dieses Preisoptimierungssystems dient auch als konkrete Begründung für die Notwendigkeit der Schaffung einer dezidierten Data Science Umgebung. Die Komplexität des Vorhabens – von der Integration heterogener Datenquellen über die anspruchsvolle Modellierung von Preiselastizitäten mittels Machine-Learning bis hin zur Operationalisierung und Visualisierung in einem BI-System – übersteigt klar den Aufgabenbereich traditioneller Data-Analystenrollen.

Das Projekt erfordert folgende Kompetenzen:

- **Machine-Learning:** Praktische Erfahrung in der Erstellung von ML-Modellen (z.B. mit Python und Bibliotheken wie scikit-learn) zur Lösung spezifischer Geschäftsprobleme wie Preisoptimierung und Elastizitätsberechnung.

- **Datenmanagement & -modellierung:** Tiefgehende Kenntnisse in ETL-Prozessen (PowerQuery, SSIS), SQL, DWH-Schichtenmodellen und analytischer Datenmodellierung (SSAS Tabular) zur Bereitstellung einer robusten Datengrundlage.

- **Business Intelligence:** Umfassende Erfahrung mit Datenvisualisierungstools wie Power BI und DAX zur Erstellung aussagekräftiger Dashboards und Reports für Fachanwender wie das Amazon-Team und das Controlling.

- **E-Commerce-Verständnis:** Ausgeprägtes Verständnis für die spezifischen Prozesse und KPIs im E-Commerce.

Das Projekt kann wegen folgenden Gründen abgegrenzt werden zu einem Data Analyst:

- **Komplexität:** Dieses Projekt erfordert nicht nur die Erstellung von Berichten, sondern die Entwicklung von Vorhersagemodellen (ML) und Optimierungsalgorithmen.

- **Technologien:** Es nutzt explizit fortgeschrittene Techniken und Werkzeuge (Python/scikit-learn für ML, SSAS für komplexe Modelle, SSIS für ETL), die über typische Analysten-Werkzeuge hinausgehen.

- **Fokus:** Der Schwerpunkt liegt auf prädiktiver (Was wird passieren?) und präskriptiver (Was sollte getan werden?) Analytik, statt primär auf deskriptiver (Was ist passiert?) Analyse.

- **Automatisierung & Systemdesign:** Es geht um den Aufbau eines automatisierten Systems, nicht nur um ad-hoc Analysen oder manuelle Berichte. Dies beinhaltet Aspekte des Data Engineerings und der Softwareentwicklung (Modell-Deployment).

- **Statistische Tiefe:** Erfordert ein tiefes Verständnis statistischer Methoden und Machine-Learning-Konzepte (Preiselastizität, Modellvalidierung, A/B-Testing).

Dieses Projekt fungiert somit als „Leuchtturmprojekt", das exemplarisch den Bedarf und den unmittelbaren Mehrwert eines dedizierten Data-Science-Setups für die Erreichung strategischer Ziele des international tätigen, mittelständischen Branchenführers im wichtigen Wachstumsfeld E-Commerce aufzeigt. Es demonstriert, wie durch die Anwendung fortgeschrittener Analytik (prädiktiv und präskriptiv) operative Prozesse optimiert und strategische Entscheidungen fundiert werden können. Die Anwendungsmöglichkeiten einer solchen technischen Umgebung geht über das Projektthema „dynamisches Preisoptimierungsmodell im E-Commerce" hinaus.

---

### 1.5 Theoretische Einordnung: Prädiktive und Präskriptive Analytik im Projektkontext

Die Nutzung von **prädiktiver Analytik** in diesem Projekt bedeutet konkret, dass mithilfe von Machine-Learning-Modellen zukünftige Ereignisse vorhergesagt werden – beispielsweise wie sich die Verkaufsmenge bei einer Preisänderung entwickeln wird (Schätzung der Preiselastizität) oder wie hoch die Nachfrage in der nächsten Periode sein könnte. Sie beantwortet die Frage: *„Was wird wahrscheinlich geschehen?"*

Die **präskriptive Analytik** geht einen entscheidenden Schritt weiter und bildet den Kern dieses Projekts zur Preisoptimierung. Sie nutzt die Ergebnisse der prädiktiven Modelle (z.B. die Elastizität), um unter Berücksichtigung definierter Geschäftsziele (wie Umsatz- oder Margenmaximierung) und Rahmenbedingungen (wie Wettbewerbspreise) konkrete Handlungsempfehlungen abzuleiten – hier also die optimalen Preisvorschläge. Sie beantwortet die Frage: *„Was sollten wir tun, um unser Ziel zu erreichen?"* Durch diese Verknüpfung greift das entwickelte System aktiv in die Geschäftssteuerung ein.

*(Prototyp-Implementierung: [`src/pricing_optimizer.py`](../src/pricing_optimizer.py) — siehe [MODELL_DOKUMENTATION.md Kap. 6](MODELL_DOKUMENTATION.md#6--preisempfehlung-präskriptive-analytik-studienarbeit-kap-44))*

Diese fortgeschrittenen Analysestufen bauen auf den grundlegenderen Stufen auf, die ebenfalls für das Geschäftsverständnis relevant sind:

Die **deskriptive Analytik** dient dazu, vergangene Ereignisse zusammenzufassen und zu visualisieren, um einen Überblick über die Geschäftsentwicklung zu geben. Ein typisches Beispiel hierfür ist ein Self-Service BI-System in Power BI, das dem Vertrieb (Sales), Produktmanagement und Controlling Kennzahlen wie den erzielten Umsatz, Deckungsbeitrag oder die verkaufte Menge für verschiedene Produkte und Kunden transparent macht. Sie beantwortet die Frage: *„Was ist passiert?"*

Die **diagnostische Analytik** baut auf der deskriptiven Analyse auf und versucht, die Ursachen für die beobachteten Ergebnisse zu ergründen. Nutzer des genannten Power BI-Systems könnten beispielsweise durch Drill-Downs, Filterung oder Vergleichsanalysen untersuchen, warum der Deckungsbeitrag einer Produktgruppe gesunken ist oder welche Faktoren zu einem Umsatzanstieg bei bestimmten Kunden geführt haben. Sie beantwortet die Frage: *„Warum ist es passiert?"*

Während deskriptive und diagnostische Analysen essenziell für das grundlegende Geschäftsverständnis und die Kontextualisierung sind (und oft durch PowerBI-Systeme wie das erwähnte abgedeckt werden), liegt der Fokus dieser Arbeit klar auf der Entwicklung prädiktiver Modelle und insbesondere präskriptiver Empfehlungen, um proaktiv und datengesteuert die Preisgestaltung zu optimieren.

---

### 1.6 Cross Industry Standard Process for Data Mining (CRISP-DM)

Der Cross Industry Standard Process for Data Mining (CRISP-DM) ist ein Standard für Datenanalyse-Prozesse, der einen strukturierten Rahmen für die Durchführung von Data-Mining-Projekten bietet. Er ermöglicht ein iteratives Vorgehen und das Wechseln zwischen verschiedenen Phasen.

*Figure 1-1: Cross Industry Standard Process for Data Mining (CRISP-DM), Quelle: Wikipedia, CC BY-SA 3.0*

Die sechs Phasen können, wie folgt, zusammengefasst werden:

- **Business Understanding:** In dieser Phase werden die Anforderungen und Zieldefinition ermittelt sowie eine Beschreibung der unternehmerischen Problemstellung erstellt.

- **Data Understanding:** Diese Phase umfasst die Datenerfassung, die Datenbeschreibung und das Untersuchen und Bewerten der Daten.

- **Data Preparation:** In dieser Phase werden die Daten bereinigt und transformiert in ein Zielformat.

- **Modeling:** Die Modeling Phase beschäftigt sich mit den Modellierungsverfahren. In der vorliegenden Arbeit wird darunter das Verfahren zum Erstellen eines „Datenmodells" verstanden.

- **Evaluation:** Während dieser Phase werden die Umsetzungen und Prozesse bewertet.

- **Deployment:** Diese Phase beschreibt die Bereitstellung der Implementierung aus der Entwicklungsumgebung in die produktiv genutzte Umgebung.

Nach jedem Kapitel wird die Einordnung in diesen CRISP-DM Standard erklärt.

> 📖 *Einordnung des Prototyps in CRISP-DM: [MODELL_DOKUMENTATION.md → Kap. 9](MODELL_DOKUMENTATION.md#9--crisp-dm-einordnung)*

---

## 2. Analyse der Ausgangslage und Datenanforderungen

*[Business Understanding / Data Understanding]*

### 2.1 Bestehende Preisprozesse und Herausforderungen im E-Commerce Team (insb. Amazon)

*Entwurf:*

- Hypothetische Beschreibung der aktuellen (vermutlich manuellen oder regelbasierten) Preisgestaltungsprozesse bei einem international tätigen, mittelständischen Branchenführer.
- Identifikation der damit verbundenen Herausforderungen (z.B. Zeitaufwand, Inkonsistenzen, verpasste Chancen).

---

### 2.2 Identifikation und Bewertung benötigter Datenquellen

#### 2.2.1 Interne Daten (Verkäufe, Lagerbestand, Produktdaten, ERP-Daten)

*Entwurf:*

- Auflistung der benötigten internen Daten (Verkäufe, Lagerbestand, Produktdaten, ERP-Daten).
- Bezug zur Prototyp-Umsetzung: Beschreibung der simulierten internen Daten (CSV-Format, Inhalt, Struktur).

> 📂 *Prototyp-Daten: [`data/produkte.csv`](../data/produkte.csv), [`data/verkaeufe.csv`](../data/verkaeufe.csv)*  
> 📄 *Datengenerierung: [`data/generate_data.py`](../data/generate_data.py)*  
> 📖 *Details: [MODELL_DOKUMENTATION.md → Kap. 2.1](MODELL_DOKUMENTATION.md#21--produktstammdaten)*

#### 2.2.2 Externe Daten (Wettbewerbspreise, Marketing-Plattformdaten z.B. Pacvue, Marktdaten)

*Entwurf:*

- Auflistung der benötigten externen Daten (Wettbewerbspreise, Marketing-Plattformdaten wie Pacvue, Marktdaten).
- Diskussion möglicher Beschaffungswege (APIs, Scraping).
- Bezug zur Prototyp-Umsetzung: Beschreibung der simulierten externen Daten (CSV-Format, Inhalt, Struktur, z.B. statische oder leicht variierende Wettbewerbspreise).

> 📂 *Prototyp-Daten: [`data/wettbewerbspreise.csv`](../data/wettbewerbspreise.csv)*

---

### 2.3 Anforderungen an Datenqualität, Granularität und Verfügbarkeit

*Entwurf:*

- Diskussion der Wichtigkeit von hoher Datenqualität (z.B. Abgleich Pacvue vs. interne).
- Festlegung der benötigten Granularität (z.B. tägliche Verkäufe/Preise).
- Anforderungen an die zeitliche Verfügbarkeit der Daten für ein operatives System.
- Bezug zur Prototyp-Umsetzung: Erläuterung, dass für den Prototyp Qualität und Verfügbarkeit durch die synthetischen Daten als gegeben angenommen wurden.

---

## 3. Datenintegration und -aufbereitung für die Preismodellierung *(Data Understanding / Data Preparation)*

### 3.1 Konzeption der ETL-Strecken zur Datenakquise und -integration

#### 3.1.1 Nutzung von PowerQuery und SQL Server Integration Services (SSIS)

*Entwurf:*

- Beschreibung der geplanten Nutzung von PowerQuery und SQL Server Integration Services (SSIS) im Zielsystem.

#### 3.1.2 Anbindung von APIs oder Scraping-Lösungen (für Wettbewerbsdaten)

*Entwurf:*

- Erläuterung der Anbindung von APIs oder Scraping-Lösungen für Wettbewerbsdaten.

*Prototyp-Umsetzung:* Detaillierte Beschreibung, wie die ETL-Strecke im Prototyp vereinfacht umgesetzt wurde:

- Laden der synthetischen CSV-Daten mittels Python (pandas).
- Alternativ/Ergänzend: Nutzung von Power Query in Power BI Desktop für Transformationen.
- Laden der vorbereiteten Daten in die lokale SQL Server Developer Edition Datenbank.
- Klarstellung, dass SSIS im Prototyp nicht verwendet wurde.

> 🐍 *Prototyp-Code: [`src/data_preparation.py → load_csv_to_db()`](../src/data_preparation.py)*  
> 🗄️ *SQL-Skripte: [`sql/create_tables.sql`](../sql/create_tables.sql) · [`sql/load_data.sql`](../sql/load_data.sql)*  
> 📖 *Details: [MODELL_DOKUMENTATION.md → Kap. 2.3](MODELL_DOKUMENTATION.md#23--etl-prozess)*

---

### 3.2 Aufbau und Erweiterung des Data Warehouse nach Schichtenmodell (Core, Bizcore, Datamart) für Pricing-Daten

#### 3.2.1 Datenmodellierung im Backend (SQL)

Ein zentraler Baustein für fortgeschrittene Analysen wie die dynamische Preisoptimierung ist ein robustes und gut strukturiertes Data Warehouse (DWH). Dieses dient als zentrale Sammelstelle, um Daten aus verschiedenen Quellsystemen zu integrieren, langfristig zu speichern und für Analysezwecke aufzubereiten. Im Gegensatz zu transaktionalen Quellsystemen (OLTP), wie ERP-Systeme, die für schnelle Lese- und Schreibvorgänge einzelner Datensätze optimiert sind, sind DWH-Systeme für komplexe Abfragen und Analysen über große Datenmengen ausgelegt.

Für das Data Warehouse, das auf einer Microsoft Azure Cloud SQL-Datenbank basiert, wird eine etablierte, mehrschichtige Architektur verwendet. Diese Struktur fördert die Nachvollziehbarkeit, Wartbarkeit und Flexibilität des Systems. Der Datenfluss folgt dabei einem ELT-Prozess (Extract-Load-Transform), bei dem Daten zunächst extrahiert, dann in das DWH geladen und erst dort transformiert werden. Die wesentlichen Schichten sind:

- **Staging-Schicht:** Die erste Anlaufstelle für Daten aus den Quellsystemen (z.B. ERP). Hier werden die Rohdaten unverändert abgelegt.

- **Cleanse-Schicht:** In dieser Schicht erfolgen erste Datenbereinigungen und Validierungen. Fehlerhafte oder unvollständige Daten werden identifiziert und behandelt. Techniken wie Lookups zur Auflösung von Fremdschlüssel-Beziehungen und das Logging von Fehlern kommen hier zum Einsatz, oft gesteuert durch SSIS-Pipelines.

- **Core-Schicht:** Diese Schicht bildet das Fundament des DWH. Hier werden die bereinigten Daten aus verschiedenen Quellen integriert und in einem stabilen, konsistenten Modell abgelegt. Eine wesentliche Aufgabe ist die Historisierung von Datenänderungen, typischerweise nach dem Prinzip der Slowly Changing Dimensions Typ 2 (SCD II). Dabei wird für jeden Datensatz ein Gültigkeitszeitraum und Status verwaltet, um Änderungen nachvollziehbar zu machen. Dies wird oft über Gespeicherte Prozeduren (Stored Procedures) in der SQL-Datenbank umgesetzt. Zudem werden hier Datenbeziehungen über Primär- und Fremdschlüssel definiert.

- **Bizcore-Schicht (Business Core):** Diese Schicht enthält die eigentliche Geschäftslogik. Hier werden Daten aus verschiedenen Vorsystemen zu einer einheitlichen Sicht zusammengeführt (z.B. ein „Konzern-Kundenstamm") und anwendungsspezifische Berechnungen durchgeführt. Beispielsweise kann hier der Deckungsbeitrag für Verkäufe ermittelt werden, indem auf historisierte Kostenkomponenten (wie den Konzern-Einstandspreis zum Belegdatum) aus der Core-Schicht zurückgegriffen wird. Die Transformationen in dieser Schicht erfolgen ebenfalls häufig über Gespeicherte Prozeduren.

- **Datamart-Schicht:** Die oberste Schicht stellt spezifische Datensichten für definierte Anwendungsbereiche oder Nutzergruppen bereit (z.B. ein Pricing-Datamart). Die Daten sind hier oft in einem dimensionalen Modell (z.B. Sternschema) aufbereitet, das für Analysewerkzeuge wie Power BI oder SSAS Tabular Models optimiert ist. Diese Schicht bildet die direkte Grundlage für Reports und Dashboards.

Der gesamte ELT-Prozess wird technologisch durch Microsoft SQL Server Integration Services (SSIS) für die Transformationslogik (teilweise direkt in SSIS, teilweise durch Aufruf von Stored Procedures in der Datenbank) und durch die Azure Data Factory für die Orchestrierung (zeitliche Steuerung der Lade- und Transformationsprozesse, z.B. nächtliche Läufe) unterstützt.

Die Kenntnis dieses Schichtenmodells und der zugrundeliegenden Prozesse ist essenziell für den Aufbau einer Data Science Umgebung.

> 🗄️ *SQL-Tabellenstruktur (Prototyp): [`sql/create_tables.sql`](../sql/create_tables.sql)*

#### 3.2.2 Maßnahmen zur Sicherstellung der Datenqualität (z.B. Abgleich Pacvue vs. interne Daten)

Im Rahmen dieser Studienarbeit und der prototypischen Umsetzung konnte aufgrund fehlenden Zugriffs auf die produktive Quellsysteme des international tätigen, mittelständischen Branchenführers sowie zur Vereinfachung nicht die volle Tiefe der beschriebenen Ziel-Architektur abgebildet werden. Stattdessen wurde das DWH-Konzept wie folgt simuliert:

- **Datenbank:** Eine einzelne Datenbank (PricingPrototypeDB) wurde auf einer lokalen SQL Server Developer Edition Instanz erstellt. Diese diente als Container für alle Tabellen des Prototyps.

- **Quellen & Staging/Cleanse:** Synthetische Beispieldaten wurden in Form von CSV-Dateien erstellt. Das Laden dieser Daten in die SQL-Tabellen (z.B. `dbo.Produkte`, `dbo.Verkaeufe`, `dbo.Wettbewerbspreise`) mittels einfacher SQL-Skripte (BULK INSERT) oder des SSMS Import/Export-Assistenten simulierte den Staging-Prozess und grundlegende Cleansing-Aspekte (durch die angenommene Qualität der synthetischen Daten).

- **Core/Bizcore:** Die Integration der Daten erfolgte durch das Definieren von Tabellenstrukturen und Beziehungen direkt in der SQL-Datenbank bzw. später im Datenmodell von Power BI. Komplexe Transformationen und Berechnungen, die typischerweise in der Bizcore-Schicht stattfinden (z.B. Feature Engineering), wurden im Prototyp primär in Python durchgeführt (siehe [Kapitel 3.3](#33-feature-engineering-mittels-python-pandas-numpy-und-sql)). Eine explizite Historisierung (SCD II) wurde im SQL-Teil des Prototyps nicht implementiert.

- **Datamart:** Die für die Analyse in Power BI genutzten Tabellen, inklusive der Tabelle mit den Modellergebnissen (`dbo.ModelOutput`), können als Simulation der Datamart-Schicht betrachtet werden, da sie die aufbereitete Datengrundlage für den spezifischen Anwendungsfall (Pricing-Analyse und -Modellierung) darstellten.

- **ELT-Werkzeuge:** Statt SSIS und Azure Data Factory wurden für den Prototyp Python (pandas) für Datenaufbereitung und -ladung sowie der SSMS Import/Export-Assistent verwendet. Die Ausführung erfolgte manuell.

Diese Simulation erlaubte es, den konzeptionellen Datenfluss von der Quelle über eine (vereinfachte) zentrale Speicherung und Transformation bis hin zur Analyse nachzubilden, auch wenn die technische Ausprägung der einzelnen DWH-Schichten stark vereinfacht wurde.

---

### 3.3 Feature Engineering mittels Python (pandas, numpy) und SQL

#### 3.3.1 Erstellung relevanter Merkmale (z.B. Zeitmerkmale, Preisindizes, Marketing-Einflüsse, rollierende Kennzahlen)

*Entwurf:*

- Auflistung und Erklärung von Beispielen (Zeitmerkmale, Preisindizes, Marketing-Einflüsse, rollierende Kennzahlen etc.).
- Beschreibung der Umsetzung im Prototyp mittels Python (pandas/numpy) auf den DataFrames.

> 🐍 *Prototyp-Code: [`src/data_preparation.py → build_feature_dataframe()`](../src/data_preparation.py)*  
> 📖 *Feature-Tabelle mit allen Merkmalen: [MODELL_DOKUMENTATION.md → Kap. 3](MODELL_DOKUMENTATION.md#3--feature-engineering-studienarbeit-kap-33)*

#### 3.3.2 Transformation von Daten für Modellierungszwecke (z.B. Log-Transformation)

*Entwurf:*

- Erläuterung notwendiger Transformationen (z.B. Log-Transformation, Skalierung).
- Beschreibung der im Prototyp durchgeführten Transformationen (Datentypen, einfache Berechnungen).

> 📖 *Theoretischer Hintergrund zur Log-Transformation: [MODELL_DOKUMENTATION.md → Kap. 4.1](MODELL_DOKUMENTATION.md#41--theoretischer-hintergrund)*

---

## 4. Entwicklung der Machine-Learning-Modelle zur Preisoptimierung *(Modeling)*

### 4.1 Auswahl geeigneter Modellierungsansätze

*Entwurf:*

- Modelle zur Schätzung der Preiselastizität (z.B. Regressionsmodelle)
- Modelle zur Nachfrageprognose (z.B. Zeitreihenanalyse, weitere Regressionsmodelle)
- Begründung der Auswahl für den Prototyp: Fokus auf Preiselastizität mittels (vereinfachter) Regression

> 📖 *Gewählter Ansatz im Prototyp: [MODELL_DOKUMENTATION.md → Kap. 4](MODELL_DOKUMENTATION.md#4--ml-modell-preiselastizität-studienarbeit-kap-4)*

---

### 4.2 Implementierung der Modelle in Python

#### 4.2.1 Nutzung von Bibliotheken

*Entwurf:*

- Detaillierte Beschreibung der Verwendung von scikit-learn für die Modellierung, pandas für Datenmanipulation und numpy für numerische Operationen.
- Erwähnung der Entwicklungsumgebung (Jupyter Notebook via Anaconda).
- Bezug zu Python/ML-Skills.

> 🐍 *Prototyp-Code: [`src/model.py`](../src/model.py)*  
> 📓 *End-to-End Notebook: [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)*  
> 📖 *Implementierungsdetails: [MODELL_DOKUMENTATION.md → Kap. 4.2](MODELL_DOKUMENTATION.md#42--implementierung)*

#### 4.2.2 Umgang mit produkt- oder kategoriespezifischen Unterschieden

*Entwurf:*

- Diskussion von Strategien (separate Modelle, Kategorie als Feature).
- Beschreibung des gewählten Ansatzes im Prototyp (z.B. ein Modell mit Produkt-ID als Feature oder separate Modelle, falls die synthetischen Daten dies zuließen).

---

### 4.3 Training, Validierung und Auswahl der Modelle

#### 4.3.1 Aufteilung in Trainings-, Validierungs- und Testdaten

*Entwurf:*

- Erläuterung des Prinzips (z.B. Hold-out, Zeitreihen-Split).
- Beschreibung der Umsetzung mit den synthetischen Daten im Prototyp.

> 📖 *Verwendeter Zeitreihen-Split (80/20): [MODELL_DOKUMENTATION.md → Kap. 4.2](MODELL_DOKUMENTATION.md#42--implementierung)*

#### 4.3.2 Metriken zur Bewertung der Modellgüte

*Entwurf:*

- Vorstellung relevanter Metriken (z.B. R², Adjusted R², MAE, RMSE für Regression).
- Erklärung, wie diese mit scikit-learn berechnet wurden.

> 📖 *Konkrete Metrikwerte (R², MAE, RMSE): [MODELL_DOKUMENTATION.md → Kap. 7.1](MODELL_DOKUMENTATION.md#71--modellgüte-metriken-testset-zeitreihen-split-8020)*

---

### 4.4 Ableitung von Preisempfehlungen aus den Modellergebnissen

*Entwurf:*

- Konzeptionelle Überlegungen: Wie können Elastizitäten und Prognosen in konkrete Preisvorschläge überführt werden (unter Berücksichtigung von Business Rules, Margenzielen, Wettbewerb)?
- Umsetzung im Prototyp: Beschreibung des vereinfachten Ansatzes, z.B. Interpretation des Preiskoeffizienten als Elastizität, einfache Regel zur Preisanpassung basierend auf Elastizität und Wettbewerbspreis.
- Speicherung der Ergebnisse (z.B. Elastizität, Vorschlag) in der SQL-Datenbanktabelle `dbo.ModelOutput`.

> 🐍 *Prototyp-Code: [`src/pricing_optimizer.py → recommend_price()`](../src/pricing_optimizer.py)*  
> 📖 *Amoroso-Robinson-Relation und Business Rules: [MODELL_DOKUMENTATION.md → Kap. 6](MODELL_DOKUMENTATION.md#6--preisempfehlung-präskriptive-analytik-studienarbeit-kap-44)*

---

## 5. Evaluation und Validierung der Preisstrategie *(Evaluation)*

### 5.1 Technische Evaluation der Modellergebnisse und Elastizitäten

*Entwurf:*

- Analyse der Modellgüte anhand der in [Kapitel 4.3.2](#432-metriken-zur-bewertung-der-modellgüte) definierten Metriken.
- Plausibilitätsprüfung der berechneten Elastizitäten (Vorzeichen, Größenordnung) im Kontext der (simulierten) Produkte.

> 📖 *Modellgüte und Plausibilitätsprüfung: [MODELL_DOKUMENTATION.md → Kap. 7](MODELL_DOKUMENTATION.md#7--ergebnisse--evaluation-studienarbeit-kap-5)*

---

### 5.2 Konzeption und Simulation von A/B-Tests im E-Commerce Kontext

*Entwurf:*

- Erläuterung der Wichtigkeit von A/B-Tests zur Validierung von Preisänderungen im realen Umfeld.
- Beschreibung eines möglichen A/B-Test Designs für einen international tätigen, mittelständischen Branchenführer auf Amazon.
- Diskussion, wie die Ergebnisse solcher Tests zur Modellverbesserung genutzt werden könnten. Betonung, dass dies im Prototyp nur konzeptionell behandelt werden kann.

> 📖 *A/B-Test Konzept: [MODELL_DOKUMENTATION.md → Kap. 7.3](MODELL_DOKUMENTATION.md#73--ab-test-konzept--studienarbeit-kap-52)*

---

### 5.3 Bewertung der Auswirkungen auf die Geschäftsziele (Umsatz, Marge)

*Entwurf:*

- Methoden zur Messung des Impacts im Live-Betrieb (Vergleich Test- vs. Kontrollgruppe, Zeitreihenvergleich).
- Simulation im Prototyp: Beschreibung, wie in Power BI (mittels DAX) der simulierte Effekt der Preisvorschläge auf Umsatz und Marge dargestellt wurde.

> 📖 *Konkrete ΔUmsatz- und ΔMarge-Berechnungen: [MODELL_DOKUMENTATION.md → Kap. 6.3](MODELL_DOKUMENTATION.md#63--konkrete-berechnung-für-alle-produkte-stand-31122023)*

---

### 5.4 Iterative Verbesserung der Modelle basierend auf Evaluationsergebnissen

*Entwurf:*

- Diskussion der Notwendigkeit eines kontinuierlichen Verbesserungsprozesses (Monitoring, Retraining, Feature-Anpassung).

---

## 6. Operationalisierung und Monitoring im BI-System *(Deployment)*

### 6.1 Bereitstellung der Modellergebnisse

*Entwurf:*

- Diskussion verschiedener Optionen für das Zielsystem: Speicherung im DWH für das Modell-Deployment.
- Umsetzung im Prototyp: Einfache Speicherung der Ergebnisse (Elastizitäten, Preisvorschläge) in einer Tabelle (`dbo.ModelOutput`) der SQL Server Datenbank.

> 🐍 *Prototyp-Code: [`src/pricing_optimizer.py → save_recommendations()`](../src/pricing_optimizer.py)*  
> 📖 *dbo.ModelOutput Schema: [MODELL_DOKUMENTATION.md → Kap. 8.1](MODELL_DOKUMENTATION.md#81--dbomodelouput)*

---

### 6.2 Aufbau eines analytischen Datenmodells (Tabular Model in SSAS) für das Frontend

#### 6.2.1 Definition von Dimensionen, Fakten und Hierarchien für Pricing-Analysen

*Entwurf:*

- Ziel-Architektur: Beschreibung der Nutzung von SQL Server Analysis Services (SSAS) Tabular für performante Analysen.
- Bezug zum Skillset.
- Prototyp-Umsetzung: Erläuterung, wie Power BI Desktop intern die gleiche Engine (VertiPaq) wie SSAS Tabular nutzt und somit das Datenmodell in Power BI als Prototyp des Tabular Models dient.
- Beschreibung der im Power BI Prototyp erstellten Tabellenbeziehungen und des Modells (Sternschema/Schneeflocke).

#### 6.2.2 Implementierung relevanter Kennzahlen mittels DAX

*Entwurf:*

- Auflistung und Erklärung der im Power BI Prototyp erstellten DAX-Measures (z.B. Turnover, Net Margin (simuliert), Durchschnittspreis, Anzeige Elastizität/Preisvorschlag).
- Betonung der Bedeutung von DAX-Kenntnissen.

---

### 6.3 Entwicklung von Power BI Dashboards und Reports

#### 6.3.1 Visualisierung von Preisempfehlungen und deren Einflussfaktoren

*Entwurf:*

- Beschreibung der im Prototyp erstellten Dashboards/Berichtsseiten in Power BI Desktop.
- Beispiele für Visualisierungen (Trends, Vergleiche, Elastizitätsanzeige).

> 📓 *Dashboard-Implementierung: [`notebooks/dynamic_pricing_prototype.ipynb`](../notebooks/dynamic_pricing_prototype.ipynb)*  
> 📖 *Dashboard-Seiten: [MODELL_DOKUMENTATION.md → Kap. 8.2](MODELL_DOKUMENTATION.md#82--dashboard-power-bi-prototyp)*

![Dashboard-Vorschau](../dashboard_preview.png)

#### 6.3.2 Monitoring der Preisentwicklung und Modell-Performance

*Entwurf:*

- Darstellung, wie das Prototyp-Dashboard zur (simulierten) Überwachung der KPIs und Modelloutputs dient.

#### 6.3.3 Bereitstellung von Analysewerkzeugen für das Amazon-Team und Controlling

*Entwurf:*

- Positionierung des Power BI Prototyps als Beispiel für ein solches Werkzeug.

---

### 6.4 Überlegungen zur Automatisierung des Gesamtprozesses

*Entwurf:*

- Diskussion der Notwendigkeit der Automatisierung im Zielsystem (Datenaktualisierung, Modell-Retraining, Reporting-Refresh).
- Skizzierung möglicher Tools und Techniken (z.B. SQL Server Agent, Azure Data Factory, Python-Skripte, Power BI Scheduled Refresh).
- Klarstellung, dass der Prototyp manuell ausgeführt wurde.

> 📖 *Erweiterungen im Zielsystem: [README.md → Erweiterungen (Zielsystem)](../README.md#erweiterungen-zielsystem)*

---

## 7. Zusammenfassung und Ergebnisse

### 7.1 Darstellung des entwickelten Systems

*Entwurf:*

- Kurze Zusammenfassung des im Prototyp realisierten End-to-End Datenflusses und der Komponenten (Synthetische Daten → SQL Server → Python/scikit-learn → SQL Server → Power BI).

> 📖 *Systemarchitektur-Überblick: [MODELL_DOKUMENTATION.md → Kap. 1](MODELL_DOKUMENTATION.md#1--systemarchitektur--datenfluss) und [README.md → Systemüberblick](../README.md#systemüberblick)*

---

### 7.2 Zusammenfassung der Kernergebnisse

*Entwurf:*

- Präsentation der wichtigsten simulierten Ergebnisse des Prototyps (z.B. Beispiel-Elastizitäten für ausgewählte Produkte, Darstellung der Preisvorschläge, simulierte KPI-Auswirkungen im Dashboard).

> 📖 *Vollständige Ergebnistabelle (ModelOutput): [MODELL_DOKUMENTATION.md → Kap. 6.4](MODELL_DOKUMENTATION.md#64-gesamtergebnis-aller-produkte-modeloutput)*

Die wichtigsten Ergebnisse des Prototyps (Produktionslauf mit `SEED=42`, Verkaufsjahr 2023):

| Produkt | ε | R² | Ist-Preis | Wettbewerbspr. | Empf. Preis | ΔMenge | ΔUmsatz | ΔMarge |
|---|---|---|---|---|---|---|---|---|
| P001 | −1,18 | 0,61 | 63,57 € | 62,67 € | **76,28 €** | −23,6 % | −8,4 % | **+5,3 %** |
| P002 | −1,05 | 0,42 | 102,71 € | 98,27 € | **104,97 €** | −2,3 % | −0,2 % | **+1,9 %** |
| P003 | −1,32 | 0,57 | 24,63 € | 22,99 € | **29,56 €** | −26,4 % | −11,6 % | **−1,6 %** |
| P004 | −0,52 | 0,50 | 30,39 € | 38,72 € | **33,95 €** | −6,2 % | +4,9 % | **+15,6 %** |
| P005 | −0,66 | 0,44 | 45,37 € | 49,96 € | **48,33 €** | −4,3 % | +2,0 % | **+6,9 %** |

---

### 7.3 Beitrag zur datengesteuerten Entscheidungsfindung und Erreichung strategischer Ziele

*Entwurf:*

- Betonung, wie das (auch im Prototyp gezeigte) System die Entscheidungsfindung im E-Commerce verbessern kann.

---

### 7.4 Ausblick auf mögliche Weiterentwicklungen und Limitationen

*Entwurf:*

- Kritische Reflexion der Limitationen des Prototyps (synthetische Daten, einfache Modelle, keine echten A/B-Tests, manuelle Prozesse).
- Skizzierung von Weiterentwicklungsmöglichkeiten (Einsatz echter Daten, komplexere Modelle, Implementierung von A/B-Tests, Automatisierung, Nutzung von Cloud-Diensten).
- Abschließende Bekräftigung der Notwendigkeit einer dedizierten Data Scientist Umgebung.

> 📖 *Geplante Erweiterungen im Zielsystem: [README.md → Erweiterungen (Zielsystem)](../README.md#erweiterungen-zielsystem)*

---

## Abbildungsverzeichnis

*Figure 1-1: Cross Industry Standard Process for Data Mining (CRISP-DM), Quelle: Wikipedia, CC BY-SA 3.0 — Seite 8*

---

## Literaturverzeichnis

1. IBCS Association, *International Business Communication Standards (IBCS)*, Version 1.2

2. Microsoft Learn Portal, *Datentypen (Transact-SQL)*, <https://learn.microsoft.com/de-de/sql/t-sql/data-types/data-types-transact-sql?view=sql-server-ver16> (abgerufen am 04.03.2024)

3. Microsoft Learn Portal, *„PowerBI usage scenarios"*, <https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-overview> (abgerufen am 04.03.2024)

4. Microsoft Learn Portal, *„PowerBI usage scenarios: Customizable managed self-service BI"*, <https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-usage-scenario-customizable-managed-self-service-bi> (abgerufen am 04.03.2024)

---

*Letzte Aktualisierung: Markdown-Konvertierung des Original-Dokuments ([`Studienarbeit Dynamisches Preisoptimierungsmodell im eCommerce- Andreas Traut.docx`](../Studienarbeit%20Dynamisches%20Preisoptimierungsmodell%20im%20eCommerce-%20Andreas%20Traut.docx))*
