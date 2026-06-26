from typing import Any

import pandas as pd

from app.schemas.data_schema import DatasetType
from app.schemas.classification_schema import (
    ClassificationRequest,
    ClassificationResponse,
)

from app.ml.preprocessing import normalize_column_names
from app.ml.text_processing import transform_text_record
from app.ml.clustering import predict_cluster

from app.services.model_store_service import load_model_artifact


def build_cluster_description(
    artifact: dict[str, Any],
    cluster: int
) -> tuple[str | None, str]:
    """
    Genera el nombre y la descripción interpretativa del cluster asignado.

    Usa la información guardada durante el entrenamiento:
    - segment_names
    - label_distribution
    - top_terms para reseñas
    """

    distribution = artifact.get("label_distribution", {})
    segment_names = artifact.get("segment_names", {})
    top_terms = artifact.get("top_terms", {})

    cluster_key = str(cluster)

    cluster_count = distribution.get(
        cluster_key,
        distribution.get(cluster, 0)
    )

    segment_name = segment_names.get(
        cluster_key,
        segment_names.get(cluster, f"Segmento {cluster}")
    )

    if cluster == -1:
        return (
            "Ruido / caso atípico",
            "El registro fue clasificado como ruido o caso atípico. "
            "Esto puede ocurrir principalmente con DBSCAN cuando el registro "
            "no se parece lo suficiente a los segmentos existentes."
        )

    terms = top_terms.get(
        cluster_key,
        top_terms.get(cluster, [])
    )

    if terms:
        selected_terms = []

        for item in terms[:5]:
            if isinstance(item, dict):
                term = item.get("term", "")
            else:
                term = str(item)

            if term:
                selected_terms.append(str(term))

        terms_text = ", ".join(selected_terms)

        description = (
            f"El registro fue asignado al segmento '{segment_name}'. "
            f"Este segmento contiene aproximadamente {cluster_count} registros "
            f"del entrenamiento. Los términos más representativos asociados son: "
            f"{terms_text}."
        )
    else:
        description = (
            f"El registro fue asignado al segmento '{segment_name}'. "
            f"Este segmento contiene aproximadamente {cluster_count} registros "
            "del entrenamiento y representa un grupo con características "
            "similares según las variables analizadas."
        )

    return segment_name, description


def build_tabular_input_dataframe(
    values: dict[str, Any],
    numeric_columns: list[str],
    categorical_columns: list[str]
) -> pd.DataFrame:
    """
    Construye un DataFrame para clasificar un nuevo freelancer.

    Agrega columnas faltantes con None para que el ColumnTransformer
    entrenado no falle al transformar.
    """

    record_df = pd.DataFrame([values])
    record_df = normalize_column_names(record_df)

    expected_columns = numeric_columns + categorical_columns

    for column in expected_columns:
        if column not in record_df.columns:
            record_df[column] = None

    return record_df


def classify_record(request: ClassificationRequest) -> ClassificationResponse:
    """
    Clasifica un nuevo registro sin reentrenar el modelo.

    Para freelancers:
    - usa el preprocessor tabular entrenado.

    Para reseñas:
    - usa el vectorizer entrenado durante el entrenamiento.
    """

    artifact = load_model_artifact(request.model_id)

    artifact_dataset_type = artifact["dataset_type"]

    if artifact_dataset_type != request.dataset_type.value:
        raise ValueError(
            "El tipo de dataset del modelo no coincide con el tipo enviado."
        )

    model = artifact["model"]
    assignment_model = artifact.get("assignment_model")

    if request.dataset_type == DatasetType.FREELANCERS:
        processor = artifact["processor"]

        if processor is None:
            raise ValueError(
                "El modelo seleccionado no tiene preprocesador tabular."
            )

        numeric_columns = artifact.get("numeric_columns", [])
        categorical_columns = artifact.get("categorical_columns", [])

        record_df = build_tabular_input_dataframe(
            values=request.values,
            numeric_columns=numeric_columns,
            categorical_columns=categorical_columns,
        )

        X_new = processor.transform(record_df)

    elif request.dataset_type == DatasetType.REVIEWS:
        vectorizer = artifact["vectorizer"]
        text_column = artifact["text_column"]

        if vectorizer is None:
            raise ValueError(
                "El modelo seleccionado no tiene vectorizador de texto."
            )

        if not text_column:
            raise ValueError(
                "El modelo seleccionado no tiene columna de texto registrada."
            )

        X_new = transform_text_record(
            values=request.values,
            text_column=text_column,
            vectorizer=vectorizer,
        )

    else:
        raise ValueError("Tipo de dataset no soportado.")

    cluster = predict_cluster(
        model=model,
        X_new=X_new,
        assignment_model=assignment_model,
    )

    segment_name, description = build_cluster_description(
        artifact=artifact,
        cluster=cluster,
    )

    return ClassificationResponse(
        model_id=request.model_id,
        dataset_type=request.dataset_type,
        cluster=cluster,
        segment_name=segment_name,
        description=description,
    )