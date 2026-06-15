"""
Router para carga y limpieza de archivos CSV.
"""

from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.creditguard_service import creditguard_engine
from app.utils.file_utils import guardar_csv_original, guardar_datos_limpios_csv


router = APIRouter()


@router.post("/cargar")
async def cargar_csv(file: UploadFile = File(...)):
    """
    Carga un archivo CSV, guarda el original, limpia los datos
    y guarda los datos limpios en storage/cleaned.
    """
    try:
        if not file.filename.lower().endswith(".csv"):
            raise HTTPException(
                status_code=400,
                detail="El archivo debe tener extensión .csv",
            )

        contenido = await file.read()

        ruta_original = guardar_csv_original(
            nombre_archivo=file.filename,
            contenido=contenido,
        )

        respuesta = creditguard_engine.cargar_y_limpiar(
            contenido_csv=contenido,
        )

        ruta_limpios = guardar_datos_limpios_csv(
            creditguard_engine.datos_limpios,
        )

        creditguard_engine.registrar_rutas_archivos(
            ruta_csv_original=ruta_original,
            ruta_datos_limpios=ruta_limpios,
        )

        respuesta["archivos"] = {
            "csv_original": ruta_original,
            "datos_limpios": ruta_limpios,
        }

        return respuesta

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )