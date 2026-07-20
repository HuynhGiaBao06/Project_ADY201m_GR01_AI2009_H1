"""Central path definitions for the churn pipeline."""

from pathlib import Path


# Project anchors
SRC_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SRC_DIR.parent


# Folder paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw_data"
CHECKPOINT_DATA_DIR = DATA_DIR / "checkpoint_data"
EDA_DATA_DIR = DATA_DIR / "EDA_data"
LOGGER_DATA_DIR = DATA_DIR / "logger_data"

DOCS_DIR = PROJECT_ROOT / "docs"
MODELS_DIR = PROJECT_ROOT / "models"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATA_REPORTS_DIR = REPORTS_DIR / "data_reports"
FIGURES_DIR = REPORTS_DIR / "figures"
SQL_DIR = PROJECT_ROOT / "sql"


# File paths
DATA_RAW_FILE = RAW_DATA_DIR / "data_raw.csv"
TRAIN_DATA_FILE = CHECKPOINT_DATA_DIR / "train_df.csv"
VALIDATION_DATA_FILE = CHECKPOINT_DATA_DIR / "validation_df.csv"
TEST_DATA_FILE = CHECKPOINT_DATA_DIR / "test_df.csv"
LOGGER_DATA_FILE = LOGGER_DATA_DIR / "logger_data.txt"
EDA_DATA_FILE = EDA_DATA_DIR / "EDA_data.csv"


# Compatibility alias used by existing project modules.
DATA_RAW = RAW_DATA_DIR


REQUIRED_DIRECTORIES = (
    DATA_DIR,
    RAW_DATA_DIR,
    CHECKPOINT_DATA_DIR,
    EDA_DATA_DIR,
    LOGGER_DATA_DIR,
    DOCS_DIR,
    MODELS_DIR,
    NOTEBOOKS_DIR,
    REPORTS_DIR,
    DATA_REPORTS_DIR,
    FIGURES_DIR,
    SQL_DIR,
    SRC_DIR,
)


def check_and_create_directories(auto_create: bool = False) -> list[Path]:
    """Check required project folders and optionally create missing folders."""

    missing_dirs = [path for path in REQUIRED_DIRECTORIES if not path.exists()]

    if not missing_dirs:
        print("All required project directories are available.")
        return []

    print(f"Found {len(missing_dirs)} missing project directories:")
    for path in missing_dirs:
        print(f" - {path.relative_to(PROJECT_ROOT)}")

    if auto_create:
        for path in missing_dirs:
            path.mkdir(parents=True, exist_ok=True)
        print("Missing directories were created.")
        return []

    print("Run check_and_create_directories(auto_create=True) to create them.")
    return missing_dirs
