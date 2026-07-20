# Dataflow

## 1. End-to-End Lifecycle

```text
Raw data
→ PostgreSQL / Neon
→ db_predictive_churn staging table
→ vw_cleaning_data cleaned/modeling view
→ 16-column base dataset
→ stratified 70% / 15% / 15% split
→ train / validation / test checkpoints
→ feature engineering after the split
→ model-specific preprocessing
→ modeling and interpretation notebooks
→ reports, figures, and dashboard outputs
```

## 2. Database Boundary

The raw 7,043-customer dataset is uploaded to the PostgreSQL staging table `db_predictive_churn`. The view `vw_cleaning_data` exposes the cleaned base data used by the ingestion workflow.

The database is the controlled storage and extraction layer. It does not replace the checkpoint lifecycle or the Python modeling pipelines.

## 3. Base Data Contract

The ingestion workflow retrieves 16 base columns and produces the following checkpoints:

| Split | Allocation | Shape | Responsibility |
| ----- | ---------- | ----- | -------------- |
| Train | 70% | 4930 × 16 | Fit learned transformations and models |
| Validation | 15% | 1056 × 16 | Compare models and select thresholds |
| Test | 15% | 1057 × 16 | Final evaluation after decisions are frozen |

The split is stratified. Checkpoints are the stable handoff between ingestion and downstream modeling.

## 4. Feature Engineering After Splitting

The following four features are created after the split:

* `tenure_group`
* `service_diversity`
* `monthly_charges_ratio`
* `is_paperless_electronic`

Applying the same deterministic feature definitions to all splits preserves a consistent schema. Any learned statistic used by a transformation must be fitted on training data only.

## 5. Model-Specific Preprocessing

Shared logic handles the target and engineered features. The downstream preprocessing then branches:

* Logistic Regression uses model-appropriate numeric transformation or capping, one-hot categorical encoding, and scaling.
* Tree-based models use categorical encoding appropriate for trees and do not use Logistic-specific scaling or numeric transformation.

Model-ready transformations are performed inside the modeling pipeline rather than materialized as a competing set of manually preprocessed datasets.

## 6. Leakage Controls

The project follows these ownership rules:

1. Training data fits learned preprocessing and model parameters.
2. Validation data supports model comparison and threshold selection.
3. Test data remains locked until preprocessing, model, and threshold decisions are frozen.
4. Validation and test data never contribute fitted statistics to preprocessing.
5. Test results are final evaluation results, not tuning feedback.

## 7. Notebook Responsibilities

| Notebook | Responsibility |
| -------- | -------------- |
| `01_EDA_and_Feature_Engineering.ipynb` | EDA and feature-engineering analysis |
| `02_Logistic_Regression.ipynb` | Logistic Regression training and evaluation |
| `03_tree_models_train.ipynb` | Random Forest workflow |
| `04_xgboost_models_train.ipynb` | XGBoost workflow |
| `05_Model_Comparison.ipynb` | Core model comparison |
| `06_Model_Interpretation_SHAP.ipynb` | Model interpretation and XGBoost SHAP |
| `07_Report_Export_Summary.ipynb` | Report and summary export |
| `08_lightgbm_models_train.ipynb` | LightGBM benchmark |
| `09_catboost_models_train.ipynb` | CatBoost benchmark |
| `10_section_4_4_visualizations.ipynb` | Final interpretation visualizations |

For a clean end-to-end rerun, use dependency order: `01` → `02` → `03` → `04` → `08` → `09` → `05` → `06` → `07` → `10`. Notebook 10 consumes the retained, validated Power BI/report-ready CSV exports under `Source/reports/data_reports/`.

## 8. Output Locations

* Checkpoint and runtime data areas: `Source/data/`
* Saved model artifacts: `Source/models/`
* Modeling notebooks: `Source/notebooks/`
* Report tables, summaries, and figures: `Source/reports/`
* PostgreSQL scripts and queries: `Source/sql/`

Runtime logs record execution history but are not a source of current path instructions.
