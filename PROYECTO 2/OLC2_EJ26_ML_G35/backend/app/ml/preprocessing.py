from dataclasses import dataclass
from typing import Any

import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ID_COLUMNS = {
    "id",
    "freelancer_id",
    "review_id",
    "client_id",
    "cliente_id",
}

TEXT_COLUMNS = {
    "review",
    "review_text",
    "comentario",
    "comentarios",
    "reseña",
    "resena",
    "texto",
    "descripcion",
    "description",
}


@dataclass
class TabularPreprocessResult:
    X: Any
    preprocessor: ColumnTransformer
    feature_names: list[str]
    ids: list[Any] | None
    clean_df: pd.DataFrame
    numeric_columns: list[str]
    categorical_columns: list[str]


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas:
    - quita espacios
    - pasa a minúsculas
    - reemplaza espacios por guion bajo
    """

    df = df.copy()
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]
    return df


def clean_basic_dataframe(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """
    Limpieza básica:
    - normaliza columnas
    - elimina filas completamente vacías
    - elimina duplicados
    - limpia espacios en textos
    """

    df = normalize_column_names(df)

    before_duplicates = len(df)

    df = df.dropna(how="all")
    df = df.drop_duplicates()

    removed_duplicates = before_duplicates - len(df)

    for column in df.select_dtypes(include=["object"]).columns:
        df[column] = df[column].astype(str).str.strip()
        df[column] = df[column].replace({"nan": None, "None": None, "": None})

    return df, removed_duplicates


def get_id_values(df: pd.DataFrame) -> list[Any] | None:
    """
    Devuelve una lista de IDs si el dataset tiene una columna tipo id.
    """

    for column in df.columns:
        if column.lower() in ID_COLUMNS:
            return df[column].tolist()

    return None


def detect_tabular_columns(
    df: pd.DataFrame,
    target_exclusions: list[str] | None = None
) -> tuple[list[str], list[str]]:
    """
    Detecta columnas numéricas y categóricas útiles para clustering.

    Excluye:
    - columnas tipo ID
    - columnas de texto largo/reseñas
    - columnas indicadas manualmente
    """

    exclusions = set(ID_COLUMNS) | set(TEXT_COLUMNS)

    if target_exclusions:
        exclusions.update([col.lower() for col in target_exclusions])

    candidate_df = df[
        [column for column in df.columns if column.lower() not in exclusions]
    ]

    numeric_columns = candidate_df.select_dtypes(include=["number"]).columns.tolist()

    categorical_columns = candidate_df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    return numeric_columns, categorical_columns


def create_one_hot_encoder() -> OneHotEncoder:
    """
    Crea un OneHotEncoder compatible con versiones recientes y anteriores
    de scikit-learn.
    """

    try:
        return OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    except TypeError:
        return OneHotEncoder(handle_unknown="ignore", sparse=False)


def build_tabular_preprocessor(
    numeric_columns: list[str],
    categorical_columns: list[str]
) -> ColumnTransformer:
    """
    Construye el preprocesador para datos tabulares.

    Numéricos:
    - rellena faltantes con mediana
    - escala con StandardScaler

    Categóricos:
    - rellena faltantes con "desconocido"
    - convierte a OneHotEncoder
    """

    transformers = []

    if numeric_columns:
        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        transformers.append(
            ("numeric", numeric_pipeline, numeric_columns)
        )

    if categorical_columns:
        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="constant", fill_value="desconocido")),
                ("encoder", create_one_hot_encoder()),
            ]
        )

        transformers.append(
            ("categorical", categorical_pipeline, categorical_columns)
        )

    if not transformers:
        raise ValueError("No se encontraron columnas útiles para entrenar el modelo.")

    return ColumnTransformer(transformers=transformers)


def preprocess_tabular_dataset(
    df: pd.DataFrame,
    target_exclusions: list[str] | None = None
) -> TabularPreprocessResult:
    """
    Preprocesa un dataset tabular completo.

    Este flujo se usará para freelancers.csv.

    Retorna:
    - X transformado
    - preprocessor entrenado
    - nombres de columnas finales
    - ids si existen
    - dataframe limpio
    """

    clean_df, _ = clean_basic_dataframe(df)

    ids = get_id_values(clean_df)

    numeric_columns, categorical_columns = detect_tabular_columns(
        clean_df,
        target_exclusions=target_exclusions
    )

    preprocessor = build_tabular_preprocessor(
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns
    )

    X = preprocessor.fit_transform(clean_df)

    try:
        feature_names = preprocessor.get_feature_names_out().tolist()
    except Exception:
        feature_names = numeric_columns + categorical_columns

    return TabularPreprocessResult(
        X=X,
        preprocessor=preprocessor,
        feature_names=feature_names,
        ids=ids,
        clean_df=clean_df,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
    )


def transform_tabular_record(
    values: dict[str, Any],
    preprocessor: ColumnTransformer
):
    """
    Transforma un nuevo registro usando el preprocessor entrenado.

    Se usará al clasificar un freelancer nuevo.
    """

    record_df = pd.DataFrame([values])
    record_df = normalize_column_names(record_df)

    return preprocessor.transform(record_df)