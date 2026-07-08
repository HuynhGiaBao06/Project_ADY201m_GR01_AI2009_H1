"""Target encoding transformer for the refactored churn pipeline."""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


logger = logging.getLogger(__name__)


class TargetEncoder(BaseEstimator, TransformerMixin):
    """Encode the churn target with a fixed business-rule mapping.

    The transformer preserves all input columns and replaces the configured
    target column with binary numeric values. It does not separate ``X``/``y``
    and does not infer mappings from train, validation, or test data.
    """

    ACTIVE_VALUES = ("1", "yes", "y")
    INACTIVE_VALUES = ("0", "no", "n")

    def __init__(self, target_column: str = "Churn"):
        self.target_column = target_column

    def fit(self, X: pd.DataFrame, y=None) -> "TargetEncoder":
        """Validate target values and store fixed mapping metadata."""

        logger.info("TargetEncoder fit started.")
        logger.info("TargetEncoder fit input shape: %s", getattr(X, "shape", None))
        self._validate_input_dataframe(X)
        self.target_column_ = self.target_column
        self._validate_target_column(X)

        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.target_mapping_ = {
            "active_to_1": [1, "1", "Yes", "yes", "Y", "y", True],
            "inactive_to_0": [0, "0", "No", "no", "N", "n", False],
        }

        logger.info("Target column: %s", self.target_column_)
        logger.info(
            "Target value counts before encoding: %s",
            X[self.target_column_].value_counts(dropna=False).to_dict(),
        )
        encoded_target = self._encode_target_series(X[self.target_column_])
        self._validate_encoded_target(encoded_target)
        logger.info(
            "Target value counts after encoding: %s",
            encoded_target.value_counts(dropna=False).to_dict(),
        )
        logger.info("TargetEncoder fit completed.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply the fixed target mapping to a copy of the input DataFrame."""

        logger.info("TargetEncoder transform started.")
        logger.info("TargetEncoder transform input shape: %s", getattr(X, "shape", None))
        self._check_is_fitted()
        self._validate_input_dataframe(X)
        self._validate_target_column(X)

        logger.info(
            "Target value counts before encoding: %s",
            X[self.target_column_].value_counts(dropna=False).to_dict(),
        )
        output = X.copy()
        output[self.target_column_] = self._encode_target_series(output[self.target_column_])
        self._validate_encoded_target(output[self.target_column_])
        self._validate_output(X, output)

        logger.info(
            "Target value counts after encoding: %s",
            output[self.target_column_].value_counts(dropna=False).to_dict(),
        )
        logger.info("TargetEncoder transform output shape: %s", output.shape)
        logger.info("TargetEncoder transform completed.")
        return output

    def _validate_input_dataframe(self, X: pd.DataFrame) -> None:
        if not isinstance(X, pd.DataFrame):
            message = "TargetEncoder expects a pandas DataFrame input."
            logger.error(message)
            raise TypeError(message)

    def _validate_target_column(self, X: pd.DataFrame) -> None:
        if self.target_column_ not in X.columns:
            message = f"Target column '{self.target_column_}' was not found."
            logger.error(message)
            raise ValueError(message)
        logger.info("Target column checked: %s", self.target_column_)

    def _check_is_fitted(self) -> None:
        missing_attributes = [
            attribute
            for attribute in ("target_column_", "feature_names_in_", "target_mapping_")
            if not hasattr(self, attribute)
        ]
        if missing_attributes:
            message = (
                "TargetEncoder must be fitted before transform(). "
                f"Missing fitted attributes: {missing_attributes}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def _encode_target_series(self, target: pd.Series) -> pd.Series:
        missing_mask = target.isna()
        if missing_mask.any():
            message = (
                f"Target column '{self.target_column_}' contains missing values at "
                f"indices: {target.index[missing_mask].tolist()}"
            )
            logger.error(message)
            raise ValueError(message)

        encoded = target.map(self._encode_target_value)
        unknown_mask = encoded.isna()
        if unknown_mask.any():
            unknown_values = sorted(target[unknown_mask].astype(str).unique().tolist())
            message = (
                f"Target column '{self.target_column_}' contains unknown values: "
                f"{unknown_values}"
            )
            logger.error(message)
            raise ValueError(message)

        return encoded.astype(int)

    def _encode_target_value(self, value):
        if isinstance(value, (bool, np.bool_)):
            return int(value)

        if isinstance(value, (int, float, np.integer, np.floating)) and not pd.isna(value):
            if value == 1:
                return 1
            if value == 0:
                return 0
            return np.nan

        if isinstance(value, str):
            normalized_value = value.strip().lower()
            if normalized_value in self.ACTIVE_VALUES:
                return 1
            if normalized_value in self.INACTIVE_VALUES:
                return 0

        return np.nan

    def _validate_encoded_target(self, target: pd.Series) -> None:
        invalid_values = sorted(
            value for value in target.dropna().unique().tolist() if value not in (0, 1)
        )
        if target.isna().any() or invalid_values:
            message = (
                f"Encoded target column '{self.target_column_}' must contain only "
                f"0 and 1. Invalid values: {invalid_values}"
            )
            logger.error(message)
            raise RuntimeError(message)
        logger.info("Encoded target validated for column: %s", self.target_column_)

    def _validate_output(self, input_df: pd.DataFrame, output_df: pd.DataFrame) -> None:
        missing_original_columns = [
            column for column in input_df.columns if column not in output_df.columns
        ]
        if missing_original_columns:
            message = (
                "TargetEncoder output validation failed. Missing original columns: "
                f"{missing_original_columns}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def get_feature_names_out(self, input_features=None):
        """Return unchanged feature names because target encoding replaces values in place."""

        if input_features is None:
            self._check_is_fitted()
            input_features = self.feature_names_in_
        return np.asarray(list(input_features), dtype=object)
