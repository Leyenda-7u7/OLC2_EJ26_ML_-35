"""
Prueba rápida del motor CreditGuard con datos sintéticos.

Ejecutar desde la carpeta backend:

    python probar_motor.py
"""

import csv
import random
from pathlib import Path

from app.ml.constants import COLUMNAS_NUMERICAS, COLUMNA_OBJETIVO
from app.ml.engine import CreditGuardEngine


def generar_csv_sintetico(ruta_csv, n=300):
    """
    Genera un CSV sintético para probar el motor.
    """
    random.seed(99)

    ruta_csv.parent.mkdir(parents=True, exist_ok=True)

    columnas = COLUMNAS_NUMERICAS + [COLUMNA_OBJETIVO]

    with ruta_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()

        for _ in range(n):
            ingresos = random.uniform(2000, 50000)
            deuda = random.uniform(0, 100000)
            historial = random.uniform(0, 100)
            antiguedad = random.uniform(0, 30)
            creditos = random.randint(0, 10)
            monto = random.uniform(1000, 200000)
            atrasos = random.randint(0, 12)
            dependientes = random.randint(0, 6)
            utilizacion = random.uniform(0, 100)

            riesgo = int(
                deuda > ingresos * 6
                or historial < 40
                or atrasos > 3
            )

            writer.writerow({
                "ingresos_mensuales": ingresos,
                "deuda_activa": deuda,
                "historial_pagos": historial,
                "antiguedad_laboral": antiguedad,
                "creditos_activos": creditos,
                "monto_solicitado": monto,
                "atrasos_previos": atrasos,
                "dependientes_economicos": dependientes,
                "utilizacion_credito": utilizacion,
                "riesgo_incumplimiento": riesgo,
            })


def main():
    ruta_csv = Path("storage/uploads/datos_sinteticos_creditguard.csv")

    generar_csv_sintetico(ruta_csv)

    engine = CreditGuardEngine()

    print("[1] Cargando y limpiando CSV...")
    respuesta_limpieza = engine.cargar_y_limpiar(ruta_csv=str(ruta_csv))
    print(respuesta_limpieza)

    print("\n[2] Entrenando modelo...")
    respuesta_entrenamiento = engine.entrenar(
        n_arboles=80,
        max_depth=10,
        max_leaves=50,
    )
    print(respuesta_entrenamiento)

    print("\n[3] Estado del motor...")
    print(engine.obtener_estado())

    print("\n[4] Predicción individual...")
    resultado = engine.predecir_solicitante({
        "ingresos_mensuales": 8000,
        "deuda_activa": 80000,
        "historial_pagos": 30,
        "antiguedad_laboral": 1,
        "creditos_activos": 5,
        "monto_solicitado": 50000,
        "atrasos_previos": 5,
        "dependientes_economicos": 3,
        "utilizacion_credito": 90,
    })

    print(resultado)


if __name__ == "__main__":
    main()