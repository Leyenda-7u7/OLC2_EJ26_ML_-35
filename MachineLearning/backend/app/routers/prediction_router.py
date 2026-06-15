"""
Router para predicciones individuales.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.creditguard_schema import SolicitanteSchema
from app.services.creditguard_service import creditguard_engine


router = APIRouter()


@router.post("/predecir")
def predecir_solicitante(solicitante: SolicitanteSchema):
    """
    Predice si un solicitante tiene riesgo de incumplimiento crediticio.
    """
    try:
        datos_solicitante = solicitante.model_dump()

        respuesta = creditguard_engine.predecir_solicitante(
            datos_solicitante
        )

        return respuesta

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )