# Predictive Customer Churn in Subscription Services

## 1. Project Overview

This project analyzes customer churn in telecommunications subscription services using the IBM Telco Customer Churn dataset. It combines exploratory analysis, PostgreSQL-based data staging, reproducible machine-learning pipelines, model comparison, model interpretation, and a Power BI dashboard to support customer-retention decisions.

## 2. Research Objectives and Questions

The project aims to identify customers at high risk of churn, explain the strongest predictive factors, and support cost-aware retention prioritization.

1. Which factors have the strongest association with customer churn probability?
2. How do Logistic Regression, Random Forest, and XGBoost compare at the default validation threshold?
3. Which customer groups should receive retention attention first when intervention resources are limited?

## 3. Dataset Overview

The project uses 7,043 telecommunications customers. The 16-column base dataset is split into training, validation, and locked test checkpoints using a stratified 70%/15%/15% allocation:

| Split | Shape | Purpose |
| ----- | ----- | ------- |
| Train | 4930 × 16 | Fit feature and preprocessing transformations and train models |
| Validation | 1056 × 16 | Compare models and select operating thresholds |
| Test | 1057 × 16 | Perform final evaluation after decisions are frozen |

Four features are engineered after splitting: `tenure_group`, `service_diversity`, `monthly_charges_ratio`, and `is_paperless_electronic`.

## 4. Project Architecture

The main data flow is:

```text
Raw data
→ PostgreSQL / Neon staging layer
→ db_predictive_churn
→ vw_cleaning_data
→ train / validation / test checkpoints
→ shared feature engineering
→ model-specific preprocessing
→ model evaluation and interpretation
→ reports, figures, and Power BI dashboard
```

See [`Source/docs/dataflow.md`](Source/docs/dataflow.md) and [`Source/docs/pipeline.md`](Source/docs/pipeline.md) for the detailed lifecycle and modeling design.

## 5. Repository Structure

```text
README.md
requirements.txt
Source/
├── data/          # Raw, checkpoint, EDA, and runtime-log data areas
├── docs/          # Canonical database, dataflow, and pipeline documentation
├── models/        # Saved model artifacts
├── notebooks/     # Numbered analysis, modeling, interpretation, and export notebooks
├── reports/       # Tables, summaries, and figures
├── sql/           # PostgreSQL scripts and queries
└── src/           # Reusable ingestion, preprocessing, and utility modules
```

## 6. Models

### Core Models

The core research comparison evaluates:

* Logistic Regression
* Random Forest
* XGBoost

### Supplementary Benchmarks

The project also benchmarks:

* LightGBM
* CatBoost

These supplementary models extend the benchmark; they do not replace the three core research models.

## 7. Evaluation Strategy

The core models are compared on the validation set at `threshold = 0.50`. Threshold sensitivity analysis focuses on XGBoost, LightGBM, and CatBoost with a Recall target of at least `0.85`. Thresholds are selected using validation data. The locked test set is evaluated only after model and threshold decisions are frozen.

## 8. Model Interpretation

The interpretation workflow includes signed Logistic Regression coefficients, Random Forest feature importance, XGBoost feature importance, XGBoost SHAP analysis, and cross-model comparison. SHAP explains the XGBoost churn-class output and is not presented as a causal analysis.

## 9. How to Set Up and Run the Project

Use Python 3.10 or newer and work from the repository root.

1. Create and activate a virtual environment.

   ```bash
   python -m venv venv
   ```

   On Windows:

   ```powershell
   venv\Scripts\activate
   ```

   On macOS or Linux:

   ```bash
   source venv/bin/activate
   ```

2. Install the declared dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Copy the repository-root `.env.example` to a repository-root `.env` and supply the required PostgreSQL/Neon connection values. Never commit credentials.

4. Verify the preprocessing entry point without database ingestion when needed:

   ```powershell
   python -m Source.src.main
   ```

   The default command reuses existing checkpoints. Do not add `--force-ingestion` or
   `--use-database` for a checkpoint-only verification.

5. Start Jupyter and run the active notebooks in dependency order when reproducing the full workflow:

   ```text
   01_EDA_and_Feature_Engineering.ipynb
   02_Logistic_Regression.ipynb
   03_tree_models_train.ipynb
   04_xgboost_models_train.ipynb
   08_lightgbm_models_train.ipynb
   09_catboost_models_train.ipynb
   05_Model_Comparison.ipynb
   06_Model_Interpretation_SHAP.ipynb
   07_Report_Export_Summary.ipynb
   10_section_4_4_visualizations.ipynb
   ```

Database availability and existing checkpoints determine whether ingestion must be rerun. Do not use the locked test set for preprocessing fitting, model selection, or threshold selection.

## 10. Key Outputs

Key outputs are stored under `Source/reports/` and include model-comparison summaries, threshold-sensitivity results, feature-importance outputs, XGBoost SHAP interpretation, report-ready tables, and figures.

## 11. Dashboard

The delivered interactive dashboard is [`[ADY201m] Dashboard.pbix`]([ADY201m]%20Dashboard.pbix). It summarizes churn performance and high-risk customer segments. Notebook 10 consumes the retained, validated report-ready CSV exports under `Source/reports/data_reports/` to produce its final interpretation visualizations.

## 12. Documentation

* [`Source/docs/database_guideline.md`](Source/docs/database_guideline.md): PostgreSQL/Neon architecture, configuration, roles, and credential safety
* [`Source/docs/dataflow.md`](Source/docs/dataflow.md): dataset lifecycle, checkpoint ownership, and leakage controls
* [`Source/docs/pipeline.md`](Source/docs/pipeline.md): preprocessing branches, models, evaluation, interpretation, and exports
* [`Source/reports/data_reports/report_summary_markdown.md`](Source/reports/data_reports/report_summary_markdown.md): validated result summary
