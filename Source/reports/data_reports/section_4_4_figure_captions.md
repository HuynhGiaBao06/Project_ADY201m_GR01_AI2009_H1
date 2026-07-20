## Figure 4.4-A

Cross-model convergence of the leading churn predictors across Logistic
Regression coefficients, Random Forest impurity importance, XGBoost gain,
LightGBM gain, CatBoost FeatureImportance, and XGBoost mean absolute SHAP.
Lower ranks indicate greater within-method importance. Raw importance
magnitudes are not directly comparable across methods.

## Figure 4.4-B

Top five positive and negative standardized Logistic Regression
coefficients. Positive coefficients are associated with higher churn
log-odds, whereas negative coefficients are associated with lower churn
log-odds, relative to the encoded reference conditions.

## Figure 4.4-C

Global XGBoost feature importance measured by mean absolute SHAP values
for 500 validation observations. Values represent average absolute
contributions to the raw model margin for the churn class and describe
contribution magnitude rather than direction or causality.
