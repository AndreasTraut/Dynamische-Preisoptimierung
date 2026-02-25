-- ============================================================
-- Skript: load_data.sql
-- Zweck:  Lädt die synthetischen CSV-Daten in die
--         PricingPrototypeDB-Tabellen (SQL Server BULK INSERT).
--
-- Hinweis: Passe den Pfad '<PFAD_ZUM_DATA_VERZEICHNIS>' an
--          dein lokales Verzeichnis an.
-- ============================================================

-- USE PricingPrototypeDB;
-- GO

DECLARE @DataDir NVARCHAR(500) = '<PFAD_ZUM_DATA_VERZEICHNIS>\';

-- ------------------------------------------------------------
-- Produkte laden
-- ------------------------------------------------------------
TRUNCATE TABLE dbo.Verkaeufe;          -- FK-Reihenfolge beachten
TRUNCATE TABLE dbo.Wettbewerbspreise;
TRUNCATE TABLE dbo.ModelOutput;
DELETE FROM dbo.Produkte;

BULK INSERT dbo.Produkte
FROM '<PFAD_ZUM_DATA_VERZEICHNIS>\produkte.csv'
WITH (
    FIRSTROW        = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '\n',
    TABLOCK
);

-- Die CSV hat 6 Spalten (ohne gueltig_von / gueltig_bis / ist_aktuell)
-- -> Defaultwerte greifen automatisch.

-- ------------------------------------------------------------
-- Verkäufe laden
-- ------------------------------------------------------------
BULK INSERT dbo.Verkaeufe
FROM '<PFAD_ZUM_DATA_VERZEICHNIS>\verkaeufe.csv'
WITH (
    FIRSTROW        = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '\n',
    TABLOCK
);

-- ------------------------------------------------------------
-- Wettbewerbspreise laden
-- ------------------------------------------------------------
BULK INSERT dbo.Wettbewerbspreise
FROM '<PFAD_ZUM_DATA_VERZEICHNIS>\wettbewerbspreise.csv'
WITH (
    FIRSTROW        = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR   = '\n',
    TABLOCK
);

SELECT 'Produkte'          AS tabelle, COUNT(*) AS zeilen FROM dbo.Produkte
UNION ALL
SELECT 'Verkaeufe',                    COUNT(*) FROM dbo.Verkaeufe
UNION ALL
SELECT 'Wettbewerbspreise',            COUNT(*) FROM dbo.Wettbewerbspreise;
GO
