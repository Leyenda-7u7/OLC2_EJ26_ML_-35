from typing import Any

from pydantic import BaseModel

from app.schemas.data_schema import DatasetType


class PCAPoint(BaseModel):
    id: int | str | None = None
    pc1: float
    pc2: float
    cluster: int


class PCAResponse(BaseModel):
    model_id: str
    dataset_type: DatasetType
    points: list[PCAPoint]
    explained_variance_ratio: list[float]
    total_explained_variance: float


class ClusterProfile(BaseModel):
    cluster: int
    count: int
    summary: dict[str, Any]


class ClusterProfileResponse(BaseModel):
    model_id: str
    dataset_type: DatasetType
    profiles: list[ClusterProfile]


class CrossSegmentItem(BaseModel):
    freelancer_id: int | str
    freelancer_cluster: int | None = None
    review_cluster: int | None = None


class CrossSegmentResponse(BaseModel):
    items: list[CrossSegmentItem]