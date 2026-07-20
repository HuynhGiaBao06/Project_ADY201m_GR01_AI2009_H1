-- PostgreSQL / Neon schema for the ADY201m churn project.
-- Upload/staging table used by the Python upload flow: db_predictive_churn
-- Column names intentionally match the current CSV header created by pandas upload.

CREATE TABLE IF NOT EXISTS db_predictive_churn (
    "ID" TEXT PRIMARY KEY,
    "Churn" SMALLINT,
    "SeniorCitizen" SMALLINT,
    "Partner" TEXT,
    "Dependents" TEXT,
    "Tenure" INTEGER,
    "Contract" TEXT,
    "PaymentMethod" TEXT,
    "PaperlessBilling" TEXT,
    "MonthlyCharges" NUMERIC(10, 2),
    "TotalCharges" NUMERIC(12, 2),
    "InternetService" TEXT,
    "OnlineSecurity" TEXT,
    "OnlineBackup" TEXT,
    "DeviceProtection" TEXT,
    "TechSupport" TEXT,
    "tenure_group" TEXT,
    "service_diversity" INTEGER,
    "monthly_charges_ratio" NUMERIC,
    "is_paperless_electronic" TEXT
);

-- Optional destructive reset for local development only.
-- DROP TABLE IF EXISTS db_predictive_churn;
