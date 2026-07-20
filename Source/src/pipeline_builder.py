"""Build and apply preprocessing branches for the churn pipeline."""

from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd
from sklearn.pipeline import Pipeline

from .pre_processing.capping_outlier import LogisticNumericTransformer
from .pre_processing.categorical_encoder import CategoricalEncoder
from .pre_processing.feature_engineer import FeatureEngineer
from .pre_processing.scaler import LogisticScaler
from .pre_processing.target_encoder import TargetEncoder


logger = logging.getLogger(__name__)


class PipelineBuilder:
    """Compose train-fitted preprocessing branches without training models."""

    REQUIRED_BASE_COLUMNS = (
        "ID",
        "Churn",
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
    )

    PROTECTED_COLUMNS = ("ID", "Churn")

    def __init__(self):
        self.logistic_stage_a_pipeline_ = None
        self.logistic_scaler_ = None
        self.tree_pipeline_ = None
        logger.info("PipelineBuilder initialized.")

    def build_logistic_pipeline(self) -> Pipeline:
        """Build the unscaled Logistic preprocessing stage.

        Scaling is fitted as a second controlled stage after one-hot encoding so
        scale columns can be resolved from actual post-encoding train output.
        """

        logger.info("Building logistic preprocessing stage A pipeline.")
        return Pipeline(
            steps=[
                ("target", TargetEncoder()),
                ("features", FeatureEngineer()),
                ("numeric", LogisticNumericTransformer()),
                ("categorical", CategoricalEncoder(encoding_strategy="onehot")),
            ]
        )

    def build_tree_pipeline(self) -> Pipeline:
        """Build the Tree preprocessing branch without capping, log transform, or scaling."""

        logger.info("Building tree preprocessing pipeline.")
        return Pipeline(
            steps=[
                ("target", TargetEncoder()),
                ("features", FeatureEngineer()),
                ("categorical", CategoricalEncoder(encoding_strategy="ordinal")),
            ]
        )

    def fit_transform_logistic(self, train_df: pd.DataFrame) -> pd.DataFrame:
        """Fit Logistic preprocessing on train and return transformed train data."""

        logger.info("Logistic fit_transform started.")
        self._validate_input_dataframe(train_df, "train_df")
        self._validate_required_base_columns(train_df, "train_df")
        logger.info("Logistic train input shape: %s", train_df.shape)

        self.logistic_stage_a_pipeline_ = self.build_logistic_pipeline()
        stage_a_train = self.logistic_stage_a_pipeline_.fit_transform(train_df)
        self._validate_output_preserves_protected_columns(stage_a_train, "logistic stage A")
        logger.info("Logistic stage A output shape: %s", stage_a_train.shape)

        scale_columns = self._resolve_logistic_scale_columns(stage_a_train)
        logger.info("Resolved logistic scale columns: %s", scale_columns)
        self.logistic_scaler_ = LogisticScaler(scale_columns=scale_columns)
        logistic_train = self.logistic_scaler_.fit_transform(stage_a_train)
        self._validate_output_preserves_protected_columns(logistic_train, "logistic final")

        logger.info("Final logistic train output shape: %s", logistic_train.shape)
        logger.info("Logistic fit_transform completed.")
        return logistic_train

    def transform_logistic(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform validation/test data with fitted Logistic preprocessing."""

        logger.info("Logistic transform started.")
        self._check_logistic_is_fitted()
        self._validate_input_dataframe(df, "logistic transform input")
        self._validate_required_base_columns(df, "logistic transform input")
        logger.info("Logistic transform input shape: %s", df.shape)

        stage_a_output = self.logistic_stage_a_pipeline_.transform(df)
        self._validate_output_preserves_protected_columns(stage_a_output, "logistic stage A")
        logger.info("Logistic stage A transform output shape: %s", stage_a_output.shape)

        logistic_output = self.logistic_scaler_.transform(stage_a_output)
        self._validate_output_preserves_protected_columns(logistic_output, "logistic final")
        logger.info("Final logistic transform output shape: %s", logistic_output.shape)
        logger.info("Logistic transform completed.")
        return logistic_output

    def fit_transform_tree(self, train_df: pd.DataFrame) -> pd.DataFrame:
        """Fit Tree preprocessing on train and return transformed train data."""

        logger.info("Tree fit_transform started.")
        self._validate_input_dataframe(train_df, "train_df")
        self._validate_required_base_columns(train_df, "train_df")
        logger.info("Tree train input shape: %s", train_df.shape)

        self.tree_pipeline_ = self.build_tree_pipeline()
        tree_train = self.tree_pipeline_.fit_transform(train_df)
        self._validate_output_preserves_protected_columns(tree_train, "tree final")
        self._validate_tree_pipeline_rules()

        logger.info("Final tree train output shape: %s", tree_train.shape)
        logger.info("Tree fit_transform completed.")
        return tree_train

    def transform_tree(self, df: pd.DataFrame) -> pd.DataFrame:
        """Transform validation/test data with fitted Tree preprocessing."""

        logger.info("Tree transform started.")
        self._check_tree_is_fitted()
        self._validate_input_dataframe(df, "tree transform input")
        self._validate_required_base_columns(df, "tree transform input")
        logger.info("Tree transform input shape: %s", df.shape)

        tree_output = self.tree_pipeline_.transform(df)
        self._validate_output_preserves_protected_columns(tree_output, "tree final")
        self._validate_tree_pipeline_rules()

        logger.info("Final tree transform output shape: %s", tree_output.shape)
        logger.info("Tree transform completed.")
        return tree_output

    def fit_transform_all(
        self,
        train_df: pd.DataFrame,
        validation_df: pd.DataFrame | None = None,
        test_df: pd.DataFrame | None = None,
    ) -> dict[str, dict[str, pd.DataFrame]]:
        """Fit both branches on train and optionally transform validation/test."""

        logger.info("fit_transform_all started.")
        logger.info("Train input shape: %s", getattr(train_df, "shape", None))
        if validation_df is not None:
            logger.info("Validation input shape: %s", getattr(validation_df, "shape", None))
            self._validate_input_dataframe(validation_df, "validation_df")
            self._validate_required_base_columns(validation_df, "validation_df")
        if test_df is not None:
            logger.info("Test input shape: %s", getattr(test_df, "shape", None))
            self._validate_input_dataframe(test_df, "test_df")
            self._validate_required_base_columns(test_df, "test_df")

        outputs = {
            "logistic": {"train": self.fit_transform_logistic(train_df)},
            "tree": {"train": self.fit_transform_tree(train_df)},
        }

        if validation_df is not None:
            outputs["logistic"]["validation"] = self.transform_logistic(validation_df)
            outputs["tree"]["validation"] = self.transform_tree(validation_df)

        if test_df is not None:
            outputs["logistic"]["test"] = self.transform_logistic(test_df)
            outputs["tree"]["test"] = self.transform_tree(test_df)

        logger.info("fit_transform_all completed.")
        return outputs

    def _validate_input_dataframe(self, df: pd.DataFrame, name: str) -> None:
        if not isinstance(df, pd.DataFrame):
            message = f"{name} must be a pandas DataFrame."
            logger.error(message)
            raise TypeError(message)

    def _validate_required_base_columns(self, df: pd.DataFrame, name: str) -> None:
        missing_columns = [column for column in self.REQUIRED_BASE_COLUMNS if column not in df.columns]
        if missing_columns:
            message = f"{name} is missing required base columns: {missing_columns}"
            logger.error(message)
            raise ValueError(message)
        logger.info("Required base columns checked for %s.", name)

    def _validate_output_preserves_protected_columns(self, df: pd.DataFrame, name: str) -> None:
        missing_columns = [column for column in self.PROTECTED_COLUMNS if column not in df.columns]
        if missing_columns:
            message = f"{name} output dropped protected columns: {missing_columns}"
            logger.error(message)
            raise RuntimeError(message)

    def _resolve_logistic_scale_columns(self, df: pd.DataFrame) -> list[str]:
        """Resolve existing numeric post-one-hot columns for LogisticScaler."""

        self._validate_input_dataframe(df, "logistic stage A output")
        scale_columns = []
        for column in df.columns:
            if column in self.PROTECTED_COLUMNS:
                continue
            if pd.api.types.is_numeric_dtype(df[column]):
                scale_columns.append(column)

        if not scale_columns:
            message = "No numeric columns were available for LogisticScaler."
            logger.error(message)
            raise RuntimeError(message)
        return scale_columns

    def _check_logistic_is_fitted(self) -> None:
        if self.logistic_stage_a_pipeline_ is None or self.logistic_scaler_ is None:
            message = "Logistic preprocessing must be fitted before transform_logistic()."
            logger.error(message)
            raise RuntimeError(message)

    def _check_tree_is_fitted(self) -> None:
        if self.tree_pipeline_ is None:
            message = "Tree preprocessing must be fitted before transform_tree()."
            logger.error(message)
            raise RuntimeError(message)

    def _validate_tree_pipeline_rules(self) -> None:
        if self.tree_pipeline_ is None:
            return
        forbidden_steps = {"numeric", "scaler"}
        present_forbidden_steps = [
            name for name, _ in self.tree_pipeline_.steps if name in forbidden_steps
        ]
        if present_forbidden_steps:
            message = (
                "Tree preprocessing must not include capping/log transform/scaling steps: "
                f"{present_forbidden_steps}"
            )
            logger.error(message)
            raise RuntimeError(message)


def build_logistic_pipeline() -> Pipeline:
    """Convenience factory for the unscaled Logistic preprocessing stage."""

    return PipelineBuilder().build_logistic_pipeline()


def build_tree_pipeline() -> Pipeline:
    """Convenience factory for the Tree preprocessing branch."""

    return PipelineBuilder().build_tree_pipeline()
