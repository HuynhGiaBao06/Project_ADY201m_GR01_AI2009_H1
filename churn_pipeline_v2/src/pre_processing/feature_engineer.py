"""Feature engineering transformer for the refactored churn pipeline."""

from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


logger = logging.getLogger(__name__)


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """Create churn features after the train/validation/test split.

    The transformer preserves all input columns and appends engineered columns.
    Only ``monthly_charges_mean_`` is learned, and it is learned in ``fit()``
    from the training DataFrame only.
    """

    REQUIRED_COLUMNS = (
        "Tenure",
        "MonthlyCharges",
        "PaymentMethod",
        "PaperlessBilling",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
    )

    SERVICE_COLUMNS = (
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
    )

    ENGINEERED_FEATURE_NAMES = (
        "tenure_group",
        "service_diversity",
        "monthly_charges_ratio",
        "is_paperless_electronic",
    )

    TENURE_BINS = [0, 12, 24, 36, 48, 60, 72, np.inf]
    TENURE_LABELS = [
        "0-12 months",
        "13-24 months",
        "25-36 months",
        "37-48 months",
        "49-60 months",
        "61-72 months",
        "72+ months",
    ]

    ACTIVE_VALUES = {1, "1", "yes", True}
    INACTIVE_VALUES = {
        0,
        "0",
        "no",
        "no internet service",
        "no phone service",
        False,
    }

    COMMON_PAYMENT_METHODS = {
        "bank transfer (automatic)",
        "credit card (automatic)",
        "electronic check",
        "mailed check",
    }

    def fit(self, X: pd.DataFrame, y=None) -> "FeatureEngineer":
        """Learn train-only statistics needed for feature creation."""

        logger.info("FeatureEngineer fit started.")
        logger.info("FeatureEngineer fit input shape: %s", getattr(X, "shape", None))
        self._validate_input_dataframe(X)
        self._validate_required_columns(X)
        self._validate_no_existing_engineered_columns(X)
        self._validate_numeric_columns(X, columns=("Tenure", "MonthlyCharges"))

        monthly_charges = pd.to_numeric(X["MonthlyCharges"], errors="coerce")
        if monthly_charges.isna().any():
            message = "MonthlyCharges contains values that cannot be converted to numeric."
            logger.error(message)
            raise ValueError(message)

        self.monthly_charges_mean_ = monthly_charges.mean()
        self._validate_monthly_charges_mean()
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.engineered_feature_names_ = list(self.ENGINEERED_FEATURE_NAMES)

        logger.info("Learned monthly_charges_mean_: %s", self.monthly_charges_mean_)
        logger.info("FeatureEngineer fit completed.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Append engineered churn features to a copy of the input DataFrame."""

        logger.info("FeatureEngineer transform started.")
        logger.info("FeatureEngineer transform input shape: %s", getattr(X, "shape", None))
        self._check_is_fitted()
        self._validate_input_dataframe(X)
        self._validate_required_columns(X)
        self._validate_no_existing_engineered_columns(X)
        self._validate_numeric_columns(X, columns=("Tenure", "MonthlyCharges"))
        self._log_uncommon_payment_methods(X["PaymentMethod"])

        output = X.copy()
        output["tenure_group"] = self._create_tenure_group(output["Tenure"])
        output["service_diversity"] = self._create_service_diversity(output)
        output["monthly_charges_ratio"] = self._create_monthly_charges_ratio(
            output["MonthlyCharges"]
        )
        output["is_paperless_electronic"] = self._create_is_paperless_electronic(output)

        self._validate_output_columns(X, output)
        logger.info("Engineered columns added: %s", self.engineered_feature_names_)
        logger.info("FeatureEngineer transform output shape: %s", output.shape)
        logger.info("FeatureEngineer transform completed.")
        return output

    def _validate_input_dataframe(self, X: pd.DataFrame) -> None:
        if not isinstance(X, pd.DataFrame):
            message = "FeatureEngineer expects a pandas DataFrame input."
            logger.error(message)
            raise TypeError(message)

    def _validate_required_columns(self, X: pd.DataFrame) -> None:
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in X.columns]
        if missing_columns:
            message = f"FeatureEngineer missing required columns: {missing_columns}"
            logger.error(message)
            raise ValueError(message)
        logger.info("Required columns checked: %s", list(self.REQUIRED_COLUMNS))

    def _validate_no_existing_engineered_columns(self, X: pd.DataFrame) -> None:
        existing_columns = [col for col in self.ENGINEERED_FEATURE_NAMES if col in X.columns]
        if existing_columns:
            message = (
                "FeatureEngineer input already contains engineered columns: "
                f"{existing_columns}"
            )
            logger.error(message)
            raise ValueError(message)

    def _validate_numeric_columns(self, X: pd.DataFrame, columns: Iterable[str]) -> None:
        invalid_columns = []
        for column in columns:
            numeric_values = pd.to_numeric(X[column], errors="coerce")
            if numeric_values.isna().any():
                invalid_columns.append(column)

        if invalid_columns:
            message = (
                "FeatureEngineer found non-numeric or missing values in required "
                f"numeric columns: {invalid_columns}"
            )
            logger.error(message)
            raise ValueError(message)

    def _check_is_fitted(self) -> None:
        if not hasattr(self, "monthly_charges_mean_"):
            message = "FeatureEngineer must be fitted before transform()."
            logger.error(message)
            raise RuntimeError(message)
        self._validate_monthly_charges_mean()

    def _validate_monthly_charges_mean(self) -> None:
        mean_value = getattr(self, "monthly_charges_mean_", None)
        if not isinstance(mean_value, (int, float, np.integer, np.floating)):
            message = "monthly_charges_mean_ must be numeric."
            logger.error(message)
            raise ValueError(message)
        if pd.isna(mean_value) or not np.isfinite(mean_value) or mean_value <= 0:
            message = "monthly_charges_mean_ must be finite and greater than zero."
            logger.error(message)
            raise ValueError(message)

    def _normalize_binary_series(self, series: pd.Series, column_name: str) -> pd.Series:
        normalized = series.map(self._normalize_binary_value)
        unexpected_mask = normalized.isna()
        if unexpected_mask.any():
            unexpected_values = sorted(
                series[unexpected_mask].dropna().astype(str).unique().tolist()
            )
            message = (
                f"Unexpected values in {column_name}: {unexpected_values}. "
                "Expected active/inactive churn binary values."
            )
            logger.error(message)
            raise ValueError(message)
        return normalized.astype(int)

    def _normalize_binary_value(self, value):
        if pd.isna(value):
            return 0
        if isinstance(value, str):
            value = value.strip().lower()
        if value in self.ACTIVE_VALUES:
            return 1
        if value in self.INACTIVE_VALUES:
            return 0
        return np.nan

    def _log_uncommon_payment_methods(self, payment_method: pd.Series) -> None:
        normalized_payment = payment_method.dropna().astype(str).str.strip().str.lower()
        uncommon_values = sorted(
            value
            for value in normalized_payment.unique().tolist()
            if value and value not in self.COMMON_PAYMENT_METHODS
        )
        if uncommon_values:
            logger.warning(
                "Uncommon PaymentMethod values found; continuing with automatic-payment "
                "contains logic: %s",
                uncommon_values,
            )
        logger.info("PaymentMethod values checked.")

    def _create_tenure_group(self, tenure: pd.Series) -> pd.Series:
        tenure_numeric = pd.to_numeric(tenure, errors="coerce")
        return pd.cut(
            tenure_numeric,
            bins=self.TENURE_BINS,
            labels=self.TENURE_LABELS,
            right=True,
            include_lowest=True,
        )

    def _create_service_diversity(self, X: pd.DataFrame) -> pd.Series:
        active_service_flags = [
            self._normalize_binary_series(X[column], column) for column in self.SERVICE_COLUMNS
        ]
        return pd.concat(active_service_flags, axis=1).sum(axis=1)

    def _create_monthly_charges_ratio(self, monthly_charges: pd.Series) -> pd.Series:
        self._validate_monthly_charges_mean()
        monthly_charges_numeric = pd.to_numeric(monthly_charges, errors="coerce")
        return monthly_charges_numeric / self.monthly_charges_mean_

    def _create_is_paperless_electronic(self, X: pd.DataFrame) -> pd.Series:
        paperless_billing = self._normalize_binary_series(
            X["PaperlessBilling"], "PaperlessBilling"
        )
        payment_method = X["PaymentMethod"].fillna("").astype(str)
        # Preserve legacy logic: paperless billing plus automatic payment method.
        automatic_payment = payment_method.str.contains("automatic", case=False, na=False)
        return (paperless_billing.eq(1) & automatic_payment).astype(int)

    def _validate_output_columns(self, input_df: pd.DataFrame, output_df: pd.DataFrame) -> None:
        missing_original_columns = [col for col in input_df.columns if col not in output_df.columns]
        missing_engineered_columns = [
            col for col in self.ENGINEERED_FEATURE_NAMES if col not in output_df.columns
        ]

        if missing_original_columns or missing_engineered_columns:
            message = (
                "FeatureEngineer output validation failed. "
                f"Missing original columns: {missing_original_columns}; "
                f"missing engineered columns: {missing_engineered_columns}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def get_feature_names_out(self, input_features=None):
        """Return original feature names plus engineered feature names."""

        if input_features is None:
            self._check_is_fitted()
            input_features = self.feature_names_in_
        return np.asarray(list(input_features) + list(self.ENGINEERED_FEATURE_NAMES), dtype=object)
