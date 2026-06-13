"""
Utilidades para manejo de archivos del proyecto CreditGuard.
Guarda CSV original y datos limpios.
"""

import csv
from datetime import datetime
from pathlib import Path

from app.ml.constants import COLUMNAS_NUMERICAS, COLUMNA_OBJETIVO


BACKEND_DIR = Path(__file__).resolve().parents[2]

UPLOADS_DIR = BACKEND_DIR / "storage" / "uploads"
CLEANED_DIR = BACKEND_DIR / "storage" / "cleaned"


def asegurar_directorios():
    """
    Crea los directorios necesarios si no existen.
    """
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    CLEANED_DIR.mkdir(parents=True, exist_ok=True)


def generar_nombre_archivo(nombre_original):
    """
    Genera un nombre único para evitar sobrescribir archivos.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_limpio = Path(nombre_original).name.replace(" ", "_")

    return f"{timestamp}_{nombre_limpio}"


def guardar_csv_original(nombre_archivo, contenido):
    """
    Guarda el archivo CSV original en storage/uploads.
    """
    asegurar_directorios()

    nombre_final = generar_nombre_archivo(nombre_archivo)
    ruta_final = UPLOADS_DIR / nombre_final

    with ruta_final.open("wb") as f:
        f.write(contenido)

    return str(ruta_final)


def guardar_datos_limpios_csv(datos_limpios):
    """
    Guarda los datos limpios en storage/cleaned/datos_limpios.csv.
    """
    asegurar_directorios()

    ruta_final = CLEANED_DIR / "datos_limpios.csv"

    columnas = COLUMNAS_NUMERICAS + [COLUMNA_OBJETIVO]

    with ruta_final.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()

        for fila in datos_limpios:
            writer.writerow(fila)

    return str(ruta_final)