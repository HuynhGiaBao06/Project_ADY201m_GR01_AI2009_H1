"""Logistic-branch numeric transformations for the churn pipeline."""

from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


logger = logging.getLogger(__name__)


class LogisticNumericTransformer(BaseEstimator, TransformerMixin):
    """Apply train-fitted IQR capping and log transforms for Logistic Regression.

    This transformer is intended only for the Logistic Regression preprocessing
    branch. It preserves all input columns, clips configured numeric columns
    using bounds learned in ``fit()``, and applies ``np.log1p`` to configured
    log-transform columns in ``transform()``.
    """

    def __init__(
        self,
        cap_columns: Iterable[str] | None = None,
        log_transform_columns: Iterable[str] | None = None,
        iqr_factor: float = 1.5,
    ):
        self.cap_columns = cap_columns
        self.log_transform_columns = log_transform_columns
        self.iqr_factor = iqr_factor

    def fit(self, X: pd.DataFrame, y=None) -> "LogisticNumericTransformer":
        """Learn IQR capping bounds from the training DataFrame only."""

        logger.info("LogisticNumericTransformer fit started.")
        logger.info("LogisticNumericTransformer fit input shape: %s", getattr(X, "shape", None))
        self.cap_columns_ = self._resolve_columns(self.cap_columns, ("Tenure", "MonthlyCharges"))
        self.log_transform_columns_ = self._resolve_columns(
            self.log_transform_columns, ("TotalCharges",)
        )

        self._validate_input_dataframe(X)
        self._validate_required_columns(X, self.cap_columns_, "capping")
        self._validate_required_columns(X, self.log_transform_columns_, "log transform")
        self._validate_numeric_columns(X, self.cap_columns_ + self.log_transform_columns_)
        self._validate_log_transform_values(X, self.log_transform_columns_)
        self._validate_iqr_factor()

        self.capping_bounds_ = self._fit_iqr_bounds(X)
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)

        logger.info("Capping columns: %s", self.cap_columns_)
        logger.info("Log transform columns: %s", self.log_transform_columns_)
        logger.info("Learned IQR capping bounds: %s", self.capping_bounds_)
        logger.info("LogisticNumericTransformer fit completed.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Clip and log-transform numeric columns on a copy of the input DataFrame."""

        logger.info("LogisticNumericTransformer transform started.")
        logger.info(
            "LogisticNumericTransformer transform input shape: %s", getattr(X, "shape", None)
        )
        self._check_is_fitted()
        self._validate_input_dataframe(X)
        self._validate_required_columns(X, self.cap_columns_, "capping")
        self._validate_required_columns(X, self.log_transform_columns_, "log transform")
        self._validate_numeric_columns(X, self.cap_columns_ + self.log_transform_columns_)
        self._validate_log_transform_values(X, self.log_transform_columns_)

        output = X.copy()
        output = self._apply_iqr_capping(output)
        output = self._apply_log_transform(output)
        self._validate_output(X, output)

        logger.info("LogisticNumericTransformer transform output shape: %s", output.shape)
        logger.info("LogisticNumericTransformer transform completed.")
        return output

    def _resolve_columns(
        self, configured_columns: Iterable[str] | None, default_columns: tuple[str, ...]
    ) -> list[str]:
        if configured_columns is None:
            return list(default_columns)
        if isinstance(configured_columns, str):
            return [configured_columns]
        return list(configured_columns)

    def _validate_input_dataframe(self, X: pd.DataFrame) -> None:
        if not isinstance(X, pd.DataFrame):
            message = "LogisticNumericTransformer expects a pandas DataFrame input."
            logger.error(message)
            raise TypeError(message)

    def _validate_required_columns(
        self, X: pd.DataFrame, columns: Iterable[str], column_group: str
    ) -> None:
        missing_columns = [column for column in columns if column not in X.columns]
        if missing_columns:
            message = (
                f"Missing required {column_group} columns for "
                f"LogisticNumericTransformer: {missing_columns}"
            )
            logger.error(message)
            raise ValueError(message)
        logger.info("%s columns checked: %s", column_group.capitalize(), list(columns))

    def _validate_numeric_columns(self, X: pd.DataFrame, columns: Iterable[str]) -> None:
        invalid_columns = []
        for column in columns:
            numeric_values = pd.to_numeric(X[column], errors="coerce")
            if numeric_values.isna().any():
                invalid_columns.append(column)

        if invalid_columns:
            message = (
                "LogisticNumericTransformer found non-numeric or missing values in "
                f"required numeric columns: {invalid_columns}"
            )
            logger.error(message)
            raise ValueError(message)

    def _validate_log_transform_values(self, X: pd.DataFrame, columns: Iterable[str]) -> None:
        invalid_columns = {}
        for column in columns:
            numeric_values = pd.to_numeric(X[column], errors="coerce")
            invalid_values = numeric_values[numeric_values < -1]
            if not invalid_values.empty:
                invalid_columns[column] = invalid_values.tolist()

        if invalid_columns:
            message = (
                "Log transform columns contain values below -1, which are invalid "
                f"for np.log1p: {invalid_columns}"
            )
            logger.error(message)
            raise ValueError(message)

    def _validate_iqr_factor(self) -> None:
        if not isinstance(self.iqr_factor, (int, float, np.integer, np.floating)):
            message = "iqr_factor must be numeric."
            logger.error(message)
            raise TypeError(message)
        if pd.isna(self.iqr_factor) or not np.isfinite(self.iqr_factor) or self.iqr_factor < 0:
            message = "iqr_factor must be finite and greater than or equal to zero."
            logger.error(message)
            raise ValueError(message)

    def _check_is_fitted(self) -> None:
        missing_attributes = [
            attribute
            for attribute in (
                "capping_bounds_",
                "feature_names_in_",
                "cap_columns_",
                "log_transform_columns_",
            )
            if not hasattr(self, attribute)
        ]
        if missing_attributes:
            message = (
                "LogisticNumericTransformer must be fitted before transform(). "
                f"Missing fitted attributes: {missing_attributes}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def _fit_iqr_bounds(self, X: pd.DataFrame) -> dict[str, dict[str, float]]:
        capping_bounds = {}
        for column in self.cap_columns_:
            numeric_values = pd.to_numeric(X[column], errors="coerce")
            q1 = numeric_values.quantile(0.25)
            q3 = numeric_values.quantile(0.75)
            iqr = q3 - q1
            capping_bounds[column] = {
                "lower_bound": float(q1 - self.iqr_factor * iqr),
                "upper_bound": float(q3 + self.iqr_factor * iqr),
                "q1": float(q1),
                "q3": float(q3),
                "iqr": float(iqr),
            }
        return capping_bounds

    def _apply_iqr_capping(self, X: pd.DataFrame) -> pd.DataFrame:
        output = X.copy()
        for column in self.cap_columns_:
            bounds = self.capping_bounds_.get(column)
            if bounds is None:
                message = f"Missing fitted capping bounds for column: {column}"
                logger.error(message)
                raise RuntimeError(message)
            output[column] = pd.to_numeric(output[column], errors="coerce").clip(
                lower=bounds["lower_bound"],
                upper=bounds["upper_bound"],
            )
        return output

    def _apply_log_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        output = X.copy()
        for column in self.log_transform_columns_:
            output[column] = np.log1p(pd.to_numeric(output[column], errors="coerce"))
        return output

    def _validate_output(self, input_df: pd.DataFrame, output_df: pd.DataFrame) -> None:
        missing_original_columns = [
            column for column in input_df.columns if column not in output_df.columns
        ]
        if missing_original_columns:
            message = (
                "LogisticNumericTransformer output validation failed. Missing "
                f"original columns: {missing_original_columns}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def get_feature_names_out(self, input_features=None):
        """Return unchanged feature names because this transformer replaces values in place."""

        if input_features is None:
            self._check_is_fitted()
            input_features = self.feature_names_in_
        return np.asarray(list(input_features), dtype=object)
