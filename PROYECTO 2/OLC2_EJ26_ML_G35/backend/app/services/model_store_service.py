import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from app.config import MODELS_DIR, RESULTS_DIR


def get_model_dir(model_id: str) -> Path:
    """
    Devuelve la carpeta de un modelo entrenado.
    """

    model_dir = MODELS_DIR / model_id
    model_dir.mkdir(parents=True, exist_ok=True)
    return model_dir


def get_model_artifact_path(model_id: str) -> Path:
    """
    Ruta del archivo joblib principal.
    """

    return get_model_dir(model_id) / "artifact.joblib"


def get_model_metadata_path(model_id: str) -> Path:
    """
    Ruta del metadata JSON.
    """

    return get_model_dir(model_id) / "metadata.json"


def get_result_csv_path(model_id: str) -> Path:
    """
    Ruta del CSV de resultados del modelo.
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    return RESULTS_DIR / f"{model_id}_results.csv"


def save_model_artifact(
    model_id: str,
    artifact: dict[str, Any],
    metadata: dict[str, Any],
    results_df: pd.DataFrame
) -> None:
    """
    Guarda:
    - artifact.joblib
    - metadata.json
    - results.csv
    """

    artifact_path = get_model_artifact_path(model_id)
    metadata_path = get_model_metadata_path(model_id)
    result_csv_path = get_result_csv_path(model_id)

    joblib.dump(artifact, artifact_path)

    with open(metadata_path, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=4)

    results_df.to_csv(result_csv_path, index=False)


def load_model_artifact(model_id: str) -> dict[str, Any]:
    """
    Carga artifact.joblib.
    """

    artifact_path = get_model_artifact_path(model_id)

    if not artifact_path.exists():
        raise FileNotFoundError(f"No existe el modelo con id: {model_id}")

    return joblib.load(artifact_path)


def load_model_metadata(model_id: str) -> dict[str, Any]:
    """
    Carga metadata.json.
    """

    metadata_path = get_model_metadata_path(model_id)

    if not metadata_path.exists():
        raise FileNotFoundError(f"No existe metadata para el modelo: {model_id}")

    with open(metadata_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_results_dataframe(model_id: str) -> pd.DataFrame:
    """
    Carga el CSV de resultados del modelo.
    """

    result_csv_path = get_result_csv_path(model_id)

    if not result_csv_path.exists():
        raise FileNotFoundError(f"No existe CSV de resultados para el modelo: {model_id}")

    return pd.read_csv(result_csv_path)