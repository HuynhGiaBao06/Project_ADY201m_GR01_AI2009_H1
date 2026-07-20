"""Categorical encoding transformer for the churn pipeline."""

from __future__ import annotations

import logging
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder


logger = logging.getLogger(__name__)


class CategoricalEncoder(BaseEstimator, TransformerMixin):
    """Encode categorical churn features for logistic or tree branches.

    ``encoding_strategy="onehot"`` preserves the legacy Logistic Regression
    behavior. ``encoding_strategy="ordinal"`` preserves the legacy tree-model
    behavior. The transformer learns categories in ``fit()`` only and returns a
    pandas DataFrame.
    """

    ALLOWED_STRATEGIES = ("onehot", "ordinal")
    DEFAULT_CATEGORICAL_COLUMNS = (
        "Dependents",
        "Contract",
        "PaymentMethod",
        "InternetService",
        "tenure_group",
        "Partner",
        "PaperlessBilling",
        "OnlineSecurity",
        "OnlineBackup",
        "DeviceProtection",
        "TechSupport",
    )
    PROTECTED_COLUMNS = ("ID", "Churn")

    def __init__(
        self,
        encoding_strategy: str = "onehot",
        categorical_columns: Iterable[str] | None = None,
    ):
        self.encoding_strategy = encoding_strategy
        self.categorical_columns = categorical_columns

    def fit(self, X: pd.DataFrame, y=None) -> "CategoricalEncoder":
        """Fit the configured sklearn categorical encoder on training data."""

        logger.info("CategoricalEncoder fit started.")
        logger.info("CategoricalEncoder fit input shape: %s", getattr(X, "shape", None))
        self._validate_input_dataframe(X)
        self.encoding_strategy_ = self._validate_encoding_strategy(self.encoding_strategy)
        self.categorical_columns_ = self._resolve_categorical_columns()
        self._validate_categorical_columns(X)

        self.encoder_ = self._build_encoder()
        self.encoder_.fit(self._categorical_frame(X))
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        self.encoded_feature_names_ = self._get_encoded_feature_names()
        self.output_feature_names_ = self._build_output_feature_names(X)

        logger.info("Encoding strategy: %s", self.encoding_strategy_)
        logger.info("Categorical columns: %s", self.categorical_columns_)
        logger.info("Unknown category handling: %s", self._unknown_category_handling())
        logger.info("Learned categories summary: %s", self._categories_summary())
        logger.info("CategoricalEncoder fit completed.")
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Encode configured categorical columns on a copy of the input DataFrame."""

        logger.info("CategoricalEncoder transform started.")
        logger.info("CategoricalEncoder transform input shape: %s", getattr(X, "shape", None))
        self._check_is_fitted()
        self._validate_input_dataframe(X)
        self._validate_categorical_columns(X)

        if self.encoding_strategy_ == "onehot":
            output = self._transform_onehot(X)
        else:
            output = self._transform_ordinal(X)

        self._validate_output(output)
        logger.info("CategoricalEncoder transform output shape: %s", output.shape)
        logger.info("CategoricalEncoder transform completed.")
        return output

    def _validate_input_dataframe(self, X: pd.DataFrame) -> None:
        if not isinstance(X, pd.DataFrame):
            message = "CategoricalEncoder expects a pandas DataFrame input."
            logger.error(message)
            raise TypeError(message)

    def _validate_encoding_strategy(self, strategy: str) -> str:
        if not isinstance(strategy, str):
            message = "encoding_strategy must be a string."
            logger.error(message)
            raise TypeError(message)

        normalized_strategy = strategy.strip().lower()
        if normalized_strategy not in self.ALLOWED_STRATEGIES:
            message = (
                f"Invalid encoding_strategy '{strategy}'. Expected one of "
                f"{list(self.ALLOWED_STRATEGIES)}."
            )
            logger.error(message)
            raise ValueError(message)
        return normalized_strategy

    def _resolve_categorical_columns(self) -> list[str]:
        if self.categorical_columns is None:
            return list(self.DEFAULT_CATEGORICAL_COLUMNS)
        if isinstance(self.categorical_columns, str):
            return [self.categorical_columns]
        return list(self.categorical_columns)

    def _validate_categorical_columns(self, X: pd.DataFrame) -> None:
        protected_columns = [
            column for column in self.categorical_columns_ if column in self.PROTECTED_COLUMNS
        ]
        if protected_columns:
            message = (
                "CategoricalEncoder must not encode protected columns: "
                f"{protected_columns}"
            )
            logger.error(message)
            raise ValueError(message)

        missing_columns = [column for column in self.categorical_columns_ if column not in X.columns]
        if missing_columns:
            message = f"Missing categorical columns for CategoricalEncoder: {missing_columns}"
            logger.error(message)
            raise ValueError(message)
        logger.info("Categorical columns checked: %s", self.categorical_columns_)

    def _build_encoder(self):
        if self.encoding_strategy_ == "onehot":
            try:
                return OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse_output=False,
                )
            except TypeError:
                return OneHotEncoder(
                    drop="first",
                    handle_unknown="ignore",
                    sparse=False,
                )

        return OrdinalEncoder(
            handle_unknown="use_encoded_value",
            unknown_value=-1,
        )

    def _categorical_frame(self, X: pd.DataFrame) -> pd.DataFrame:
        return X.loc[:, self.categorical_columns_].astype("object")

    def _get_encoded_feature_names(self) -> list[str]:
        if self.encoding_strategy_ == "onehot":
            return self.encoder_.get_feature_names_out(self.categorical_columns_).tolist()
        return list(self.categorical_columns_)

    def _build_output_feature_names(self, X: pd.DataFrame) -> list[str]:
        if self.encoding_strategy_ == "ordinal":
            return list(X.columns)

        non_encoded_columns = [
            column for column in X.columns if column not in self.categorical_columns_
        ]
        return non_encoded_columns + self.encoded_feature_names_

    def _unknown_category_handling(self) -> str:
        if self.encoding_strategy_ == "onehot":
            return 'OneHotEncoder(handle_unknown="ignore")'
        return 'OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=-1)'

    def _categories_summary(self) -> dict[str, list[object]]:
        return {
            column: categories.tolist()
            for column, categories in zip(self.categorical_columns_, self.encoder_.categories_)
        }

    def _check_is_fitted(self) -> None:
        missing_attributes = [
            attribute
            for attribute in (
                "encoding_strategy_",
                "categorical_columns_",
                "encoder_",
                "feature_names_in_",
                "encoded_feature_names_",
                "output_feature_names_",
            )
            if not hasattr(self, attribute)
        ]
        if missing_attributes:
            message = (
                "CategoricalEncoder must be fitted before transform(). "
                f"Missing fitted attributes: {missing_attributes}"
            )
            logger.error(message)
            raise RuntimeError(message)

    def _transform_onehot(self, X: pd.DataFrame) -> pd.DataFrame:
        non_encoded = X.drop(columns=self.categorical_columns_).copy()
        encoded_array = self.encoder_.transform(self._categorical_frame(X))
        encoded = pd.DataFrame(
            encoded_array,
            columns=self.encoded_feature_names_,
            index=X.index,
        )
        return pd.concat([non_encoded, encoded], axis=1)

    def _transform_ordinal(self, X: pd.DataFrame) -> pd.DataFrame:
        output = X.copy()
        encoded_array = self.encoder_.transform(self._categorical_frame(X))
        encoded = pd.DataFrame(
            encoded_array,
            columns=self.categorical_columns_,
            index=X.index,
        )
        for column in self.categorical_columns_:
            output[column] = encoded[column]
        return output

    def _validate_output(self, output: pd.DataFrame) -> None:
        missing_columns = [
            column for column in self.output_feature_names_ if column not in output.columns
        ]
        extra_columns = [
            column for column in output.columns if column not in self.output_feature_names_
        ]
        if missing_columns or extra_columns:
            message = (
                "CategoricalEncoder output validation failed. "
                f"Missing columns: {missing_columns}; extra columns: {extra_columns}"
            )
            logger.error(message)
            raise RuntimeError(message)

        if list(output.columns) != self.output_feature_names_:
            message = (
                "CategoricalEncoder output column order mismatch. Expected "
                f"{self.output_feature_names_}, got {list(output.columns)}."
            )
            logger.error(message)
            raise RuntimeError(message)

    def get_feature_names_out(self, input_features=None):
        """Return fitted output feature names."""

        self._check_is_fitted()
        return np.asarray(self.output_feature_names_, dtype=object)
