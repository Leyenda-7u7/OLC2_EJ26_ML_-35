from typing import Any

from pydantic import BaseModel

from app.schemas.data_schema import DatasetType


class ClassificationRequest(BaseModel):
    model_id: str
    dataset_type: DatasetType
    values: dict[str, Any]


class ClassificationResponse(BaseModel):
    model_id: str
    dataset_type: DatasetType
    cluster: int
    segment_name: str | None = None
    description: str | None = None