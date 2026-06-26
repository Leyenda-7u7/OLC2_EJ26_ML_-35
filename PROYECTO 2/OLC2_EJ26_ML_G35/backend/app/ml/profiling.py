from typing import Any

import numpy as np
import pandas as pd


def get_top_terms_by_cluster(
    X_text,
    feature_names: list[str],
    labels: np.ndarray,
    n_terms: int = 8
) -> dict[int, list[dict[str, Any]]]:
    """
    Obtiene los términos más relevantes por cluster.

    Se usa para reseñas vectorizadas con TF-IDF o Bag of Words.

    Para cada cluster:
    - toma las filas pertenecientes a ese cluster
    - calcula el peso promedio de cada término
    - devuelve los términos con mayor peso
    """

    labels = np.asarray(labels)

    result: dict[int, list[dict[str, Any]]] = {}

    for cluster_id in sorted(set(labels.tolist())):
        if cluster_id == -1:
            continue

        cluster_rows = X_text[labels == cluster_id]

        if cluster_rows.shape[0] == 0:
            result[int(cluster_id)] = []
            continue

        avg_weights = np.asarray(cluster_rows.mean(axis=0)).ravel()

        top_indices = avg_weights.argsort()[::-1][:n_terms]

        terms = []

        for index in top_indices:
            terms.append(
                {
                    "term": str(feature_names[index]),
                    "weight": float(avg_weights[index])
                }
            )

        result[int(cluster_id)] = terms

    return result


def build_text_segment_names(
    top_terms_by_cluster: dict[int, list[dict[str, Any]]],
    n_terms: int = 2
) -> dict[int, str]:
    """
    Genera un nombre corto para clusters de texto.

    Ejemplo:
    Cluster 0 -> "Calidad / Comunicacion"
    """

    names: dict[int, str] = {}

    for cluster_id, terms in top_terms_by_cluster.items():
        if not terms:
            names[int(cluster_id)] = f"Segmento {cluster_id}"
            continue

        selected_terms = [
            item["term"].replace("_", " ").capitalize()
            for item in terms[:n_terms]
        ]

        names[int(cluster_id)] = " / ".join(selected_terms)

    return names


def build_numeric_segment_names(
    df: pd.DataFrame,
    numeric_columns: list[str],
    labels: np.ndarray,
    n_terms: int = 2,
    min_z_score: float = 0.3
) -> dict[int, str]:
    """
    Genera nombres cortos para clusters numéricos.

    La idea viene del código del auxiliar:
    - calcula promedio global
    - calcula promedio por cluster
    - mide diferencia usando z-score
    - toma las variables más distintivas

    Ejemplo:
    Cluster 0 -> "Alto hourly rate / Bajo response time hours"
    """

    labels = np.asarray(labels)

    names: dict[int, str] = {}

    if not numeric_columns:
        for cluster_id in sorted(set(labels.tolist())):
            if cluster_id != -1:
                names[int(cluster_id)] = f"Segmento {cluster_id}"
        return names

    numeric_df = df[numeric_columns].copy()

    global_mean = numeric_df.mean()
    global_std = numeric_df.std().replace(0, 1)

    for cluster_id in sorted(set(labels.tolist())):
        if cluster_id == -1:
            continue

        cluster_df = numeric_df[labels == cluster_id]

        if cluster_df.empty:
            names[int(cluster_id)] = f"Segmento {cluster_id}"
            continue

        cluster_mean = cluster_df.mean()

        z_scores = (cluster_mean - global_mean) / global_std

        top = z_scores.abs().sort_values(ascending=False).head(n_terms)

        if top.empty or top.iloc[0] < min_z_score:
            names[int(cluster_id)] = "Segmento promedio"
            continue

        parts = []

        for column in top.index:
            direction = "Alto" if z_scores[column] > 0 else "Bajo"
            readable_column = column.replace("_", " ")
            parts.append(f"{direction} {readable_column}")

        names[int(cluster_id)] = " / ".join(parts)

    return names


def build_contingency_table(
    df: pd.DataFrame,
    row_column: str,
    column_column: str
) -> dict[str, Any]:
    """
    Genera tabla de contingencia con conteos y porcentajes por fila.

    Ejemplo:
    filas = segmentos freelancers
    columnas = segmentos reseñas
    """

    if row_column not in df.columns:
        raise ValueError(f"No existe la columna '{row_column}'.")

    if column_column not in df.columns:
        raise ValueError(f"No existe la columna '{column_column}'.")

    counts = pd.crosstab(
        df[row_column],
        df[column_column]
    )

    percentages = (
        pd.crosstab(
            df[row_column],
            df[column_column],
            normalize="index"
        ).round(4) * 100
    )

    return {
        "counts": counts.reset_index().to_dict(orient="records"),
        "percentages": percentages.reset_index().to_dict(orient="records"),
    }


def build_cross_segment_table(
    freelancer_results: pd.DataFrame,
    review_results: pd.DataFrame
) -> dict[str, Any]:
    """
    Construye tabla cruzada entre segmentos de freelancers y reseñas.

    Une ambos resultados por freelancer_id y calcula:
    - conteos absolutos
    - porcentajes por fila
    """

    if "freelancer_id" not in freelancer_results.columns:
        raise ValueError("El resultado de freelancers no tiene la columna freelancer_id.")

    if "freelancer_id" not in review_results.columns:
        raise ValueError("El resultado de reseñas no tiene la columna freelancer_id.")

    if "cluster" not in freelancer_results.columns:
        raise ValueError("El resultado de freelancers no tiene la columna cluster.")

    if "cluster" not in review_results.columns:
        raise ValueError("El resultado de reseñas no tiene la columna cluster.")

    freelancers = freelancer_results[["freelancer_id", "cluster"]].copy()
    reviews = review_results[["freelancer_id", "cluster"]].copy()

    freelancers = freelancers.rename(
        columns={"cluster": "freelancer_cluster"}
    )

    reviews = reviews.rename(
        columns={"cluster": "review_cluster"}
    )

    # Evita problemas si un CSV trae freelancer_id como número y el otro como texto.
    freelancers["freelancer_id"] = freelancers["freelancer_id"].astype(str)
    reviews["freelancer_id"] = reviews["freelancer_id"].astype(str)

    merged = pd.merge(
        freelancers,
        reviews,
        on="freelancer_id",
        how="inner"
    )

    if merged.empty:
        return {
            "merged_rows": 0,
            "counts": [],
            "percentages": [],
            "message": "No se encontraron freelancer_id coincidentes entre ambos modelos."
        }

    counts = pd.crosstab(
        merged["freelancer_cluster"],
        merged["review_cluster"]
    )

    percentages = pd.crosstab(
        merged["freelancer_cluster"],
        merged["review_cluster"],
        normalize="index"
    ).round(4) * 100

    return {
        "merged_rows": int(len(merged)),
        "counts": counts.reset_index().to_dict(orient="records"),
        "percentages": percentages.reset_index().to_dict(orient="records"),
        "message": "Tabla cruzada generada correctamente."
    }