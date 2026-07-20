# Contributing to Predictive Customer Churn in Subscription Services

## 1. Project Scope

Contributions should support the completed customer-churn analysis without changing its research contract unintentionally. The core comparison covers Logistic Regression, Random Forest, and XGBoost; LightGBM and CatBoost are supplementary benchmarks. PostgreSQL hosted on Neon.tech provides the database layer, and Power BI is the delivered dashboard.

Read `README.md` and the canonical documents under `Source/docs/` before changing data flow, preprocessing, evaluation, or interpretation behavior.

## 2. Repository Structure

```text
Source/
├── data/          # Raw data, checkpoints, EDA data, and runtime logs
├── docs/          # Canonical database, dataflow, and pipeline documentation
├── models/        # Saved model artifacts
├── notebooks/     # EDA, training, evaluation, interpretation, and export workflows
├── reports/       # Report-ready summaries, tables, and figures
├── sql/           # PostgreSQL scripts and analytical queries
└── src/           # Reusable ingestion, preprocessing, and utility logic
```

Keep reusable logic in `Source/src/`; use notebooks for analysis, experiments, interpretation, and report export.

## 3. Environment Setup

Use Python 3.10 or newer and work from the repository root.

1. Create and activate a Python virtual environment.

   ```bash
   python -m venv venv
   ```

2. Install declared dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the repository-root `.env.example` to a repository-root `.env` and supply the required PostgreSQL/Neon values. Never commit a populated `.env` file.

See `README.md` for the full setup and dependency-aware notebook sequence (`01`, `02`, `03`, `04`, `08`, `09`, `05`, `06`, `07`, `10`).

## 4. Development Workflow

* Create a focused branch for each change.
* Keep changes small, scoped, and easy to review.
* Avoid unrelated formatting or generated-output changes.
* Review the affected workflow and documentation before requesting review.
* Inspect staged files carefully so secrets and local artifacts are not included.

## 5. Branch and Commit Guidelines

Use a descriptive branch such as `feat12-update-threshold-report` or `fix13-correct-dataflow-docs`. Use clear Conventional Commit messages:

* `feat: add churn segment analysis`
* `fix: correct validation threshold summary`
* `docs: update PostgreSQL guidance`

Do not push development changes directly to `main`, and avoid vague commit messages such as `update`, `fix`, or `done`.

## 6. Documentation Standards

Documentation must:

* be written in English;
* use the formal project title;
* use current `Source/` paths;
* avoid obsolete project terminology;
* avoid personal absolute paths and credentials;
* identify PostgreSQL/Neon and Power BI correctly;
* distinguish core models from supplementary benchmarks;
* keep README concise and place detailed technical guidance under `Source/docs/`.

Update relevant documentation whenever behavior, paths, data contracts, or outputs change.

## 7. Data and Model Safety Rules

* Do not overwrite raw data unnecessarily.
* Preserve the stratified train/validation/test checkpoint contract.
* Fit learned preprocessing on training data only.
* Do not use validation or test data to fit preprocessing statistics.
* Use validation data for model comparison and threshold selection.
* Do not use the locked test set for tuning, model selection, or threshold selection.
* Evaluate the test set only after preprocessing, model, and threshold decisions are frozen.
* Treat feature importance and SHAP outputs as predictive associations, not causal evidence.

## 8. Database and Credential Safety

The current database flow uses PostgreSQL on Neon.tech, with `db_predictive_churn` as the staging table and `vw_cleaning_data` as the cleaned/modeling view.

* Load credentials through environment variables.
* Never expose Neon/PostgreSQL passwords or credential-bearing connection strings.
* Keep the staging and cleaned/modeling layers conceptually separate.
* Avoid destructive SQL operations unless the change has explicit approval and review.
* Prefer read-only verification queries when checking shared database state.

## 9. Notebook and Experiment Guidelines

* Restart and run affected notebooks from beginning to end before review.
* Remove excessive output and temporary diagnostic cells.
* Record the purpose, assumptions, metrics, and conclusions of experiments.
* Keep reusable preprocessing and pipeline behavior in `Source/src/` rather than duplicating it across notebooks.
* Do not silently change checkpoint ownership, threshold-selection data, or the locked-test policy.

## 10. Pull Request and Review Expectations

A pull request should explain:

* the objective and scope;
* affected files and pipeline stages;
* validation or verification performed;
* changes to metrics, outputs, or documentation;
* any data, model, database, or reproducibility risk.

Request independent review, address feedback on the same branch, resolve conflicts, and rerun affected workflows before merging. Do not merge changes that expose credentials, introduce data leakage, or leave documentation inconsistent with the implementation.
