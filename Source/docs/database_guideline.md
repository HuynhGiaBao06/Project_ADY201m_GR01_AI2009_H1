# Database Guideline

## 1. Purpose

This document describes the canonical database architecture for the churn project. The project uses PostgreSQL hosted on Neon.tech.

## 2. Database Architecture

```text
Raw customer data
→ PostgreSQL / Neon staging layer
→ db_predictive_churn
→ vw_cleaning_data
→ ingestion and checkpoint pipeline
```

The main objects are:

* `db_predictive_churn`: staging table that receives the 7,043-row customer dataset.
* `vw_cleaning_data`: cleaned/modeling view used by the ingestion workflow to retrieve the 16 base columns.

The database layer provides controlled storage and a consistent extraction boundary. Feature engineering and model-specific preprocessing are performed after the train, validation, and test checkpoints are created.

## 3. Environment Configuration

Database credentials and connection settings must be supplied through local environment configuration. Use the repository-root `.env.example` template as the source for required variable names and keep the populated `.env` at the repository root.

Rules:

* Never commit a populated `.env` file.
* Never place passwords, access tokens, or complete credential-bearing connection strings in Markdown, notebooks, SQL scripts, or logs.
* Use separate credentials when the hosting platform supports role separation.
* Rotate credentials immediately if they are exposed.
* Confirm that SSL/TLS is enabled for remote Neon connections.

## 4. Data Upload Role

The upload stage reads the raw customer dataset and writes it to `db_predictive_churn`. Its responsibilities are limited to establishing the staging dataset required by the database workflow and reporting whether the upload completed successfully.

Before an upload, confirm:

* the connection targets the intended Neon project and database;
* the staging table name is `db_predictive_churn`;
* the source contains 7,043 customer records;
* credentials are loaded from the local environment rather than embedded in a command or document.

## 5. Data Ingestion Role

The ingestion stage reads from `vw_cleaning_data`, selects the 16 base columns, and creates stratified checkpoint files:

| Checkpoint | Rows | Columns |
| ---------- | ---- | ------- |
| Train | 4930 | 16 |
| Validation | 1056 | 16 |
| Test | 1057 | 16 |

The test checkpoint is locked. Database extraction must not be used to bypass the established split or to refit preprocessing on validation or test data.

## 6. SQL Script Organization

Project SQL assets belong under `Source/sql/`. Keep scripts focused on database responsibilities such as staging objects, views, data-quality queries, and analysis queries. Python-side feature engineering and model preprocessing should not be duplicated as competing SQL transformations.

When database objects change, update this document and `Source/docs/dataflow.md` so that the documented object names and data movement remain consistent.

## 7. Safe Operational Checks

Use read-only checks whenever possible to verify:

* access to the target PostgreSQL database;
* existence of `db_predictive_churn` and `vw_cleaning_data`;
* expected row and column contracts;
* absence of credentials in committed files;
* successful ingestion before model workflows are run.

Database setup details that depend on a specific Neon account should remain outside the repository.
