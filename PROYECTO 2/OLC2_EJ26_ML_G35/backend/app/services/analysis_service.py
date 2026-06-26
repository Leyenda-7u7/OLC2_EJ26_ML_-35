from typing import Any

import numpy as np
import pandas as pd

from app.ml.profiling import build_cross_segment_table
from app.schemas.data_schema import DatasetType
from app.schemas.analysis_schema import (
    PCAPoint,
    PCAResponse,
    ClusterProfile,
    ClusterProfileResponse,
    CrossSegmentItem,
    CrossSegmentResponse,
)

from app.services.model_store_service import (
    load_model_artifact,
    load_model_metadata,
    load_results_dataframe,
)


def get_pca_analysis(model_id: str) -> PCAResponse:
    """
    Devuelve los puntos PCA/SVD para graficar en frontend.
    """

    artifact = load_model_artifact(model_id)
    metadata = load_model_metadata(model_id)

    points = [
        PCAPoint(**point)
        for point in artifact["pca_points"]
    ]

    return PCAResponse(
        model_id=model_id,
        dataset_type=DatasetType(metadata["dataset_type"]),
        points=points,
        explained_variance_ratio=metadata.get("pca_explained_variance", []),
        total_explained_variance=metadata.get("pca_total_explained_variance", 0.0),
    )


def build_cluster_summary(group_df: pd.DataFrame) -> dict[str, Any]:
    """
    Genera un resumen simple de un cluster.

    Para numéricos:
    - mean
    - min
    - max

    Para categóricos:
    - valor más frecuente
    """

    summary: dict[str, Any] = {}

    ignored_columns = {"cluster", "pc1", "pc2"}

    usable_columns = [
        column for column in group_df.columns
        if column not in ignored_columns
    ]

    numeric_columns = group_df[usable_columns].select_dtypes(include=["number"]).columns.tolist()
    categorical_columns = group_df[usable_columns].select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    numeric_summary = {}

    for column in numeric_columns:
        numeric_summary[column] = {
            "mean": float(group_df[column].mean()),
            "min": float(group_df[column].min()),
            "max": float(group_df[column].max()),
        }

    categorical_summary = {}

    for column in categorical_columns:
        mode_values = group_df[column].mode(dropna=True)

        if len(mode_values) > 0:
            categorical_summary[column] = str(mode_values.iloc[0])
        else:
            categorical_summary[column] = None

    summary["numeric"] = numeric_summary
    summary["categorical"] = categorical_summary

    return summary


def get_cluster_profiles(model_id: str) -> ClusterProfileResponse:
    """
    Devuelve perfil por cluster:
    - count
    - resumen numérico
    - resumen categórico
    """

    metadata = load_model_metadata(model_id)
    results_df = load_results_dataframe(model_id)

    if "cluster" not in results_df.columns:
        raise ValueError("El CSV de resultados no tiene columna cluster.")

    profiles = []

    for cluster_id, group_df in results_df.groupby("cluster"):
        profile = ClusterProfile(
            cluster=int(cluster_id),
            count=int(len(group_df)),
            summary=build_cluster_summary(group_df),
        )

        profiles.append(profile)

    return ClusterProfileResponse(
        model_id=model_id,
        dataset_type=DatasetType(metadata["dataset_type"]),
        profiles=profiles,
    )


def cross_segment_models(
    freelancer_model_id: str,
    reviews_model_id: str
) -> CrossSegmentResponse:
    """
    Cruza segmentos de freelancers y reseñas usando freelancer_id.

    Requiere que ambos resultados tengan freelancer_id.
    """

    freelancer_results = load_results_dataframe(freelancer_model_id)
    reviews_results = load_results_dataframe(reviews_model_id)

    if "freelancer_id" not in freelancer_results.columns:
        raise ValueError("El modelo de freelancers no tiene columna freelancer_id.")

    if "freelancer_id" not in reviews_results.columns:
        raise ValueError("El modelo de reseñas no tiene columna freelancer_id.")

    freelancer_segments = freelancer_results[
        ["freelancer_id", "cluster"]
    ].rename(
        columns={"cluster": "freelancer_cluster"}
    )

    reviews_segments = reviews_results[
        ["freelancer_id", "cluster"]
    ].rename(
        columns={"cluster": "review_cluster"}
    )

    merged = pd.merge(
        freelancer_segments,
        reviews_segments,
        on="freelancer_id",
        how="outer"
    )

    items = []

    for _, row in merged.iterrows():
        freelancer_cluster = row.get("freelancer_cluster")
        review_cluster = row.get("review_cluster")

        item = CrossSegmentItem(
            freelancer_id=row["freelancer_id"],
            freelancer_cluster=None if pd.isna(freelancer_cluster) else int(freelancer_cluster),
            review_cluster=None if pd.isna(review_cluster) else int(review_cluster),
        )

        items.append(item)

    return CrossSegmentResponse(items=items)

def get_cross_segment_table(
    freelancer_model_id: str,
    reviews_model_id: str
) -> dict[str, Any]:
    """
    Devuelve una tabla cruzada entre el modelo de freelancers
    y el modelo de reseñas.
    """

    freelancer_results = load_results_dataframe(freelancer_model_id)
    reviews_results = load_results_dataframe(reviews_model_id)

    return build_cross_segment_table(
        freelancer_results=freelancer_results,
        review_results=reviews_results
    )