from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.schemas.data_schema import (
    DatasetType,
    DatasetUploadResponse,
    DatasetCleanResponse,
    DatasetPreviewResponse,
)

from app.services.data_service import (
    save_uploaded_dataset,
    clean_dataset,
    get_dataset_preview,
)


router = APIRouter(
    prefix="/data",
    tags=["Data"]
)


@router.post(
    "/upload",
    response_model=DatasetUploadResponse
)
async def upload_dataset(
    dataset_type: DatasetType = Query(...),
    file: UploadFile = File(...)
):
    """
    Carga un archivo CSV.

    dataset_type:
    - freelancers
    - reviews
    """

    try:
        file_content = await file.read()

        return save_uploaded_dataset(
            file_content=file_content,
            filename=file.filename,
            dataset_type=dataset_type,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al cargar dataset: {str(error)}"
        )


@router.post(
    "/clean",
    response_model=DatasetCleanResponse
)
def clean_uploaded_dataset(
    dataset_type: DatasetType = Query(...),
    filename: str = Query(...)
):
    """
    Limpia un dataset previamente cargado.

    Primero debes subir el archivo con /data/upload.
    """

    try:
        return clean_dataset(
            dataset_type=dataset_type,
            filename=filename,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al limpiar dataset: {str(error)}"
        )


@router.get(
    "/preview",
    response_model=DatasetPreviewResponse
)
def preview_dataset(
    dataset_type: DatasetType = Query(...),
    filename: str = Query(...),
    prefer_clean: bool = Query(default=True)
):
    """
    Devuelve una vista previa del dataset.

    Si prefer_clean=True, intenta leer primero la versión limpia.
    """

    try:
        return get_dataset_preview(
            dataset_type=dataset_type,
            filename=filename,
            prefer_clean=prefer_clean,
        )

    except FileNotFoundError as error:
        raise HTTPException(
            status_code=404,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener preview: {str(error)}"
        )