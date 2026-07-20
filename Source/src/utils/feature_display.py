"""Report-only feature display helpers for churn notebooks.

This module maps internal feature codes to report-friendly labels. It must not
be used to rename model input columns before fitting or prediction.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


ID_COLUMN = "ID"
TARGET_COLUMN = "Churn"

BASE_FEATURES = [
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "Tenure",
    "Contract",
    "PaymentMethod",
    "PaperlessBilling",
    "MonthlyCharges",
    "TotalCharges",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
]

ENGINEERED_FEATURES = [
    "tenure_group",
    "service_diversity",
    "monthly_charges_ratio",
    "is_paperless_electronic",
]

MODEL_FEATURES = BASE_FEATURES + ENGINEERED_FEATURES

BINARY_FEATURES = [
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "PaperlessBilling",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "is_paperless_electronic",
]

FEATURE_DISPLAY_NAME_MAP = {
    "ID": "Customer ID",
    "Churn": "Churn",
    "SeniorCitizen": "Senior Citizen",
    "Partner": "Partner",
    "Dependents": "Dependents",
    "Tenure": "Tenure (Months)",
    "Contract": "Contract Type",
    "PaymentMethod": "Payment Method",
    "PaperlessBilling": "Paperless Billing",
    "MonthlyCharges": "Monthly Charges",
    "TotalCharges": "Total Charges",
    "InternetService": "Internet Service",
    "OnlineSecurity": "Online Security",
    "OnlineBackup": "Online Backup",
    "DeviceProtection": "Device Protection",
    "TechSupport": "Tech Support",
    "tenure_group": "Tenure Group",
    "service_diversity": "Service Diversity Score",
    "monthly_charges_ratio": "Monthly Charges Ratio",
    "is_paperless_electronic": "Paperless & Electronic Payment Combo",
}

FEATURE_GROUP_MAP = {
    "ID": "Identifier",
    "Churn": "Target",
    "SeniorCitizen": "Customer Profile",
    "Partner": "Customer Profile",
    "Dependents": "Customer Profile",
    "Tenure": "Account / Contract",
    "Contract": "Account / Contract",
    "PaymentMethod": "Billing",
    "PaperlessBilling": "Billing",
    "MonthlyCharges": "Charges",
    "TotalCharges": "Charges",
    "InternetService": "Service",
    "OnlineSecurity": "Service",
    "OnlineBackup": "Service",
    "DeviceProtection": "Service",
    "TechSupport": "Service",
    "tenure_group": "Engineered",
    "service_diversity": "Engineered",
    "monthly_charges_ratio": "Engineered",
    "is_paperless_electronic": "Engineered",
}

FEATURE_TYPE_MAP = {
    "ID": "Identifier",
    "Churn": "Target",
    "SeniorCitizen": "Binary",
    "Partner": "Binary",
    "Dependents": "Binary",
    "PaperlessBilling": "Binary",
    "OnlineSecurity": "Binary",
    "OnlineBackup": "Binary",
    "DeviceProtection": "Binary",
    "TechSupport": "Binary",
    "is_paperless_electronic": "Binary Engineered",
    "Tenure": "Numeric",
    "MonthlyCharges": "Numeric",
    "TotalCharges": "Numeric",
    "service_diversity": "Numeric Engineered",
    "monthly_charges_ratio": "Numeric Engineered",
    "Contract": "Categorical",
    "PaymentMethod": "Categorical",
    "InternetService": "Categorical",
    "tenure_group": "Categorical Engineered",
}

_BINARY_VALUE_DISPLAY_MAP = {
    0: "No",
    1: "Yes",
    0.0: "No",
    1.0: "Yes",
    "0": "No",
    "1": "Yes",
    "No": "No",
    "Yes": "Yes",
    "False": "No",
    "True": "Yes",
    "false": "No",
    "true": "Yes",
}

CATEGORY_VALUE_DISPLAY_MAP = {
    "Churn": {
        0: "Non-churn",
        1: "Churn",
        0.0: "Non-churn",
        1.0: "Churn",
        "0": "Non-churn",
        "1": "Churn",
        "No": "Non-churn",
        "Yes": "Churn",
        "Non-Churn": "Non-churn",
        "Non-churn": "Non-churn",
        "Churn": "Churn",
    },
    "Contract": {
        1: "Month-to-month",
        12: "One year",
        24: "Two year",
        1.0: "Month-to-month",
        12.0: "One year",
        24.0: "Two year",
        "1": "Month-to-month",
        "12": "One year",
        "24": "Two year",
        "Month-to-month": "Month-to-month",
        "One year": "One year",
        "Two year": "Two year",
    },
    "InternetService": {
        "DSL": "DSL",
        "Fiber optic": "Fiber optic",
        "No": "No Internet Service",
    },
    "PaymentMethod": {
        "Electronic check": "Electronic check",
        "Mailed check": "Mailed check",
        "Bank transfer (automatic)": "Bank transfer automatic",
        "Credit card (automatic)": "Credit card automatic",
    },
}

for _binary_feature in BINARY_FEATURES:
    CATEGORY_VALUE_DISPLAY_MAP.setdefault(_binary_feature, _BINARY_VALUE_DISPLAY_MAP)

_PIPELINE_PREFIXES = (
    "cat__",
    "num__",
    "remainder__",
    "encoder__",
    "iqr_capper__",
    "log_transform__",
    "scaler__",
)

_KNOWN_PARSE_BASE_FEATURES = sorted(
    [ID_COLUMN, TARGET_COLUMN, *MODEL_FEATURES],
    key=len,
    reverse=True,
)


def clean_pipeline_prefix(feature_name: str) -> str:
    """Remove known sklearn/pipeline prefixes from a feature code."""

    cleaned = str(feature_name)
    prefix_removed = True
    while prefix_removed:
        prefix_removed = False
        for prefix in _PIPELINE_PREFIXES:
            if cleaned.startswith(prefix):
                cleaned = cleaned[len(prefix) :]
                prefix_removed = True
    return cleaned


def _fallback_display_name(feature_name: str) -> str:
    return str(feature_name).replace("_", " ").strip().title()


def get_feature_display_name(feature_name: str) -> str:
    """Return the report label for a raw or encoded feature code."""

    parsed = parse_encoded_feature_name(feature_name)
    if parsed["Is_Encoded"]:
        return get_encoded_feature_display_name(feature_name)

    feature_code = parsed["Base_Feature"]
    return FEATURE_DISPLAY_NAME_MAP.get(feature_code, _fallback_display_name(feature_code))


def get_category_display_name(feature_name: str, value: Any) -> str:
    """Return a report label for a category value without changing model data."""

    feature_code = clean_pipeline_prefix(feature_name)
    value_map = CATEGORY_VALUE_DISPLAY_MAP.get(feature_code, {})
    try:
        if pd.isna(value):
            return "Missing"
    except (TypeError, ValueError):
        pass

    if value in value_map:
        return value_map[value]

    value_as_text = str(value)
    if value_as_text in value_map:
        return value_map[value_as_text]

    return value_as_text


def parse_encoded_feature_name(feature_name: str) -> dict[str, Any]:
    """Parse a raw or one-hot encoded feature code into display metadata."""

    feature_code = clean_pipeline_prefix(feature_name)

    if feature_code in FEATURE_DISPLAY_NAME_MAP:
        base_feature = feature_code
        encoded_category = None
        is_encoded = False
    else:
        base_feature = feature_code
        encoded_category = None
        is_encoded = False
        for candidate in _KNOWN_PARSE_BASE_FEATURES:
            prefix = f"{candidate}_"
            if feature_code.startswith(prefix):
                base_feature = candidate
                encoded_category = feature_code[len(prefix) :]
                is_encoded = True
                break

    base_feature_display = FEATURE_DISPLAY_NAME_MAP.get(
        base_feature,
        _fallback_display_name(base_feature),
    )
    encoded_category_display = (
        get_category_display_name(base_feature, encoded_category)
        if encoded_category is not None
        else None
    )

    return {
        "Feature_Code": feature_code,
        "Base_Feature": base_feature,
        "Base_Feature_Display_Name": base_feature_display,
        "Encoded_Category": encoded_category,
        "Encoded_Category_Display_Name": encoded_category_display,
        "Feature_Group": FEATURE_GROUP_MAP.get(base_feature, "Other"),
        "Feature_Type": FEATURE_TYPE_MAP.get(base_feature, "Unknown"),
        "Is_Encoded": is_encoded,
    }


def get_encoded_feature_display_name(feature_name: str) -> str:
    """Return a display label for encoded features such as Contract_12."""

    parsed = parse_encoded_feature_name(feature_name)
    if not parsed["Is_Encoded"]:
        return parsed["Base_Feature_Display_Name"]

    return (
        f"{parsed['Base_Feature_Display_Name']} = "
        f"{parsed['Encoded_Category_Display_Name']}"
    )


def build_feature_mapping_table(feature_names) -> pd.DataFrame:
    """Build report metadata for raw or encoded model feature codes."""

    rows = []
    for feature_name in feature_names:
        parsed = parse_encoded_feature_name(feature_name)
        rows.append(
            {
                "Feature_Code": parsed["Feature_Code"],
                "Feature_Display_Name": get_feature_display_name(feature_name),
                "Base_Feature": parsed["Base_Feature"],
                "Base_Feature_Display_Name": parsed["Base_Feature_Display_Name"],
                "Encoded_Category": parsed["Encoded_Category"],
                "Encoded_Category_Display_Name": parsed[
                    "Encoded_Category_Display_Name"
                ],
                "Feature_Group": parsed["Feature_Group"],
                "Feature_Type": parsed["Feature_Type"],
                "Is_Encoded": parsed["Is_Encoded"],
            }
        )

    return pd.DataFrame(rows)


def build_feature_reference_table() -> pd.DataFrame:
    """Build the canonical base/engineered feature reference table."""

    rows = []
    for feature_code in MODEL_FEATURES:
        rows.append(
            {
                "Feature_Code": feature_code,
                "Feature_Display_Name": get_feature_display_name(feature_code),
                "Feature_Group": FEATURE_GROUP_MAP.get(feature_code, "Other"),
                "Feature_Type": FEATURE_TYPE_MAP.get(feature_code, "Unknown"),
                "Used_In_EDA": True,
                "Used_In_Logistic": True,
                "Used_In_Tree_Models": True,
                "Notes": "Canonical project feature",
            }
        )

    return pd.DataFrame(rows)
