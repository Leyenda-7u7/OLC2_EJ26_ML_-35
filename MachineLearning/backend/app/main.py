"""
Punto de entrada de la API CreditGuard.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import csv_router
from app.routers import model_router
from app.routers import prediction_router


app = FastAPI(
    title="CreditGuard API",
    description="Backend para predicción de riesgo crediticio usando Random Forest propio.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción se recomienda restringir esto.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    csv_router.router,
    prefix="/csv",
    tags=["CSV"],
)

app.include_router(
    model_router.router,
    prefix="/modelo",
    tags=["Modelo"],
)

app.include_router(
    prediction_router.router,
    prefix="/predicciones",
    tags=["Predicciones"],
)


@app.get("/")
def root():
    return {
        "mensaje": "CreditGuard API funcionando correctamente"
    }