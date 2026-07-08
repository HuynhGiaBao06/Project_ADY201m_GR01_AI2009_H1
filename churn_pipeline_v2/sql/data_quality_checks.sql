-- Active: 1783414455395@@ep-quiet-queen-aop3s0b5-pooler.c-2.ap-southeast-1.aws.neon.tech@5432@neondb
-- PostgreSQL / Neon data quality checks for vw_cleaning_data.

-- 1. Duplicate or missing customer IDs.
SELECT
    "ID",
    COUNT(*) AS duplicate_count
FROM vw_cleaning_data
GROUP BY "ID"
HAVING COUNT(*) > 1 OR "ID" IS NULL;
-- 2. Missing values in critical modeling/dashboard columns.
SELECT
    "ID",
    "Churn",
    "Tenure",
    "MonthlyCharges",
    "TotalCharges",
    "InternetService"
FROM vw_cleaning_data
WHERE "Churn" IS NULL
   OR "Tenure" IS NULL
   OR "MonthlyCharges" IS NULL
   OR "TotalCharges" IS NULL
   OR "InternetService" IS NULL;
-- 3. Inconsistent tenure and total charges relationships.
SELECT
    "ID",
    "Tenure",
    "MonthlyCharges",
    "TotalCharges"
FROM vw_cleaning_data
WHERE ("Tenure" = 0 AND "TotalCharges" <> 0)
   OR ("Tenure" > 0 AND "TotalCharges" = 0);
