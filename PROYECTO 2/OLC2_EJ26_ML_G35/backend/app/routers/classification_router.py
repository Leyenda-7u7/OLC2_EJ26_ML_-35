from fastapi import APIRouter, HTTPException

from app.schemas.classification_schema import (
    ClassificationRequest,
    ClassificationResponse,
)

from app.services.classification_service import classify_record


router = APIRouter(
    prefix="/classification",
    tags=["Classification"]
)


@router.post(
    "/predict",
    response_model=ClassificationResponse
)
def predict_cluster(
    request: ClassificationRequest
):
    """
    Clasifica un nuevo registro.

    Para freelancers:
    values puede ser algo como:
    {
        "hourly_rate": 25,
        "experience_years": 3,
        "rating": 4.7
    }

    Para reviews:
    values puede ser algo como:
    {
        "review_text": "Excelente trabajo y muy buena comunicación"
    }
    """

    try:
        return classify_record(request)

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
            detail=f"Error al clasificar registro: {str(error)}"
        )