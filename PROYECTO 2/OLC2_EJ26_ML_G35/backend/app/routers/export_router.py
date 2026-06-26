from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.services.export_service import (
    export_clustered_csv,
    export_pdf_report,
)


router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


@router.get("/csv/{model_id}")
def download_csv_report(model_id: str):
    """
    Descarga el CSV con los resultados del modelo.

    Incluye:
    - columnas originales
    - cluster
    - pc1
    - pc2
    """

    try:
        csv_path = export_clustered_csv(model_id)

        return FileResponse(
            path=str(csv_path),
            media_type="text/csv",
            filename=csv_path.name,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al exportar CSV: {str(error)}",
        )


@router.get("/pdf/{model_id}")
def download_pdf_report(model_id: str):
    """
    Descarga el reporte PDF del modelo.

    Incluye:
    - información general
    - métricas
    - interpretación
    - visualización PCA/SVD
    - distribución de clusters
    - perfiles básicos por cluster
    """

    try:
        pdf_path = export_pdf_report(model_id)

        return FileResponse(
            path=str(pdf_path),
            media_type="application/pdf",
            filename=pdf_path.name,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al exportar PDF: {str(error)}",
        )