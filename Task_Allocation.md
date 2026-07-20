# Task Allocation and Contribution Record

Project: **Predictive Customer Churn in Subscription Services**  
Recorded project period: **18 May 2026 – 14 June 2026**

This file is a historical contribution record. It is retained for possible academic contribution evidence and is not the canonical source for the final technical architecture.

## Team Members

* **Huỳnh Gia Bảo — Team Leader:** Project setup, PostgreSQL/Neon schema and pipeline coordination, feature engineering, XGBoost, methodology, repository review, and report integration.
* **Nguyễn An Duy — Member:** Data cleaning, data-quality analysis, Logistic Regression, foundational visualizations, report introduction/business context, and Power BI dashboard development.
* **Nguyễn Hữu Kiệt — Member:** SQL analysis, advanced visualizations, Random Forest, model comparison support, strategic insights, conclusion, and presentation design.

## Sprint 1 — Project Setup, Raw Data, and Database Foundation

### Huỳnh Gia Bảo

* Established the repository, dependency manifest, and initial `Source/` structure.
* Prepared the base notebook environment and team setup guidance.
* Coordinated the PostgreSQL/Neon staging design and data-upload workflow.

### Nguyễn An Duy

* Established project-management and communication spaces.
* Cleaned missing values and logical data issues while preserving the downstream model-preprocessing boundary.
* Prepared data-quality checks for the database workflow.

### Nguyễn Hữu Kiệt

* Developed the database-to-Python connection workflow.
* Prepared churn-rate queries by contract, payment method, and subscribed services.

## Sprint 2 — Analysis, Feature Engineering, and Visualization

### Huỳnh Gia Bảo

* Developed `tenure_group`, `service_diversity`, `monthly_charges_ratio`, and `is_paperless_electronic`.
* Coordinated database-view and query integration.
* Reviewed and integrated team contributions.

### Nguyễn An Duy

* Analyzed charges and tenure for churned versus retained customers.
* Produced foundational bar charts and boxplots for `MonthlyCharges` and `TotalCharges`.

### Nguyễn Hữu Kiệt

* Investigated service factors associated with elevated churn rates.
* Produced multivariable correlation and tenure-group visualizations.

## Sprint 3 — Modeling and Dashboard

### Huỳnh Gia Bảo

* Coordinated the train, validation, and locked test checkpoint contract.
* Developed and tuned XGBoost and produced its feature-importance analysis.
* Led validation-based threshold analysis for recall-sensitive operation.

### Nguyễn An Duy

* Developed the Logistic Regression preprocessing and modeling workflow.
* Interpreted signed model coefficients.
* Built the Power BI dashboard for churn overview and high-risk segments.

### Nguyễn Hữu Kiệt

* Developed the Random Forest workflow and feature-importance analysis.
* Supported the core model comparison across Accuracy, Precision, Recall, F1-score, and ROC-AUC.
* Developed retention scenarios and early-warning recommendations.

## Sprint 4 — Reporting and Presentation

### Huỳnh Gia Bảo

* Wrote the methodology and XGBoost analysis.
* Coordinated the academic report structure and final integration.

### Nguyễn An Duy

* Wrote the introduction and business-understanding sections.
* Presented Logistic Regression results and integrated dashboard/report visuals.

### Nguyễn Hữu Kiệt

* Presented Random Forest results.
* Wrote the conclusion and actionable insights.
* Designed the final presentation.

## Project-Level Supplementary Work

The completed project also includes LightGBM and CatBoost supplementary benchmarks, XGBoost SHAP interpretation, threshold-sensitivity outputs for the boosting models, report exports, and final interpretation figures. This historical allocation file does not assign individual ownership for work that was not attributed in the original task record.
