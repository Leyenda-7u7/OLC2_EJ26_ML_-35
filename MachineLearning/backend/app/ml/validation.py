"""
Validaciones de entrada para el motor CreditGuard.
"""

from app.ml.constants import COLUMNAS_NUMERICAS


def validar_hiperparametros(n_arboles, max_depth, max_leaves):
    """
    Valida hiperparámetros configurables desde la UI.
    """
    if n_arboles <= 0:
        raise ValueError("La cantidad de árboles debe ser mayor a 0.")

    if max_depth <= 0:
        raise ValueError("La profundidad máxima debe ser mayor a 0.")

    if max_leaves <= 1:
        raise ValueError("El número máximo de hojas debe ser mayor a 1.")


def validar_solicitante(datos_solicitante):
    """
    Valida y convierte a float los datos de un solicitante individual.
    """
    solicitante_limpio = {}

    for col in COLUMNAS_NUMERICAS:
        if col not in datos_solicitante:
            raise ValueError(f"Falta el campo requerido: {col}")

        try:
            valor = float(datos_solicitante[col])
        except (ValueError, TypeError):
            raise ValueError(f"El campo {col} debe ser numérico.")

        if col in ("ingresos_mensuales", "monto_solicitado") and valor <= 0:
            raise ValueError(f"El campo {col} debe ser mayor a 0.")

        if col in (
            "deuda_activa",
            "creditos_activos",
            "atrasos_previos",
            "dependientes_economicos",
            "antiguedad_laboral",
        ) and valor < 0:
            raise ValueError(f"El campo {col} no puede ser negativo.")

        if col in ("historial_pagos", "utilizacion_credito") and not (0 <= valor <= 100):
            raise ValueError(f"El campo {col} debe estar entre 0 y 100.")

        solicitante_limpio[col] = valor

    return solicitante_limpio