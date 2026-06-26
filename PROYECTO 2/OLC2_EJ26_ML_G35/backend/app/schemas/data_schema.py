from enum import Enum
from typing import Any

from pydantic import BaseModel


class DatasetType(str, Enum):
    FREELANCERS = "freelancers"
    REVIEWS = "reviews"


class DatasetUploadResponse(BaseModel):
    message: str
    dataset_type: DatasetType
    filename: str
    total_rows: int
    total_columns: int
    columns: list[str]
    preview: list[dict[str, Any]]


class DatasetCleanResponse(BaseModel):
    message: str
    dataset_type: DatasetType
    original_filename: str
    clean_filename: str
    total_rows: int
    total_columns: int
    removed_duplicates: int
    missing_values_filled: dict[str, int]
    columns: list[str]


class DatasetPreviewResponse(BaseModel):
    dataset_type: DatasetType
    filename: str
    total_rows: int
    total_columns: int
    columns: list[str]
    preview: list[dict[str, Any]]