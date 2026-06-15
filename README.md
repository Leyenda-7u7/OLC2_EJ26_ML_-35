# CreditGuard - Sistema de Riesgo Crediticio

Sistema de evaluación de riesgo crediticio basado en Random Forest implementado desde cero. Incluye backend en FastAPI y frontend en Angular.

## Requisitos del sistema

| Requisito | Versión |
|-----------|---------|
| Python | 3.9 o superior |
| Node.js | 18.x o superior |
| Angular CLI | 15.x o superior |
| Windows | 10 / 11 (recomendado) |

## Estructura del proyecto


## Instalación y ejecución

### 1. Backend (FastAPI)

# Ingresar a la carpeta del backend
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install fastapi uvicorn python-multipart

# Ejecutar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

cd backend
python probar_motor.py


