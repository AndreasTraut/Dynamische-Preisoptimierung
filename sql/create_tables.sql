-- ============================================================
-- Skript: create_tables.sql
-- Zweck:  Erstellt alle Tabellen der PricingPrototypeDB
--         (kompatibel mit SQL Server Developer Edition)
--
-- Schichtenmodell:
--   dbo.Produkte          -> Core / Stammdaten
--   dbo.Verkaeufe         -> Core / Faktdaten
--   dbo.Wettbewerbspreise -> Core / Externe Daten
--   dbo.ModelOutput       -> Datamart / Modellergebnisse
-- ============================================================

-- Datenbank anlegen (bei Bedarf auskommentieren / anpassen)
-- CREATE DATABASE PricingPrototypeDB;
-- GO
-- USE PricingPrototypeDB;
-- GO

-- ------------------------------------------------------------
-- Core: Produktstammdaten
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.Produkte', 'U') IS NOT NULL
    DROP TABLE dbo.Produkte;

CREATE TABLE dbo.Produkte (
    produkt_id      NVARCHAR(10)   NOT NULL PRIMARY KEY,
    name            NVARCHAR(100)  NOT NULL,
    kategorie       NVARCHAR(50)   NOT NULL,
    einstandspreis  DECIMAL(10, 2) NOT NULL,
    mindestpreis    DECIMAL(10, 2) NOT NULL,
    listenpreis     DECIMAL(10, 2) NOT NULL,
    gueltig_von     DATE           NOT NULL DEFAULT GETDATE(),
    gueltig_bis     DATE           NULL,          -- NULL = aktueller Satz (SCD II)
    ist_aktuell     BIT            NOT NULL DEFAULT 1
);
GO

-- ------------------------------------------------------------
-- Core: Verkaufsdaten (täglich je Produkt)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.Verkaeufe', 'U') IS NOT NULL
    DROP TABLE dbo.Verkaeufe;

CREATE TABLE dbo.Verkaeufe (
    verkauf_id   INT            NOT NULL PRIMARY KEY,
    produkt_id   NVARCHAR(10)   NOT NULL,
    datum        DATE           NOT NULL,
    menge        INT            NOT NULL,
    preis        DECIMAL(10, 2) NOT NULL,
    umsatz       DECIMAL(12, 2) NOT NULL,
    CONSTRAINT fk_verkaeufe_produkt FOREIGN KEY (produkt_id)
        REFERENCES dbo.Produkte (produkt_id)
);
GO

CREATE NONCLUSTERED INDEX ix_verkaeufe_datum
    ON dbo.Verkaeufe (datum);
GO

-- ------------------------------------------------------------
-- Core: Wettbewerbspreise (wöchentlich je Produkt)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.Wettbewerbspreise', 'U') IS NOT NULL
    DROP TABLE dbo.Wettbewerbspreise;

CREATE TABLE dbo.Wettbewerbspreise (
    id                INT            NOT NULL IDENTITY(1,1) PRIMARY KEY,
    produkt_id        NVARCHAR(10)   NOT NULL,
    datum             DATE           NOT NULL,
    wettbewerbspreis  DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_wettbewerb_produkt FOREIGN KEY (produkt_id)
        REFERENCES dbo.Produkte (produkt_id)
);
GO

-- ------------------------------------------------------------
-- Datamart: Modellergebnisse (Output des ML-Modells)
-- ------------------------------------------------------------
IF OBJECT_ID('dbo.ModelOutput', 'U') IS NOT NULL
    DROP TABLE dbo.ModelOutput;

CREATE TABLE dbo.ModelOutput (
    output_id               INT            NOT NULL IDENTITY(1,1) PRIMARY KEY,
    produkt_id              NVARCHAR(10)   NOT NULL,
    berechnungsdatum        DATETIME       NOT NULL DEFAULT GETDATE(),
    preiselastizitaet       DECIMAL(8, 4)  NOT NULL,
    modell_r2               DECIMAL(6, 4)  NULL,
    aktueller_preis         DECIMAL(10, 2) NOT NULL,
    wettbewerbspreis        DECIMAL(10, 2) NULL,
    empfohlener_preis       DECIMAL(10, 2) NOT NULL,
    erwartete_mengenänderung DECIMAL(8, 4) NULL,
    erwartete_umsatzaenderung DECIMAL(8, 4) NULL,
    erwartete_margenänderung  DECIMAL(8, 4) NULL,
    CONSTRAINT fk_output_produkt FOREIGN KEY (produkt_id)
        REFERENCES dbo.Produkte (produkt_id)
);
GO

PRINT 'Tabellen erfolgreich erstellt.';
