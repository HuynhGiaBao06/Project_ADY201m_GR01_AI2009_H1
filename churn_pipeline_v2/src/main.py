"""Main orchestration entry point for the refactored churn pipeline."""

from __future__ import annotations

import argparse
from typing import Any

import pandas as pd

from churn_pipeline_v2.src.data_ingestion import DataIngestion
from churn_pipeline_v2.src.path import (
    TEST_DATA_FILE,
    TRAIN_DATA_FILE,
    VALIDATION_DATA_FILE,
    check_and_create_directories,
)
from churn_pipeline_v2.src.pipeline_builder import PipelineBuilder
from churn_pipeline_v2.src.utils.logger import get_pipeline_logger


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

CHECKPOINT_FILES = {
    "train": TRAIN_DATA_FILE,
    "validation": VALIDATION_DATA_FILE,
    "test": TEST_DATA_FILE,
}

BRANCH_NAMES = ("logistic", "tree")
SPLIT_NAMES = ("train", "validation", "test")
PROTECTED_COLUMNS = ("ID", "Churn")


def run_pipeline(
    force_ingestion: bool = False,
    use_database: bool = False,
    view_name: str | None = None,
) -> dict[str, Any]:
    """Run checkpoint-aware ingestion and preprocessing branch orchestration.

    The function does not train models, evaluate models, save artifacts, or
    write model-ready CSV outputs. It returns fitted preprocessing state and
    in-memory preprocessed DataFrames for notebooks to consume later.
    """

    check_and_create_directories(auto_create=True)
    log = get_pipeline_logger("main")
    log.info("Refactored churn pipeline orchestration started.")
    log.info(
        "Run options: force_ingestion=%s, use_database=%s, view_name=%s",
        force_ingestion,
        use_database,
        view_name,
    )
    _log_checkpoint_paths(log)

    if use_database and not view_name:
        raise ValueError("view_name is required when use_database=True.")

    if force_ingestion or not _check_checkpoint_files_exist():
        log.info("Checkpoint ingestion will run.")
        ingestor = DataIngestion()
        ingestion_success = ingestor.process_and_checkpoint(
            view_name=view_name if use_database else None,
            target_col="Churn",
            overwrite=force_ingestion,
        )
        if not ingestion_success:
            raise RuntimeError(
                "Data ingestion did not complete successfully. "
                "Check existing checkpoints, source data, and force_ingestion settings."
            )
    else:
        log.info("All checkpoint files exist; ingestion skipped.")

    _validate_checkpoint_files_exist()
    train_df, validation_df, test_df = _load_checkpoint_data()
    _validate_input_dataframes(
        {
            "train": train_df,
            "validation": validation_df,
            "test": test_df,
        }
    )
    log.info("Loaded train checkpoint shape: %s", train_df.shape)
    log.info("Loaded validation checkpoint shape: %s", validation_df.shape)
    log.info("Loaded test checkpoint shape: %s", test_df.shape)

    builder = PipelineBuilder()
    outputs = builder.fit_transform_all(train_df, validation_df, test_df)
    _validate_preprocessing_outputs(outputs)
    _log_output_shapes(outputs, log)

    log.info("Preprocessing branch orchestration completed.")
    log.info("Refactored churn pipeline orchestration finished.")
    return {
        "builder": builder,
        "outputs": outputs,
    }


def _check_checkpoint_files_exist() -> bool:
    """Return whether all locked checkpoint files currently exist."""

    return all(path.exists() for path in CHECKPOINT_FILES.values())


def _validate_checkpoint_files_exist() -> None:
    """Raise a clear error if any expected checkpoint file is missing."""

    missing_files = [
        f"{split}: {path}"
        for split, path in CHECKPOINT_FILES.items()
        if not path.exists()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Missing required checkpoint files after ingestion step: "
            f"{missing_files}"
        )


def _load_checkpoint_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, validation, and test checkpoint DataFrames."""

    return (
        pd.read_csv(TRAIN_DATA_FILE),
        pd.read_csv(VALIDATION_DATA_FILE),
        pd.read_csv(TEST_DATA_FILE),
    )


def _validate_input_dataframes(dataframes: dict[str, pd.DataFrame]) -> None:
    """Validate checkpoint DataFrames before preprocessing."""

    for split, df in dataframes.items():
        _validate_dataframe(df, split)
        missing_columns = [
            column for column in REQUIRED_BASE_COLUMNS if column not in df.columns
        ]
        if missing_columns:
            raise ValueError(
                f"{split} checkpoint is missing required base columns: "
                f"{missing_columns}"
            )


def _validate_preprocessing_outputs(
    outputs: dict[str, dict[str, pd.DataFrame]],
) -> None:
    """Validate nested preprocessing output structure and protected columns."""

    if not isinstance(outputs, dict):
        raise TypeError("Preprocessing outputs must be a nested dictionary.")

    missing_branches = [branch for branch in BRANCH_NAMES if branch not in outputs]
    if missing_branches:
        raise RuntimeError(
            f"Preprocessing outputs missing branches: {missing_branches}"
        )

    for branch in BRANCH_NAMES:
        branch_outputs = outputs[branch]
        if not isinstance(branch_outputs, dict):
            raise TypeError(f"{branch} outputs must be a dictionary.")

        missing_splits = [
            split for split in SPLIT_NAMES if split not in branch_outputs
        ]
        if missing_splits:
            raise RuntimeError(
                f"{branch} outputs missing splits: {missing_splits}"
            )

        for split in SPLIT_NAMES:
            name = f"{branch}.{split}"
            df = branch_outputs[split]
            _validate_dataframe(df, name)
            missing_protected = [
                column for column in PROTECTED_COLUMNS if column not in df.columns
            ]
            if missing_protected:
                raise RuntimeError(
                    f"{name} output dropped protected columns: "
                    f"{missing_protected}"
                )


def _validate_dataframe(df: pd.DataFrame, name: str) -> None:
    """Validate that an object is a non-empty pandas DataFrame."""

    if not isinstance(df, pd.DataFrame):
        raise TypeError(f"{name} must be a pandas DataFrame.")
    if df.empty:
        raise ValueError(f"{name} DataFrame is empty.")


def _log_checkpoint_paths(log) -> None:
    """Log checkpoint file paths used by orchestration."""

    for split, path in CHECKPOINT_FILES.items():
        log.info("%s checkpoint path: %s", split.capitalize(), path)


def _log_output_shapes(
    outputs: dict[str, dict[str, pd.DataFrame]],
    log,
) -> None:
    """Log output shapes for each preprocessing branch and split."""

    for branch in BRANCH_NAMES:
        for split in SPLIT_NAMES:
            log.info(
                "%s %s output shape: %s",
                branch.capitalize(),
                split,
                outputs[branch][split].shape,
            )


def _build_arg_parser() -> argparse.ArgumentParser:
    """Build a minimal safe CLI for module execution."""

    parser = argparse.ArgumentParser(
        description="Run safe ADY201m churn refactor orchestration."
    )
    parser.add_argument(
        "--force-ingestion",
        action="store_true",
        help="Rebuild checkpoint splits through DataIngestion overwrite=True.",
    )
    parser.add_argument(
        "--use-database",
        action="store_true",
        help="Load raw data through DataIngestion database mode.",
    )
    parser.add_argument(
        "--view-name",
        default=None,
        help="Database view name used only with --use-database.",
    )
    return parser


def main() -> dict[str, Any]:
    """CLI wrapper for safe default orchestration."""

    args = _build_arg_parser().parse_args()
    return run_pipeline(
        force_ingestion=args.force_ingestion,
        use_database=args.use_database,
        view_name=args.view_name,
    )


if __name__ == "__main__":
    main()
