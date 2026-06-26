from fastapi import APIRouter, HTTPException, Query

from app.schemas.analysis_schema import (
    PCAResponse,
    ClusterProfileResponse,
    CrossSegmentResponse,
)

from app.services.analysis_service import (
    get_pca_analysis,
    get_cluster_profiles,
    cross_segment_models,
)

from app.services.analysis_service import (
    get_pca_analysis,
    get_cluster_profiles,
    cross_segment_models,
    get_cross_segment_table,
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.get(
    "/pca/{model_id}",
    response_model=PCAResponse
)
def get_pca_points(
    model_id: str
):
    """
    Devuelve los puntos reducidos a 2 dimensiones usando PCA o SVD.

    Esto sirve para graficar los clusters en el frontend.
    """

    try:
        return get_pca_analysis(model_id)

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
            detail=f"Error al obtener análisis PCA: {str(error)}"
        )


@router.get(
    "/profiles/{model_id}",
    response_model=ClusterProfileResponse
)
def get_profiles(
    model_id: str
):
    """
    Devuelve el perfil de cada cluster.

    Incluye:
    - cantidad de registros
    - resumen numérico
    - resumen categórico
    """

    try:
        return get_cluster_profiles(model_id)

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
            detail=f"Error al obtener perfiles: {str(error)}"
        )


@router.get(
    "/cross-segments",
    response_model=CrossSegmentResponse
)
def cross_segments(
    freelancer_model_id: str = Query(...),
    reviews_model_id: str = Query(...)
):
    """
    Cruza los clusters de freelancers y reseñas usando freelancer_id.

    Requiere:
    - un modelo entrenado con freelancers
    - un modelo entrenado con reviews
    """

    try:
        return cross_segment_models(
            freelancer_model_id=freelancer_model_id,
            reviews_model_id=reviews_model_id,
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
            detail=f"Error al cruzar segmentos: {str(error)}"
        )
    

@router.get("/cross-table")
def cross_segment_table(
    freelancer_model_id: str,
    reviews_model_id: str
):
    """
    Genera tabla cruzada entre clusters de freelancers y clusters de reseñas.
    """

    try:
        return get_cross_segment_table(
            freelancer_model_id=freelancer_model_id,
            reviews_model_id=reviews_model_id,
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
            detail=f"Error al generar tabla cruzada: {str(error)}"
        )