from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

STORAGE_DIR = BASE_DIR / "storage"

RAW_DATA_DIR = STORAGE_DIR / "data"
CLEAN_DATA_DIR = STORAGE_DIR / "clean"
MODELS_DIR = STORAGE_DIR / "models"
RESULTS_DIR = STORAGE_DIR / "results"
REPORTS_DIR = STORAGE_DIR / "reports"


def create_storage_directories() -> None:
    """
    Crea las carpetas necesarias para almacenar archivos del proyecto.
    """

    directories = [
        STORAGE_DIR,
        RAW_DATA_DIR,
        CLEAN_DATA_DIR,
        MODELS_DIR,
        RESULTS_DIR,
        REPORTS_DIR,
    ]

    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


create_storage_directories()