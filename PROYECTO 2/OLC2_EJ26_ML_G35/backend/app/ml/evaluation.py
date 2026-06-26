import numpy as np

from scipy import sparse
from sklearn.cluster import KMeans
from sklearn.metrics import (
    calinski_harabasz_score,
    davies_bouldin_score,
    silhouette_score,
)


def to_dense_if_needed(X):
    """
    Convierte matrices sparse a densas para métricas que no siempre
    aceptan matrices dispersas.
    """

    if sparse.issparse(X):
        return X.toarray()

    return X


def can_compute_cluster_metrics(labels: np.ndarray) -> bool:
    """
    Verifica si se pueden calcular métricas internas.

    Se necesitan al menos 2 clusters válidos.
    En DBSCAN, -1 es ruido y no se toma como cluster válido.
    """

    labels = np.asarray(labels)

    valid_labels = labels[labels != -1]

    if valid_labels.size == 0:
        return False

    unique_labels = set(valid_labels.tolist())

    return len(unique_labels) >= 2


def compute_clustering_metrics(X, labels: np.ndarray) -> dict[str, float | None]:
    """
    Calcula métricas internas de clustering:

    - Silhouette Score:
      Más alto es mejor. Evalúa qué tan separado está cada punto
      de otros clusters.

    - Davies-Bouldin:
      Más bajo es mejor. Evalúa qué tan similares son los clusters
      entre sí.

    - Calinski-Harabasz:
      Más alto es mejor. Evalúa separación entre clusters contra
      compactación interna.
    """

    labels = np.asarray(labels)

    if not can_compute_cluster_metrics(labels):
        return {
            "silhouette_score": None,
            "davies_bouldin_score": None,
            "calinski_harabasz_score": None,
        }

    # Ignorar ruido de DBSCAN
    valid_mask = labels != -1

    X_valid = X[valid_mask]
    labels_valid = labels[valid_mask]

    unique_labels = set(labels_valid.tolist())

    # No se pueden calcular métricas si cada punto quedó como su propio cluster
    if len(unique_labels) >= len(labels_valid):
        return {
            "silhouette_score": None,
            "davies_bouldin_score": None,
            "calinski_harabasz_score": None,
        }

    X_metric = to_dense_if_needed(X_valid)

    return {
        "silhouette_score": float(silhouette_score(X_metric, labels_valid)),
        "davies_bouldin_score": float(davies_bouldin_score(X_metric, labels_valid)),
        "calinski_harabasz_score": float(calinski_harabasz_score(X_metric, labels_valid)),
    }


def calculate_elbow_curve(
    X,
    max_k: int = 10,
    random_state: int = 42
) -> list[dict[str, float]]:
    """
    Calcula la curva del codo para KMeans.

    Retorna una lista como:
    [
        {"k": 2, "inertia": 123.45},
        {"k": 3, "inertia": 98.76}
    ]

    La inercia mide qué tan compactos están los clusters.
    Menor inercia significa clusters más compactos, pero no siempre
    significa mejor modelo. Por eso se busca el "codo".
    """

    n_samples = X.shape[0]

    if n_samples < 3:
        return []

    # Evitamos usar k = n_samples porque no ayuda a interpretar el codo
    max_possible_k = min(max_k, n_samples - 1)

    points = []

    for k in range(2, max_possible_k + 1):
        model = KMeans(
            n_clusters=k,
            n_init=10,
            random_state=random_state
        )

        model.fit(X)

        points.append(
            {
                "k": k,
                "inertia": float(model.inertia_)
            }
        )

    return points


def get_cluster_distribution(labels: np.ndarray) -> dict[str, int]:
    """
    Devuelve la cantidad de registros por cluster.

    Ejemplo:
    {
        "0": 120,
        "1": 85,
        "-1": 10
    }

    En DBSCAN, -1 representa ruido.
    """

    labels = np.asarray(labels)

    distribution = {}

    for label in sorted(set(labels.tolist())):
        distribution[str(label)] = int(np.sum(labels == label))

    return distribution


def interpret_metrics(metrics: dict[str, float | None]) -> str:
    """
    Genera una interpretación simple para mostrar en el frontend
    o en el reporte PDF.
    """

    silhouette = metrics.get("silhouette_score")
    davies = metrics.get("davies_bouldin_score")
    calinski = metrics.get("calinski_harabasz_score")

    if silhouette is None:
        return (
            "No fue posible calcular métricas internas. "
            "Puede que solo exista un cluster válido o que DBSCAN haya marcado "
            "muchos puntos como ruido."
        )

    if silhouette >= 0.7:
        quality = "muy buena separación entre clusters"
    elif silhouette >= 0.5:
        quality = "buena separación entre clusters"
    elif silhouette >= 0.25:
        quality = "separación moderada entre clusters"
    else:
        quality = "separación débil entre clusters"

    return (
        f"El modelo presenta {quality}. "
        f"Silhouette={silhouette:.3f}, "
        f"Davies-Bouldin={davies:.3f}, "
        f"Calinski-Harabasz={calinski:.3f}."
    )