from dataclasses import dataclass
from typing import Any
import re
import unicodedata

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

STOPWORDS_ES = [
    "el", "la", "los", "las", "de", "del", "y", "en", "es",
    "un", "una", "unos", "unas", "que", "se", "con", "por",
    "para", "muy", "mas", "más", "su", "sus", "lo", "al",
    "tiene", "tienen", "hay", "ha", "han", "esta", "este",
    "estas", "estos", "como", "pero", "tambien", "también",
    "son", "ser", "fue", "le", "les", "o", "u", "e", "ni",
    "sin", "sobre", "ya", "cada", "entre", "hacia", "desde",
]

TEXT_COLUMN_CANDIDATES = [
    "review_text",
    "review",
    "reseña",
    "resena",
    "comentario",
    "comentarios",
    "texto",
    "description",
    "descripcion",
]

ID_COLUMN_CANDIDATES = [
    "freelancer_id",
    "id",
    "review_id",
]


@dataclass
class TextVectorizationResult:
    X: Any
    vectorizer: TfidfVectorizer | CountVectorizer
    ids: list[Any] | None
    clean_df: pd.DataFrame
    text_column: str
    feature_names: list[str]


def normalize_text(text: Any) -> str:
    """
    Limpia texto:
    - convierte a string
    - pasa a minúsculas
    - quita URLs
    - quita caracteres raros
    - normaliza espacios
    """

    if text is None:
        return ""

    text = str(text).lower().strip()

    text = unicodedata.normalize("NFKD", text)
    text = "".join(
        char for char in text
        if not unicodedata.combining(char)
    )

    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"[^a-zA-ZáéíóúñüÁÉÍÓÚÑÜ0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def normalize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza nombres de columnas.
    """

    df = df.copy()
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]
    return df


def detect_text_column(
    df: pd.DataFrame,
    text_column: str | None = None
) -> str:
    """
    Detecta la columna de texto.

    Si el usuario manda text_column, se usa esa.
    Si no, busca nombres comunes como review_text, reseña, comentario, etc.
    """

    df = normalize_column_names(df)

    if text_column:
        text_column = text_column.strip().lower().replace(" ", "_")

        if text_column not in df.columns:
            raise ValueError(f"La columna de texto '{text_column}' no existe.")

        return text_column

    for candidate in TEXT_COLUMN_CANDIDATES:
        if candidate in df.columns:
            return candidate

    object_columns = df.select_dtypes(include=["object"]).columns.tolist()

    if not object_columns:
        raise ValueError("No se encontró ninguna columna de texto para vectorizar.")

    return object_columns[0]


def get_id_values(df: pd.DataFrame) -> list[Any] | None:
    """
    Devuelve IDs si existe freelancer_id, id o review_id.
    """

    for column in ID_COLUMN_CANDIDATES:
        if column in df.columns:
            return df[column].tolist()

    return None


def build_vectorizer(
    vectorizer_type: str = "tfidf",
    max_features: int = 1000
) -> TfidfVectorizer | CountVectorizer:
    """
    Crea el vectorizador de texto.

    vectorizer_type:
    - "tfidf"
    - "bow"
    """

    vectorizer_type = str(vectorizer_type).lower().strip()

    if vectorizer_type == "tfidf":
        return TfidfVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=1,
            stop_words=STOPWORDS_ES
        )

    if vectorizer_type == "bow":
        return CountVectorizer(
            max_features=max_features,
            ngram_range=(1, 2),
            min_df=1,
            stop_words=STOPWORDS_ES
        )

    raise ValueError("Vectorizer no soportado. Usa 'tfidf' o 'bow'.")


def vectorize_text_dataset(
    df: pd.DataFrame,
    text_column: str | None = None,
    vectorizer_type: str = "tfidf",
    max_features: int = 1000
) -> TextVectorizationResult:
    """
    Limpia y vectoriza un dataset de reseñas.

    Este flujo se usará para reseñas_clientes.csv.
    """

    clean_df = normalize_column_names(df)
    clean_df = clean_df.dropna(how="all").drop_duplicates()

    selected_text_column = detect_text_column(
        clean_df,
        text_column=text_column
    )

    clean_df[selected_text_column] = clean_df[selected_text_column].apply(
        normalize_text
    )

    if clean_df[selected_text_column].str.strip().eq("").all():
        raise ValueError(
            "La columna de texto está vacía después de la limpieza. "
            "No se puede vectorizar."
        )

    ids = get_id_values(clean_df)

    vectorizer = build_vectorizer(
        vectorizer_type=vectorizer_type,
        max_features=max_features
    )

    X = vectorizer.fit_transform(clean_df[selected_text_column])

    feature_names = vectorizer.get_feature_names_out().tolist()

    return TextVectorizationResult(
        X=X,
        vectorizer=vectorizer,
        ids=ids,
        clean_df=clean_df,
        text_column=selected_text_column,
        feature_names=feature_names,
    )


def transform_text_record(
    values: dict[str, Any],
    text_column: str,
    vectorizer: TfidfVectorizer | CountVectorizer
):
    """
    Transforma una nueva reseña usando el vectorizer entrenado.
    """

    normalized_values = {
        str(key).strip().lower().replace(" ", "_"): value
        for key, value in values.items()
    }

    text_column = text_column.strip().lower().replace(" ", "_")

    if text_column not in normalized_values:
        raise ValueError(
            f"Debe enviar el campo '{text_column}' para clasificar la reseña."
        )

    clean_text = normalize_text(normalized_values[text_column])

    if clean_text.strip() == "":
        raise ValueError("El texto enviado está vacío después de la limpieza.")

    return vectorizer.transform([clean_text])