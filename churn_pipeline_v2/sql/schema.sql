-- Active: 1783414455395@@ep-quiet-queen-aop3s0b5-pooler.c-2.ap-southeast-1.aws.neon.tech@5432@neondb
-- PostgreSQL / Neon schema for the ADY201m churn refactor.
-- Legacy SQL Server table: dbo.Predictive_Customer_Churn_DB
-- Refactor upload/staging table used by Python upload flow: db_predictive_churn
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
