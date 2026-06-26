from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from app.config import RAW_DATA_DIR, CLEAN_DATA_DIR
from app.schemas.data_schema import (
    DatasetType,
    DatasetUploadResponse,
    DatasetCleanResponse,
    DatasetPreviewResponse,
)
from app.ml.preprocessing import clean_basic_dataframe
from app.ml.text_processing import detect_text_column, normalize_text


def safe_filename(filename: str) -> str:
    """
    Evita rutas peligrosas y conserva solo el nombre del archivo.
    """

    return Path(filename).name


def get_dataset_folder(base_dir: Path, dataset_type: DatasetType) -> Path:
    """
    Devuelve la carpeta según el tipo de dataset.
    """

    folder = base_dir / dataset_type.value
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_raw_dataset_path(dataset_type: DatasetType, filename: str) -> Path:
    """
    Ruta donde se guarda el CSV original.
    """

    folder = get_dataset_folder(RAW_DATA_DIR, dataset_type)
    return folder / safe_filename(filename)


def get_clean_dataset_path(dataset_type: DatasetType, filename: str) -> Path:
    """
    Ruta donde se guarda el CSV limpio.
    """

    folder = get_dataset_folder(CLEAN_DATA_DIR, dataset_type)
    return folder / safe_filename(filename)


def dataframe_to_preview(df: pd.DataFrame, limit: int = 10) -> list[dict[str, Any]]:
    """
    Convierte un dataframe a preview JSON.
    Reemplaza NaN por None para evitar problemas en FastAPI.
    """

    preview_df = df.head(limit).replace({np.nan: None})
    return preview_df.to_dict(orient="records")


def read_csv_file(path: Path) -> pd.DataFrame:
    """
    Lee un CSV desde disco.
    """

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    return pd.read_csv(path)


def save_uploaded_dataset(
    file_content: bytes,
    filename: str,
    dataset_type: DatasetType
) -> DatasetUploadResponse:
    """
    Guarda un CSV subido por el usuario.
    """

    filename = safe_filename(filename)

    if not filename.lower().endswith(".csv"):
        raise ValueError("Solo se permiten archivos CSV.")

    path = get_raw_dataset_path(dataset_type, filename)

    with open(path, "wb") as file:
        file.write(file_content)

    df = read_csv_file(path)

    return DatasetUploadResponse(
        message="Archivo cargado correctamente.",
        dataset_type=dataset_type,
        filename=filename,
        total_rows=len(df),
        total_columns=len(df.columns),
        columns=df.columns.tolist(),
        preview=dataframe_to_preview(df),
    )


def clean_dataset(
    dataset_type: DatasetType,
    filename: str
) -> DatasetCleanResponse:
    """
    Limpia un dataset y guarda una copia en storage/clean.

    Para freelancers:
    - normaliza columnas
    - elimina duplicados
    - rellena numéricos con mediana
    - rellena categóricos con 'desconocido'

    Para reviews:
    - aplica la misma limpieza básica
    - detecta texto y lo normaliza
    """

    filename = safe_filename(filename)

    raw_path = get_raw_dataset_path(dataset_type, filename)
    clean_path = get_clean_dataset_path(dataset_type, filename)

    df = read_csv_file(raw_path)

    clean_df, removed_duplicates = clean_basic_dataframe(df)

    missing_before = clean_df.isna().sum().to_dict()
    missing_values_filled: dict[str, int] = {}

    for column, missing_count in missing_before.items():
        if int(missing_count) > 0:
            missing_values_filled[column] = int(missing_count)

    numeric_columns = clean_df.select_dtypes(include=["number"]).columns.tolist()
    object_columns = clean_df.select_dtypes(include=["object", "category"]).columns.tolist()

    for column in numeric_columns:
        median_value = clean_df[column].median()

        if pd.isna(median_value):
            median_value = 0

        clean_df[column] = clean_df[column].fillna(median_value)

    for column in object_columns:
        clean_df[column] = clean_df[column].fillna("desconocido")

    if dataset_type == DatasetType.REVIEWS:
        try:
            text_column = detect_text_column(clean_df)
            clean_df[text_column] = clean_df[text_column].apply(normalize_text)
        except Exception:
            pass

    clean_df.to_csv(clean_path, index=False)

    return DatasetCleanResponse(
        message="Dataset limpiado correctamente.",
        dataset_type=dataset_type,
        original_filename=filename,
        clean_filename=filename,
        total_rows=len(clean_df),
        total_columns=len(clean_df.columns),
        removed_duplicates=removed_duplicates,
        missing_values_filled=missing_values_filled,
        columns=clean_df.columns.tolist(),
    )


def load_dataset_dataframe(
    dataset_type: DatasetType,
    filename: str,
    prefer_clean: bool = True
) -> pd.DataFrame:
    """
    Carga un dataset.

    Si prefer_clean=True, intenta cargar primero la versión limpia.
    Si no existe, usa el CSV original.
    """

    filename = safe_filename(filename)

    clean_path = get_clean_dataset_path(dataset_type, filename)
    raw_path = get_raw_dataset_path(dataset_type, filename)

    if prefer_clean and clean_path.exists():
        return read_csv_file(clean_path)

    return read_csv_file(raw_path)


def get_dataset_preview(
    dataset_type: DatasetType,
    filename: str,
    prefer_clean: bool = True
) -> DatasetPreviewResponse:
    """
    Devuelve información y preview de un dataset.
    """

    df = load_dataset_dataframe(
        dataset_type=dataset_type,
        filename=filename,
        prefer_clean=prefer_clean
    )

    return DatasetPreviewResponse(
        dataset_type=dataset_type,
        filename=safe_filename(filename),
        total_rows=len(df),
        total_columns=len(df.columns),
        columns=df.columns.tolist(),
        preview=dataframe_to_preview(df),
    )