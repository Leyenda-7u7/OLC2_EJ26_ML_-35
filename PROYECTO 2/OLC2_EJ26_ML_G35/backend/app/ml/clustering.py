from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy import sparse

from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors


@dataclass
class ClusteringResult:
    model: Any
    labels: np.ndarray
    algorithm: str
    clusters_found: int
    noise_points: int
    assignment_model: Any | None = None


def to_dense_if_sparse(X):
    """
    Convierte una matriz sparse a densa cuando el algoritmo no soporta sparse.

    Esto sirve especialmente para:
    - AgglomerativeClustering
    - GaussianMixture
    - KNeighborsClassifier
    """

    if sparse.issparse(X):
        return X.toarray()

    return X


def count_clusters(labels: np.ndarray) -> int:
    """
    Cuenta la cantidad de clusters válidos.

    En DBSCAN, la etiqueta -1 representa ruido, por lo que no se cuenta
    como cluster.
    """

    labels = np.asarray(labels)

    valid_labels = labels[labels != -1]

    if valid_labels.size == 0:
        return 0

    return len(set(valid_labels.tolist()))


def count_noise_points(labels: np.ndarray) -> int:
    """
    Cuenta cuántos puntos fueron marcados como ruido.

    Aplica principalmente para DBSCAN, donde el ruido se marca como -1.
    """

    labels = np.asarray(labels)

    return int(np.sum(labels == -1))


def get_label_distribution(labels: np.ndarray) -> dict[str, int]:
    """
    Devuelve la distribución de registros por cluster.

    Ejemplo:
    {
        "0": 50,
        "1": 30,
        "-1": 4
    }
    """

    labels = np.asarray(labels)

    distribution = {}

    for label in sorted(set(labels.tolist())):
        distribution[str(label)] = int(np.sum(labels == label))

    return distribution


def build_assignment_model(
    X,
    labels: np.ndarray,
    n_neighbors: int = 3
) -> KNeighborsClassifier | None:
    """
    Crea un modelo auxiliar KNN para clasificar nuevos registros.

    Se usa cuando el algoritmo original no tiene predict nativo:
    - DBSCAN
    - AgglomerativeClustering

    Para DBSCAN se ignoran los puntos con etiqueta -1 porque son ruido.
    """

    labels = np.asarray(labels)

    valid_mask = labels != -1
    valid_labels = labels[valid_mask]

    if valid_labels.size == 0:
        return None

    X_dense = to_dense_if_sparse(X)
    X_valid = X_dense[valid_mask]

    n_neighbors = min(n_neighbors, len(X_valid))

    if n_neighbors <= 0:
        return None

    knn = KNeighborsClassifier(n_neighbors=n_neighbors)
    knn.fit(X_valid, valid_labels)

    return knn


def train_kmeans(
    X,
    n_clusters: int = 3,
    random_state: int = 42
) -> ClusteringResult:
    """
    Entrena KMeans.

    KMeans sí tiene método predict, por lo que no necesita modelo auxiliar.
    """

    model = KMeans(
        n_clusters=n_clusters,
        n_init=10,
        random_state=random_state
    )

    labels = model.fit_predict(X)

    return ClusteringResult(
        model=model,
        labels=labels,
        algorithm="kmeans",
        clusters_found=count_clusters(labels),
        noise_points=count_noise_points(labels),
        assignment_model=None
    )


def train_dbscan(
    X,
    eps: float = 0.5,
    min_samples: int = 5,
    knn_neighbors: int = 3
) -> ClusteringResult:
    """
    Entrena DBSCAN.

    DBSCAN no necesita k. Usa:
    - eps: radio de vecindad
    - min_samples: cantidad mínima de vecinos para considerar una zona densa

    DBSCAN no tiene predict nativo, por eso se crea un KNN auxiliar
    para clasificar registros nuevos según los clusters ya encontrados.
    """

    model = DBSCAN(
        eps=eps,
        min_samples=min_samples
    )

    labels = model.fit_predict(X)

    assignment_model = build_assignment_model(
        X=X,
        labels=labels,
        n_neighbors=knn_neighbors
    )

    return ClusteringResult(
        model=model,
        labels=labels,
        algorithm="dbscan",
        clusters_found=count_clusters(labels),
        noise_points=count_noise_points(labels),
        assignment_model=assignment_model
    )


def train_agglomerative(
    X,
    n_clusters: int = 3,
    linkage: str = "ward",
    knn_neighbors: int = 3
) -> ClusteringResult:
    """
    Entrena Clustering Jerárquico Aglomerativo.

    Este algoritmo tampoco tiene predict nativo.
    Por eso se crea un KNN auxiliar para asignar registros nuevos
    al cluster más cercano según los datos ya etiquetados.
    """

    X_dense = to_dense_if_sparse(X)

    model = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage=linkage
    )

    labels = model.fit_predict(X_dense)

    assignment_model = build_assignment_model(
        X=X_dense,
        labels=labels,
        n_neighbors=knn_neighbors
    )

    return ClusteringResult(
        model=model,
        labels=labels,
        algorithm="agglomerative",
        clusters_found=count_clusters(labels),
        noise_points=count_noise_points(labels),
        assignment_model=assignment_model
    )


def train_gmm(
    X,
    n_clusters: int = 3,
    random_state: int = 42
) -> ClusteringResult:
    """
    Entrena Gaussian Mixture Model.

    GMM sí tiene predict, igual que KMeans.
    Lo dejamos como opción extra.
    """

    X_dense = to_dense_if_sparse(X)

    model = GaussianMixture(
        n_components=n_clusters,
        random_state=random_state
    )

    labels = model.fit_predict(X_dense)

    return ClusteringResult(
        model=model,
        labels=labels,
        algorithm="gmm",
        clusters_found=count_clusters(labels),
        noise_points=count_noise_points(labels),
        assignment_model=None
    )


def train_clustering_model(
    X,
    algorithm: str = "kmeans",
    n_clusters: int = 3,
    eps: float = 0.5,
    min_samples: int = 5,
    linkage: str = "ward",
    random_state: int = 42,
    knn_neighbors: int = 3
) -> ClusteringResult:
    """
    Entrena el algoritmo seleccionado.

    Algoritmos soportados:
    - kmeans
    - dbscan
    - agglomerative
    - hierarchical
    - gmm
    """

    algorithm = algorithm.lower()

    if algorithm == "kmeans":
        return train_kmeans(
            X=X,
            n_clusters=n_clusters,
            random_state=random_state
        )

    if algorithm == "dbscan":
        return train_dbscan(
            X=X,
            eps=eps,
            min_samples=min_samples,
            knn_neighbors=knn_neighbors
        )

    if algorithm in {"agglomerative", "hierarchical"}:
        return train_agglomerative(
            X=X,
            n_clusters=n_clusters,
            linkage=linkage,
            knn_neighbors=knn_neighbors
        )

    if algorithm == "gmm":
        return train_gmm(
            X=X,
            n_clusters=n_clusters,
            random_state=random_state
        )

    raise ValueError(
        "Algoritmo no soportado. Usa: kmeans, dbscan, agglomerative o gmm."
    )


def predict_cluster(
    model,
    X_new,
    assignment_model=None
) -> int:
    """
    Predice el cluster de un nuevo registro.

    Para modelos con predict nativo:
    - KMeans
    - GMM

    Para modelos sin predict:
    - DBSCAN
    - AgglomerativeClustering

    usa assignment_model, que normalmente será un KNeighborsClassifier.
    """

    if hasattr(model, "predict"):
        X_input = X_new

        if isinstance(model, GaussianMixture):
            X_input = to_dense_if_sparse(X_new)

        prediction = model.predict(X_input)

        return int(prediction[0])

    if assignment_model is None:
        raise ValueError(
            "Este algoritmo no tiene predict nativo y no existe modelo auxiliar KNN."
        )

    X_dense = to_dense_if_sparse(X_new)

    prediction = assignment_model.predict(X_dense)

    return int(prediction[0])


def calculate_k_distance_curve(
    X,
    min_samples: int = 5
) -> list[dict[str, float]]:
    """
    Calcula la curva de distancia al k-ésimo vecino.

    Esta curva ayuda a elegir eps en DBSCAN.
    En clase se vio la idea usando NearestNeighbors.
    """

    X_dense = to_dense_if_sparse(X)

    neighbors = NearestNeighbors(n_neighbors=min_samples)
    neighbors.fit(X_dense)

    distances, _ = neighbors.kneighbors(X_dense)

    k_distances = np.sort(distances[:, -1])

    return [
        {
            "index": int(index),
            "distance": float(distance)
        }
        for index, distance in enumerate(k_distances)
    ]