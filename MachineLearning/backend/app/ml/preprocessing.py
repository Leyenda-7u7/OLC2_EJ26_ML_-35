"""
Funciones de carga, limpieza, normalización y preparación de datos.
"""

import csv
import io
import random

from app.ml.constants import (
    COLUMNAS_NUMERICAS,
    COLUMNA_OBJETIVO,
    COLUMNAS_REQUERIDAS,
)


def validar_columnas_csv(columnas_csv):
    """
    Valida que el CSV tenga todas las columnas requeridas.
    """
    if columnas_csv is None:
        raise ValueError("El archivo CSV no tiene encabezados.")

    columnas_csv = [col.strip() for col in columnas_csv]
    faltantes = [col for col in COLUMNAS_REQUERIDAS if col not in columnas_csv]

    if faltantes:
        raise ValueError(
            "El CSV no contiene todas las columnas requeridas. "
            f"Columnas faltantes: {faltantes}"
        )


def cargar_csv(ruta_archivo=None, contenido_csv=None):
    """
    Carga un CSV desde una ruta local o desde contenido en memoria.

    Parámetros:
        ruta_archivo: ruta física del archivo CSV.
        contenido_csv: contenido CSV como str o bytes.

    Retorna:
        Lista de diccionarios.
    """
    if ruta_archivo is None and contenido_csv is None:
        raise ValueError("Debes proporcionar una ruta de archivo o contenido CSV.")

    datos = []

    if contenido_csv is not None:
        if isinstance(contenido_csv, bytes):
            contenido_csv = contenido_csv.decode("utf-8-sig")

        archivo = io.StringIO(contenido_csv)
        lector = csv.DictReader(archivo)

        validar_columnas_csv(lector.fieldnames)

        for fila in lector:
            datos.append(dict(fila))

        archivo.close()
        return datos

    with open(ruta_archivo, newline="", encoding="utf-8-sig") as f:
        lector = csv.DictReader(f)

        validar_columnas_csv(lector.fieldnames)

        for fila in lector:
            datos.append(dict(fila))

    return datos


def limpiar_datos(datos):
    """
    Limpia y valida el dataset.

    Maneja:
    - valores faltantes
    - tipos inválidos
    - rangos incorrectos
    - montos negativos
    - objetivo inválido

    Retorna:
        datos_limpios, reporte_limpieza
    """
    datos_limpios = []

    reporte = {
        "total_original": len(datos),
        "filas_eliminadas": 0,
        "valores_imputados": 0,
        "errores_por_columna": {},
    }

    medianas = _calcular_medianas(datos)

    for fila in datos:
        fila_limpia = {}
        fila_valida = True

        for col in COLUMNAS_NUMERICAS:
            valor_raw = fila.get(col, None)

            if valor_raw is None or str(valor_raw).strip() == "":
                fila_limpia[col] = medianas.get(col, 0.0)
                reporte["valores_imputados"] += 1
                _registrar_error(reporte, col, "valor_faltante")
                continue

            try:
                valor = float(str(valor_raw).strip())
            except ValueError:
                fila_limpia[col] = medianas.get(col, 0.0)
                reporte["valores_imputados"] += 1
                _registrar_error(reporte, col, "tipo_invalido")
                continue

            if col == "historial_pagos" and not (0 <= valor <= 100):
                _registrar_error(reporte, col, "fuera_de_rango")
                valor = max(0, min(100, valor))

            elif col == "utilizacion_credito" and not (0 <= valor <= 100):
                _registrar_error(reporte, col, "fuera_de_rango")
                valor = max(0, min(100, valor))

            elif col in ("ingresos_mensuales", "deuda_activa", "monto_solicitado") and valor < 0:
                _registrar_error(reporte, col, "valor_negativo")
                fila_valida = False
                break

            elif col in ("ingresos_mensuales", "monto_solicitado") and valor == 0:
                _registrar_error(reporte, col, "valor_cero")
                fila_valida = False
                break

            elif col in ("creditos_activos", "atrasos_previos", "dependientes_economicos") and valor < 0:
                _registrar_error(reporte, col, "valor_negativo_corregido")
                valor = 0

            fila_limpia[col] = valor

        if not fila_valida:
            reporte["filas_eliminadas"] += 1
            continue

        objetivo_raw = fila.get(COLUMNA_OBJETIVO, None)

        if objetivo_raw is None or str(objetivo_raw).strip() == "":
            reporte["filas_eliminadas"] += 1
            _registrar_error(reporte, COLUMNA_OBJETIVO, "valor_faltante")
            continue

        try:
            objetivo = int(float(str(objetivo_raw).strip()))
            if objetivo not in (0, 1):
                raise ValueError
        except ValueError:
            reporte["filas_eliminadas"] += 1
            _registrar_error(reporte, COLUMNA_OBJETIVO, "tipo_o_valor_invalido")
            continue

        fila_limpia[COLUMNA_OBJETIVO] = objetivo
        datos_limpios.append(fila_limpia)

    reporte["total_limpio"] = len(datos_limpios)

    return datos_limpios, reporte


def _calcular_medianas(datos):
    """
    Calcula la mediana de cada columna numérica ignorando valores inválidos.
    """
    medianas = {}

    for col in COLUMNAS_NUMERICAS:
        valores = []

        for fila in datos:
            v = fila.get(col, None)

            if v is not None and str(v).strip() != "":
                try:
                    valores.append(float(str(v).strip()))
                except ValueError:
                    pass

        if valores:
            valores.sort()
            n = len(valores)

            if n % 2 == 1:
                medianas[col] = valores[n // 2]
            else:
                medianas[col] = (valores[n // 2 - 1] + valores[n // 2]) / 2
        else:
            medianas[col] = 0.0

    return medianas


def _registrar_error(reporte, col, tipo):
    """
    Registra un error o corrección dentro del reporte de limpieza.
    """
    if col not in reporte["errores_por_columna"]:
        reporte["errores_por_columna"][col] = {}

    reporte["errores_por_columna"][col][tipo] = (
        reporte["errores_por_columna"][col].get(tipo, 0) + 1
    )


def normalizar_datos(datos):
    """
    Normaliza las columnas numéricas usando Min-Max.

    Retorna:
        datos_normalizados, parametros_normalizacion
    """
    params = {}

    for col in COLUMNAS_NUMERICAS:
        valores = [fila[col] for fila in datos]
        minv = min(valores)
        maxv = max(valores)

        params[col] = {
            "min": minv,
            "max": maxv,
        }

    datos_norm = []

    for fila in datos:
        fila_norm = {}

        for col in COLUMNAS_NUMERICAS:
            minv = params[col]["min"]
            maxv = params[col]["max"]

            if maxv == minv:
                fila_norm[col] = 0.0
            else:
                fila_norm[col] = (fila[col] - minv) / (maxv - minv)

        fila_norm[COLUMNA_OBJETIVO] = fila[COLUMNA_OBJETIVO]
        datos_norm.append(fila_norm)

    return datos_norm, params


def normalizar_solicitante(solicitante, params):
    """
    Normaliza un solicitante usando los parámetros del entrenamiento.
    """
    resultado = {}

    for col in COLUMNAS_NUMERICAS:
        minv = params[col]["min"]
        maxv = params[col]["max"]

        if maxv == minv:
            resultado[col] = 0.0
        else:
            resultado[col] = (solicitante[col] - minv) / (maxv - minv)

    return resultado


def dividir_datos_estratificado(datos, proporcion_entrenamiento=0.8, semilla=42):
    """
    Divide los datos manteniendo la proporción de clases 0 y 1.
    """
    random.seed(semilla)

    clase_0 = [fila for fila in datos if fila[COLUMNA_OBJETIVO] == 0]
    clase_1 = [fila for fila in datos if fila[COLUMNA_OBJETIVO] == 1]

    random.shuffle(clase_0)
    random.shuffle(clase_1)

    corte_0 = int(len(clase_0) * proporcion_entrenamiento)
    corte_1 = int(len(clase_1) * proporcion_entrenamiento)

    entrenamiento = clase_0[:corte_0] + clase_1[:corte_1]
    prueba = clase_0[corte_0:] + clase_1[corte_1:]

    random.shuffle(entrenamiento)
    random.shuffle(prueba)

    return entrenamiento, prueba


def datos_a_matrices(datos):
    """
    Convierte una lista de diccionarios a X e y.
    """
    X = [[fila[col] for col in COLUMNAS_NUMERICAS] for fila in datos]
    y = [fila[COLUMNA_OBJETIVO] for fila in datos]

    return X, y