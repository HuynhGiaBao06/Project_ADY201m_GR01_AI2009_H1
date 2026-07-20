# Machine-Learning Pipeline

## 1. Completed Pipeline Overview

```text
Train / validation / locked test checkpoints
                    │
                    ▼
       Shared target handling and
           feature engineering
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
Logistic Regression       Tree-based branch
branch                    RF / XGB / LGBM / CAT
        │                       │
Numeric transformation          Tree-appropriate
or capping                      categorical encoding
        │                       │
One-hot encoding                No Logistic-specific
and scaling                     scaling/transformation
        │                       │
        └───────────┬───────────┘
                    ▼
       Validation evaluation and
       interpretation workflows
                    │
                    ▼
   Frozen decisions → final test evaluation
                    │
                    ▼
        Reports, figures, and exports
```

## 2. Shared Preprocessing

All model workflows share:

* target handling;
* deterministic creation of `tenure_group`, `service_diversity`, `monthly_charges_ratio`, and `is_paperless_electronic` after splitting;
* the same train, validation, and locked test checkpoint contract;
* train-only fitting for every learned transformation.

## 3. Logistic Regression Branch

The Logistic Regression branch applies preprocessing appropriate for a linear model:

1. numeric transformation or capping;
2. one-hot categorical encoding;
3. feature scaling;
4. Logistic Regression fitting and probability generation.

Signed standardized coefficients are used to describe the direction of association with churn log-odds relative to encoded reference conditions.

## 4. Tree-Based Branch

Random Forest, XGBoost, LightGBM, and CatBoost use the tree-based branch. It applies categorical encoding suitable for tree models and does not apply Logistic-specific scaling or numeric transformation.

Each model is trained and evaluated independently. Model-specific feature-importance values retain their own scales and should not be compared as if their raw magnitudes were equivalent.

## 5. Model Scope

### Core Research Models

* Logistic Regression
* Random Forest
* XGBoost

These models answer the core comparison research question.

### Supplementary Benchmarks

* LightGBM
* CatBoost

The supplementary models extend the benchmark without changing the core research comparison.

## 6. Evaluation Workflow

### Default-Threshold Comparison

Logistic Regression, Random Forest, and XGBoost are compared on validation data at `threshold = 0.50`.

### Threshold Sensitivity

The final threshold-sensitivity presentation focuses on XGBoost, LightGBM, and CatBoost with a Recall target of at least `0.85`. Candidate thresholds are assessed using validation data only.

### Final Test Evaluation

The test set is evaluated after preprocessing, model, and threshold decisions are frozen. Test performance is not fed back into threshold selection or model tuning.

## 7. Interpretation

The implemented interpretation workflow includes:

* signed Logistic Regression coefficients;
* Random Forest feature importance;
* XGBoost feature importance;
* XGBoost SHAP analysis;
* cross-model comparison of leading predictive factors.

XGBoost SHAP explains contributions for `Churn = 1` on the raw margin/log-odds scale. Feature importance and SHAP describe predictive associations, not causal effects.

## 8. Report and Export Workflow

The completed notebooks export model-comparison summaries, threshold results, interpretation tables, and figures under `Source/reports/`. `07_Report_Export_Summary.ipynb` produces report-ready summaries, while `10_section_4_4_visualizations.ipynb` produces the final interpretation visualizations.
