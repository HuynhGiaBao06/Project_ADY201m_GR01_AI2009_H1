-- PostgreSQL / Neon cleaned view for downstream ingestion.
-- View used by data_ingestion.py: vw_cleaning_data

CREATE OR REPLACE VIEW vw_cleaning_data AS
SELECT
    "ID",
    CASE
        WHEN LOWER(TRIM("Churn"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("Churn"::text)) IN ('0', 'no', 'false') THEN 0
        ELSE NULL
    END AS "Churn",
    CASE
        WHEN LOWER(TRIM("SeniorCitizen"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("SeniorCitizen"::text)) IN ('0', 'no', 'false') THEN 0
        ELSE NULL
    END AS "SeniorCitizen",
    CASE
        WHEN LOWER(TRIM("Partner"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("Partner"::text)) IN ('0', 'no', 'false') THEN 0
        ELSE NULL
    END AS "Partner",
    "Dependents",
    NULLIF("Tenure"::text, '')::integer AS "Tenure",
    "Contract",
    "PaymentMethod",
    CASE
        WHEN LOWER(TRIM("PaperlessBilling"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("PaperlessBilling"::text)) IN ('0', 'no', 'false') THEN 0
        ELSE NULL
    END AS "PaperlessBilling",
    NULLIF("MonthlyCharges"::text, '')::numeric AS "MonthlyCharges",
    NULLIF("TotalCharges"::text, '')::numeric AS "TotalCharges",
    "InternetService",
    CASE
        WHEN LOWER(TRIM("OnlineSecurity"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("OnlineSecurity"::text)) IN ('0', 'no', 'false', 'no internet service', 'no phone service') THEN 0
        ELSE NULL
    END AS "OnlineSecurity",
    CASE
        WHEN LOWER(TRIM("OnlineBackup"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("OnlineBackup"::text)) IN ('0', 'no', 'false', 'no internet service', 'no phone service') THEN 0
        ELSE NULL
    END AS "OnlineBackup",
    CASE
        WHEN LOWER(TRIM("DeviceProtection"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("DeviceProtection"::text)) IN ('0', 'no', 'false', 'no internet service', 'no phone service') THEN 0
        ELSE NULL
    END AS "DeviceProtection",
    CASE
        WHEN LOWER(TRIM("TechSupport"::text)) IN ('1', 'yes', 'true') THEN 1
        WHEN LOWER(TRIM("TechSupport"::text)) IN ('0', 'no', 'false', 'no internet service', 'no phone service') THEN 0
        ELSE NULL
    END AS "TechSupport"
FROM db_predictive_churn;
