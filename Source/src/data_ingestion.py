"""Load churn data and create train/validation/test checkpoints."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


from .path import (
    DATA_RAW_FILE,
    TEST_DATA_FILE,
    TRAIN_DATA_FILE,
    VALIDATION_DATA_FILE,
    check_and_create_directories,
)
from .utils.logger import get_pipeline_logger


BASE_CHURN_COLUMNS = [
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
]

ENGINEERED_COLUMNS = [
    "tenure_group",
    "service_diversity",
    "monthly_charges_ratio",
    "is_paperless_electronic",
]


class DataIngestion:
    """Create locked churn data checkpoints before any preprocessing."""

    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.db = None
        self.log = get_pipeline_logger(self.__class__.__name__)
        self.log.debug("Initializing DataIngestion class.")

    def load_from_database(self, view_name: str) -> pd.DataFrame:
        """Load churn data from a PostgreSQL/Neon view."""

        from .db_config import NeonDBManager

        self.log.info(f"Fetching churn data from view '{view_name}'.")
        if self.db is None:
            self.db = NeonDBManager()
        query = f"SELECT * FROM {view_name};"
        return self.db.fetch_data(query)

    def load_from_csv(self, file_path: Path = DATA_RAW_FILE) -> pd.DataFrame:
        """Load raw churn data from the project raw-data folder."""

        if not file_path.exists():
            self.log.error(f"Raw data file not found: {file_path}")
            return pd.DataFrame()

        self.log.info(f"Loading raw churn data from: {file_path}")
        return pd.read_csv(file_path)

    def process_and_checkpoint(
        self,
        view_name: str | None = None,
        target_col: str = "Churn",
        overwrite: bool = False,
    ) -> bool:
        """Load churn data, split 70/15/15, and save checkpoint CSV files."""

        output_files = (TRAIN_DATA_FILE, VALIDATION_DATA_FILE, TEST_DATA_FILE)
        existing_outputs = [path for path in output_files if path.exists()]
        if existing_outputs and not overwrite:
            self.log.warning(
                "Checkpoint files already exist. Test set remains locked. "
                "Pass overwrite=True only when intentionally rebuilding the split."
            )
            for path in existing_outputs:
                self.log.warning(f"Existing checkpoint: {path}")
            return False

        df = self.load_from_database(view_name) if view_name else self.load_from_csv()
        if df.empty:
            self.log.error("Input data is empty. Aborting ingestion.")
            return False

        df = self._select_base_columns(df)
        if df is None:
            return False

        if target_col not in df.columns:
            self.log.error(f"Target column '{target_col}' was not found.")
            return False

        stratify_target = self._get_safe_stratify_target(df, target_col)
        train_df, temp_df = train_test_split(
            df,
            train_size=0.70,
            test_size=0.30,
            random_state=self.random_state,
            stratify=stratify_target,
        )

        temp_stratify_target = self._get_safe_stratify_target(temp_df, target_col)
        validation_df, test_df = train_test_split(
            temp_df,
            train_size=0.50,
            test_size=0.50,
            random_state=self.random_state,
            stratify=temp_stratify_target,
        )

        check_and_create_directories(auto_create=True)
        train_df.to_csv(TRAIN_DATA_FILE, index=False)
        validation_df.to_csv(VALIDATION_DATA_FILE, index=False)
        test_df.to_csv(TEST_DATA_FILE, index=False)

        self.log.info("Successfully saved churn checkpoint splits.")
        self.log.info(f"Train set: {train_df.shape} -> {TRAIN_DATA_FILE.name}")
        self.log.info(f"Validation set: {validation_df.shape} -> {VALIDATION_DATA_FILE.name}")
        self.log.info(f"Test set: {test_df.shape} -> {TEST_DATA_FILE.name} - LOCKED")
        return True

    def _select_base_columns(self, df: pd.DataFrame) -> pd.DataFrame | None:
        """Keep only base churn columns so checkpoints do not contain engineered features."""

        missing_columns = [col for col in BASE_CHURN_COLUMNS if col not in df.columns]
        if missing_columns:
            self.log.error(f"Missing required base churn columns: {missing_columns}")
            return None

        existing_engineered = [col for col in ENGINEERED_COLUMNS if col in df.columns]
        if existing_engineered:
            self.log.warning(
                "Dropping precomputed engineered columns before checkpoint split: "
                f"{existing_engineered}"
            )

        selected_df = df.loc[:, BASE_CHURN_COLUMNS].copy()
        self.log.info(f"Selected base churn columns: {BASE_CHURN_COLUMNS}")
        self.log.info(f"Base churn dataset shape after column selection: {selected_df.shape}")
        return selected_df

    def _get_safe_stratify_target(self, df: pd.DataFrame, target_col: str):
        """Return target values for stratify when class distribution supports it."""

        target = df[target_col]
        if target.isna().any():
            self.log.warning(
                f"Target column '{target_col}' contains missing values. Splitting without stratify."
            )
            return None

        class_counts = target.value_counts()
        if len(class_counts) < 2:
            self.log.warning(
                f"Target column '{target_col}' has fewer than two classes. Splitting without stratify."
            )
            return None

        if class_counts.min() < 2:
            self.log.warning(
                f"Target column '{target_col}' has a class with fewer than two rows. "
                "Splitting without stratify."
            )
            return None

        return target


if __name__ == "__main__":
    ingestor = DataIngestion()
    ingestor.process_and_checkpoint(view_name="vw_cleaning_data", target_col="Churn")
