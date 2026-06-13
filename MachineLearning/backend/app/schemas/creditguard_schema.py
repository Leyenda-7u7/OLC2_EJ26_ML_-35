"""
Schemas Pydantic para validar datos de entrada y salida de CreditGuard.
"""

from pydantic import BaseModel, Field


class HyperparametrosSchema(BaseModel):
    """
    Hiperparámetros configurables del Random Forest.
    """

    n_arboles: int = Field(default=100, gt=0, description="Cantidad de árboles")
    max_depth: int = Field(default=10, gt=0, description="Profundidad máxima")
    max_leaves: int = Field(default=50, gt=1, description="Número máximo de hojas")


class SolicitanteSchema(BaseModel):
    """
    Datos de entrada para predecir el riesgo de un solicitante.
    """

    ingresos_mensuales: float = Field(..., gt=0)
    deuda_activa: float = Field(..., ge=0)
    historial_pagos: float = Field(..., ge=0, le=100)
    antiguedad_laboral: float = Field(..., ge=0)
    creditos_activos: float = Field(..., ge=0)
    monto_solicitado: float = Field(..., gt=0)
    atrasos_previos: float = Field(..., ge=0)
    dependientes_economicos: float = Field(..., ge=0)
    utilizacion_credito: float = Field(..., ge=0, le=100)