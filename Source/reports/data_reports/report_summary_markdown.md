# Report Summary

## Core Research Comparison (RQ2)
RQ2 compares Logistic Regression, Random Forest and XGBoost on validation at threshold 0.50. Highest Recall in this scope: Logistic Regression (0.8036).

## Five-Model Default Benchmark
The additional benchmark compares all five models on validation at threshold 0.50. Highest F1 in this scope: LightGBM (0.6454).

## Boosting Threshold Sensitivity Analysis
XGBoost, LightGBM and CatBoost only were assessed across validation thresholds. Recall target status and selected thresholds were determined only from validation.

## Final Boosting Test Results
Test evaluation used thresholds frozen from validation. Highest test Recall among the three boosting models: CatBoost (0.8754). This is metric-specific, not a universal best-model claim.

## Model Interpretation
Logistic coefficients, Random Forest impurity importance, XGBoost gain, LightGBM gain and CatBoost FeatureImportance are reported separately. Detailed SHAP is XGBoost-only and explains Churn = 1 on the raw margin/log-odds scale.

## Recommendations
Observed drivers are predictive associations, not causal effects. Operating-model choice should follow the required metric and intervention costs.