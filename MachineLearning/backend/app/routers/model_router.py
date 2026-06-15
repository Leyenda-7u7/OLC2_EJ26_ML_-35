"""
Router para entrenamiento, reentrenamiento, métricas y estado del modelo.
"""

from fastapi import APIRouter, HTTPException

from app.schemas.creditguard_schema import HyperparametrosSchema
from app.services.creditguard_service import creditguard_engine


router = APIRouter()


@router.get("/estado")
def obtener_estado():
    """
    Retorna el estado actual del motor.
    """
    try:
        return creditguard_engine.obtener_estado()

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/entrenar")
def entrenar_modelo(hiperparametros: HyperparametrosSchema):
    """
    Entrena el modelo con los datos limpios cargados previamente.
    """
    try:
        respuesta = creditguard_engine.entrenar(
            n_arboles=hiperparametros.n_arboles,
            max_depth=hiperparametros.max_depth,
            max_leaves=hiperparametros.max_leaves,
        )

        return respuesta

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/reentrenar")
def reentrenar_modelo(hiperparametros: HyperparametrosSchema):
    """
    Reentrena el modelo con nuevos hiperparámetros.
    """
    try:
        respuesta = creditguard_engine.reentrenar_con_hiperparametros(
            n_arboles=hiperparametros.n_arboles,
            max_depth=hiperparametros.max_depth,
            max_leaves=hiperparametros.max_leaves,
        )

        return respuesta

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/metricas")
def obtener_metricas():
    """
    Retorna las métricas actuales del modelo.
    """
    try:
        estado = creditguard_engine.obtener_estado()

        if not estado["modelo_entrenado"]:
            raise HTTPException(
                status_code=400,
                detail="El modelo aún no ha sido entrenado.",
            )

        return {
            "metricas": estado["metricas"]
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )