# Path Guideline

`churn_pipeline_v2/src/path.py` is the single source of truth for paths in the
ADY201m churn refactor.

Modules should import paths through refactor-safe package or relative imports instead
of hard-coding folder or file locations. Do not use ambiguous legacy-style imports
such as `from src.path import ...` or `from src.paths import ...` inside
`churn_pipeline_v2/`.

## Required Folder Constants

- `PROJECT_ROOT`
- `SRC_DIR`
- `DATA_DIR`
- `RAW_DATA_DIR`
- `CHECKPOINT_DATA_DIR`
- `EDA_DATA_DIR`
- `LOGGER_DATA_DIR`
- `DOCS_DIR`
- `MODELS_DIR`
- `NOTEBOOKS_DIR`
- `REPORTS_DIR`
- `DATA_REPORTS_DIR`
- `FIGURES_DIR`
- `SQL_DIR`

## Required File Constants

- `DATA_RAW_FILE`
- `TRAIN_DATA_FILE`
- `VALIDATION_DATA_FILE`
- `TEST_DATA_FILE`
- `LOGGER_DATA_FILE`
- `EDA_DATA_FILE`

## Data Ingestion Checkpoints

`data_ingestion.py` is responsible for creating only the locked split checkpoint files:

- `data/checkpoint_data/train_df.csv`
- `data/checkpoint_data/validation_df.csv`
- `data/checkpoint_data/test_df.csv`

The split rule is:

- Train: 70%
- Validation: 15%
- Test: 15%

The test checkpoint is conceptually locked after ingestion and should only be used for
final evaluation.

## Refactor Data Storage Rule

The refactor architecture should not save intermediate preprocessed CSV files into
`data/processing/`.

Preprocessing outputs should be managed by the pipeline flow, and model training belongs
to notebooks.

## Usage Example

```python
from churn_pipeline_v2.src.path import (
    DATA_RAW_FILE,
    TRAIN_DATA_FILE,
    VALIDATION_DATA_FILE,
    TEST_DATA_FILE,
    check_and_create_directories,
)

check_and_create_directories(auto_create=True)
```

For modules directly inside `churn_pipeline_v2/src/`, relative imports are also
acceptable:

```python
from .path import TRAIN_DATA_FILE, VALIDATION_DATA_FILE, TEST_DATA_FILE
```

For modules inside subpackages such as `churn_pipeline_v2/src/utils/`, use
parent-relative imports:

```python
from ..path import LOGGER_DATA_FILE, check_and_create_directories
```
