"""Logistic-branch scaling transformer for the churn pipeline."""

from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler


logger = logging.getLogger(__name__)


class LogisticScaler(BaseEstimator, TransformerMixin):
    """Scale selected Logistic Regression numeric columns with ``StandardScaler``.

    The transformer is intended only for the Logistic Regression preprocessing
    branch. It preserves all input columns and replaces configured numeric
    column values with train-fitted standardized values.
    """

    DEFAULT_SCALE_COLUMNS = (
        "Tenure",
        "MonthlyCharges",
        "TotalCharges",
        "SeniorCitizen",
        "Partner",
        "Dependents",
        "PaperlessBilling",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
        "service_diversity",
        "monthly_charges_ratio",
        "is_paperless_electronic",
    )

    def __init__(self, scale_columns: Iterable[str] | None = None):
        self.scale_columns = scale_columns

    def fit(self, X: pd.DataFrame, y=None) -> "LogisticScaler":
        """Fit ``StandardScaler`` parameters from the training DataFrame only."""

        logger.info("LogisticScaler fit started.")
        logger.info("LogisticScaler fit input shape: %s", getattr(X, "shape", None))
        self._validate_input_dataframe(X)
        self.scale_columns_ = self._resolve_scale_columns()
        self._validate_scale_columns(X)
        self._validate_numeric_columns(X)

        self.scaler_ = StandardScaler()
        self.scaler_.fit(self._numeric_frame(X))
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)

        logger.info("Scale columns: %s", self.scale_columns_)
        logger.info(
            "Fitted scaler mean/scale summary: %s",
            {
                column: {
                    "mean": float(mean),
                    "scale": float(scale),
                }
                for column, mean, scale in zip(
                    self.scale_columns_, self.scaler_.mean_, self.scaler_.scale_
                )
            },
        )
        logger.info("LogisticScaler fit completed.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Scale selected columns on a copy of the input DataFrame."""

        logger.info("LogisticScaler transform started.")
        logger.info("LogisticScaler transform input shape: %s", getattr(X, "shape", None))
        self._check_is_fitted()
        self._validate_input_dataframe(X)
        self._validate_scale_columns(X)
        self._validate_numeric_columns(X)

        output = X.copy()
        scaled_values = pd.DataFrame(
            self.scaler_.transform(self._numeric_frame(X)),
            columns=self.scale_columns_,
            index=X.index,
        )
        for column in self.scale_columns_:
            output[column] = scaled_values[column]
        self._validate_output(X, output)

        logger.info("LogisticScaler transform output shape: %s", output.shape)
        logger.info("LogisticScaler transform completed.")
        return output

    def _validate_input_dataframe(self, X: pd.DataFrame) -> None:
        if not isinstance(X, pd.DataFrame):
            message = "LogisticScaler expects a pandas DataFrame input."
            logger.error(message)
            raise TypeError(message)

    def _resolve_scale_columns(self) -> list[str]:
        if self.scale_columns is None:
            return list(self.DEFAULT_SCALE_COLUMNS)
        if isinstance(self.scale_columns, str):
            return [self.scale_columns]
        return list(self.scale_columns)

    def _validate_scale_columns(self, X: pd.DataFrame) -> None:
        missing_columns = [column for column in self.scale_columns_ if column not in X.columns]
        if missing_columns:
            message = f"Missing required scale columns for LogisticScaler: {missing_columns}"
            logger.error(message)
            raise ValueError(message)
        logger.info("Scale columns checked: %s", self.scale_columns_)

    def _validate_numeric_columns(self, X: pd.DataFrame) -> None:
        invalid_columns = []
        for column in self.scale_columns_:
            numeric_values = pd.to_numeric(X[column], errors="coerce")
            if numeric_values.isna().any():
                invalid_columns.append(column)

        if invalid_columns:
            message = (
                "LogisticScaler found non-numeric or missing values in scale "
                f"columns: {invalid_columns}"
            )
            logger.error(message)
            raise ValueError(message)

    def _check_is_fitted(self) -> None:
        missing_attributes = [
            attribute
            for attribute in ("scaler_", "scale_columns_", "feature_names_in_")
            if not hasattr(self, attribute)
        ]
        if missing_attributes:
            message = (
                "LogisticScaler must be fitted before transform(). "
                f"Missing fitted attributes: {missing_attributes}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def _numeric_frame(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.loc[:, self.scale_columns_].apply(pd.to_numeric, errors="coerce")

    def _validate_output(self, input_df: pd.DataFrame, output_df: pd.DataFrame) -> None:
        missing_original_columns = [
            column for column in input_df.columns if column not in output_df.columns
        ]
        if missing_original_columns:
            message = (
                "LogisticScaler output validation failed. Missing original "
                f"columns: {missing_original_columns}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def get_feature_names_out(self, input_features=None):
        """Return unchanged feature names because scaling replaces values in place."""

        if input_features is None:
            self._check_is_fitted()
            input_features = self.feature_names_in_
        return np.asarray(list(input_features), dtype=object)
