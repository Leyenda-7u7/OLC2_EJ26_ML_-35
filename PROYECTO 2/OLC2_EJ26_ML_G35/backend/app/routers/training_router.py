from fastapi import APIRouter, HTTPException

from app.schemas.training_schema import (
    TrainingRequest,
    TrainingResponse,
)

from app.services.training_service import train_model


router = APIRouter(
    prefix="/training",
    tags=["Training"]
)


@router.post(
    "/train",
    response_model=TrainingResponse
)
def train_clustering_model(
    request: TrainingRequest
):
    """
    Entrena un modelo de clustering.

    Soporta:
    - KMeans
    - DBSCAN
    - Agglomerative
    - GMM

    Para freelancers:
    - usa preprocesamiento tabular

    Para reviews:
    - usa vectorización de texto
    """

    try:
        return train_model(request)

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al entrenar modelo: {str(error)}"
        )