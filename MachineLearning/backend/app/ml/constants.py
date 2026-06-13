"""
Constantes principales del motor CreditGuard.
"""

COLUMNAS_NUMERICAS = [
    "ingresos_mensuales",
    "deuda_activa",
    "historial_pagos",
    "antiguedad_laboral",
    "creditos_activos",
    "monto_solicitado",
    "atrasos_previos",
    "dependientes_economicos",
    "utilizacion_credito",
]

COLUMNA_OBJETIVO = "riesgo_incumplimiento"  # 0 = sin riesgo, 1 = con riesgo

COLUMNAS_REQUERIDAS = COLUMNAS_NUMERICAS + [COLUMNA_OBJETIVO]