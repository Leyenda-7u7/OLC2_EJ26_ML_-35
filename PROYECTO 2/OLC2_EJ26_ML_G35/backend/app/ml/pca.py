from dataclasses import dataclass
from typing import Any

import numpy as np

from scipy import sparse
from sklearn.decomposition import PCA, TruncatedSVD


@dataclass
class ReductionResult:
    reducer: Any
    coordinates: np.ndarray
    explained_variance_ratio: list[float]
    total_explained_variance: float
    method: str


def reduce_to_2d(
    X,
    random_state: int = 42
) -> ReductionResult:
    """
    Reduce una matriz a 2 dimensiones para graficar.

    Si X es densa:
    - usa PCA

    Si X es dispersa, como TF-IDF:
    - usa TruncatedSVD

    Si solo hay una feature o una muestra:
    - crea coordenadas básicas para evitar errores

    Retorna:
    - modelo reductor
    - coordenadas 2D
    - varianza explicada
    - método usado
    """

    n_samples, n_features = X.shape

    # Caso extremo: dataset vacío
    if n_samples == 0:
        return ReductionResult(
            reducer=None,
            coordinates=np.empty((0, 2)),
            explained_variance_ratio=[0.0, 0.0],
            total_explained_variance=0.0,
            method="empty"
        )

    # Caso extremo: solo una muestra
    if n_samples == 1:
        return ReductionResult(
            reducer=None,
            coordinates=np.array([[0.0, 0.0]]),
            explained_variance_ratio=[1.0, 0.0],
            total_explained_variance=1.0,
            method="single_sample"
        )

    # Caso extremo: solo una feature
    if n_features == 1:
        dense_x = X.toarray() if sparse.issparse(X) else np.asarray(X)

        coordinates = np.column_stack(
            [dense_x[:, 0], np.zeros(n_samples)]
        )

        return ReductionResult(
            reducer=None,
            coordinates=coordinates,
            explained_variance_ratio=[1.0, 0.0],
            total_explained_variance=1.0,
            method="single_feature"
        )

    # Si la matriz es sparse, normalmente viene de TF-IDF o Bag of Words.
    # En ese caso usamos TruncatedSVD porque PCA no trabaja bien con sparse.
    if sparse.issparse(X):
        reducer = TruncatedSVD(
            n_components=2,
            random_state=random_state
        )

        coordinates = reducer.fit_transform(X)

        explained_variance_ratio = [
            float(value)
            for value in reducer.explained_variance_ratio_
        ]

        return ReductionResult(
            reducer=reducer,
            coordinates=coordinates,
            explained_variance_ratio=explained_variance_ratio,
            total_explained_variance=float(sum(explained_variance_ratio)),
            method="truncated_svd"
        )

    # Para matrices densas usamos PCA normal.
    reducer = PCA(n_components=2)

    coordinates = reducer.fit_transform(X)

    explained_variance_ratio = [
        float(value)
        for value in reducer.explained_variance_ratio_
    ]

    return ReductionResult(
        reducer=reducer,
        coordinates=coordinates,
        explained_variance_ratio=explained_variance_ratio,
        total_explained_variance=float(sum(explained_variance_ratio)),
        method="pca"
    )


def transform_to_2d(reducer, X):
    """
    Transforma nuevos datos usando un PCA/SVD ya entrenado.

    Si reducer es None, significa que el entrenamiento cayó en un caso
    especial como single_feature o single_sample.
    """

    if reducer is None:
        n_samples = X.shape[0]

        if n_samples == 0:
            return np.empty((0, 2))

        dense_x = X.toarray() if sparse.issparse(X) else np.asarray(X)

        if dense_x.shape[1] == 1:
            return np.column_stack(
                [dense_x[:, 0], np.zeros(n_samples)]
            )

        return np.zeros((n_samples, 2))

    return reducer.transform(X)


def build_pca_points(
    coordinates: np.ndarray,
    labels: np.ndarray,
    ids: list[Any] | None = None
) -> list[dict[str, Any]]:
    """
    Convierte coordenadas y clusters en una lista lista para enviar al frontend.

    Ejemplo:
    [
        {"id": 1, "pc1": 0.25, "pc2": -1.31, "cluster": 0}
    ]
    """

    points = []

    for index, coordinate in enumerate(coordinates):
        point = {
            "pc1": float(coordinate[0]),
            "pc2": float(coordinate[1]),
            "cluster": int(labels[index])
        }

        if ids is not None:
            point["id"] = ids[index]

        points.append(point)

    return points