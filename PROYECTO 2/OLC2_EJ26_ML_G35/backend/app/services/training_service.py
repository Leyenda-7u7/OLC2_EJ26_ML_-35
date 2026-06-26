import uuid
from typing import Any

from app.schemas.data_schema import DatasetType
from app.schemas.training_schema import (
    TrainingRequest,
    TrainingResponse,
    TrainingMetrics,
)

from app.ml.profiling import (
    get_top_terms_by_cluster,
    build_text_segment_names,
    build_numeric_segment_names,
)

from app.ml.preprocessing import preprocess_tabular_dataset
from app.ml.text_processing import vectorize_text_dataset
from app.ml.clustering import train_clustering_model, get_label_distribution
from app.ml.pca import reduce_to_2d, build_pca_points
from app.ml.evaluation import compute_clustering_metrics, interpret_metrics

from app.services.data_service import load_dataset_dataframe
from app.services.model_store_service import save_model_artifact


def enum_value(value: Any) -> Any:
    """
    Convierte un Enum a su value.
    Si no es Enum, devuelve el valor original.
    """

    return value.value if hasattr(value, "value") else value


def train_model(request: TrainingRequest) -> TrainingResponse:
    """
    Entrena un modelo de clustering.

    Flujo:
    1. Carga CSV
    2. Preprocesa según tipo de dataset
    3. Entrena clustering
    4. Reduce a 2D con PCA/SVD
    5. Calcula métricas internas
    6. Genera nombres de segmentos
    7. Guarda artifact, metadata y resultados
    8. Devuelve respuesta para API
    """

    dataset_type = request.dataset_type
    dataset_type_value = enum_value(dataset_type)

    algorithm_value = enum_value(request.algorithm)

    df = load_dataset_dataframe(
        dataset_type=dataset_type,
        filename=request.filename,
        prefer_clean=True,
    )

    if dataset_type == DatasetType.FREELANCERS:
        preprocess_result = preprocess_tabular_dataset(df)

        X = preprocess_result.X
        ids = preprocess_result.ids
        clean_df = preprocess_result.clean_df

        processor = preprocess_result.preprocessor
        vectorizer = None
        text_column = None

        numeric_columns = preprocess_result.numeric_columns
        categorical_columns = preprocess_result.categorical_columns
        feature_names = preprocess_result.feature_names

    elif dataset_type == DatasetType.REVIEWS:
        vectorizer_type = enum_value(request.vectorizer)

        preprocess_result = vectorize_text_dataset(
            df=df,
            text_column=request.text_column,
            vectorizer_type=vectorizer_type,
            max_features=1000,
        )

        X = preprocess_result.X
        ids = preprocess_result.ids
        clean_df = preprocess_result.clean_df

        processor = None
        vectorizer = preprocess_result.vectorizer
        text_column = preprocess_result.text_column

        numeric_columns = []
        categorical_columns = []
        feature_names = preprocess_result.feature_names

    else:
        raise ValueError("Tipo de dataset no soportado.")

    clustering_result = train_clustering_model(
        X=X,
        algorithm=algorithm_value,
        n_clusters=request.n_clusters or 3,
        eps=request.eps or 0.5,
        min_samples=request.min_samples or 5,
        linkage=getattr(request, "linkage", "ward") or "ward",
        random_state=request.random_state,
        knn_neighbors=3,
    )

    reduction_result = reduce_to_2d(
        X=X,
        random_state=request.random_state,
    )

    metrics_dict = compute_clustering_metrics(
        X=X,
        labels=clustering_result.labels,
    )

    interpretation = interpret_metrics(metrics_dict)

    top_terms = {}
    segment_names = {}

    if dataset_type == DatasetType.REVIEWS:
        top_terms = get_top_terms_by_cluster(
            X_text=X,
            feature_names=feature_names,
            labels=clustering_result.labels,
            n_terms=8,
        )

        segment_names = build_text_segment_names(
            top_terms_by_cluster=top_terms,
            n_terms=2,
        )

    elif dataset_type == DatasetType.FREELANCERS:
        segment_names = build_numeric_segment_names(
            df=clean_df,
            numeric_columns=numeric_columns,
            labels=clustering_result.labels,
            n_terms=2,
        )

    pca_points = build_pca_points(
        coordinates=reduction_result.coordinates,
        labels=clustering_result.labels,
        ids=ids,
    )

    results_df = clean_df.copy()

    results_df["cluster"] = clustering_result.labels

    results_df["cluster_name"] = [
        segment_names.get(
            int(label),
            segment_names.get(str(int(label)), f"Segmento {label}"),
        )
        for label in clustering_result.labels
    ]

    results_df["pc1"] = reduction_result.coordinates[:, 0]
    results_df["pc2"] = reduction_result.coordinates[:, 1]

    model_id = str(uuid.uuid4())

    label_distribution = get_label_distribution(clustering_result.labels)

    metadata = {
        "model_id": model_id,
        "dataset_type": dataset_type_value,
        "filename": request.filename,
        "algorithm": algorithm_value,
        "total_records": int(X.shape[0]),
        "total_features": int(X.shape[1]),
        "clusters_found": int(clustering_result.clusters_found),
        "noise_points": int(clustering_result.noise_points),
        "metrics": metrics_dict,
        "interpretation": interpretation,
        "pca_explained_variance": reduction_result.explained_variance_ratio,
        "pca_total_explained_variance": reduction_result.total_explained_variance,
        "reduction_method": reduction_result.method,
        "label_distribution": label_distribution,
        "top_terms": top_terms,
        "segment_names": segment_names,
        "text_column": text_column,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "feature_names": feature_names,
    }

    artifact = {
        "model_id": model_id,
        "dataset_type": dataset_type_value,
        "filename": request.filename,
        "algorithm": algorithm_value,
        "model": clustering_result.model,
        "assignment_model": clustering_result.assignment_model,
        "processor": processor,
        "vectorizer": vectorizer,
        "text_column": text_column,
        "numeric_columns": numeric_columns,
        "categorical_columns": categorical_columns,
        "feature_names": feature_names,
        "labels": clustering_result.labels,
        "ids": ids,
        "X_train": X,
        "reducer": reduction_result.reducer,
        "pca_points": pca_points,
        "metrics": metrics_dict,
        "interpretation": interpretation,
        "label_distribution": label_distribution,
        "top_terms": top_terms,
        "segment_names": segment_names,
    }

    save_model_artifact(
        model_id=model_id,
        artifact=artifact,
        metadata=metadata,
        results_df=results_df,
    )

    return TrainingResponse(
        message="Modelo entrenado correctamente.",
        model_id=model_id,
        dataset_type=dataset_type,
        filename=request.filename,
        algorithm=request.algorithm,
        total_records=int(X.shape[0]),
        total_features=int(X.shape[1]),
        clusters_found=int(clustering_result.clusters_found),
        noise_points=int(clustering_result.noise_points),
        metrics=TrainingMetrics(**metrics_dict),
        pca_explained_variance=reduction_result.explained_variance_ratio,
    )