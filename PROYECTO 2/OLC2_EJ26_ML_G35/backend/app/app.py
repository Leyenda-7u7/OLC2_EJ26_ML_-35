from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.data_router import router as data_router
from app.routers.training_router import router as training_router
from app.routers.analysis_router import router as analysis_router
from app.routers.classification_router import router as classification_router
from app.routers.export_router import router as export_router


app = FastAPI(
    title="TalentMosaic API",
    description="API para segmentación de freelancers y reseñas usando clustering.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "TalentMosaic API funcionando correctamente."
    }


app.include_router(data_router)
app.include_router(training_router)
app.include_router(analysis_router)
app.include_router(classification_router)
app.include_router(export_router)