from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.data_schema import DatasetType


class AlgorithmType(str, Enum):
    KMEANS = "kmeans"
    DBSCAN = "dbscan"
    AGGLOMERATIVE = "agglomerative"
    GMM = "gmm"


class VectorizerType(str, Enum):
    TFIDF = "tfidf"
    BAG_OF_WORDS = "bow"


class TrainingRequest(BaseModel):
    dataset_type: DatasetType
    filename: str

    algorithm: AlgorithmType = AlgorithmType.KMEANS

    # KMeans, Agglomerative y GMM
    n_clusters: int | None = Field(default=3, ge=2, le=20)

    # DBSCAN
    eps: float | None = Field(default=0.5, gt=0)
    min_samples: int | None = Field(default=5, ge=1)

    # Agglomerative
    linkage: str | None = "ward"

    # Solo para reseñas
    text_column: str | None = None
    vectorizer: VectorizerType | None = VectorizerType.TFIDF

    random_state: int = 42


class TrainingMetrics(BaseModel):
    silhouette_score: float | None = None
    davies_bouldin_score: float | None = None
    calinski_harabasz_score: float | None = None


class TrainingResponse(BaseModel):
    message: str
    model_id: str
    dataset_type: DatasetType
    filename: str
    algorithm: AlgorithmType
    total_records: int
    total_features: int
    clusters_found: int
    noise_points: int = 0
    metrics: TrainingMetrics
    pca_explained_variance: list[float] | None = None