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


### Instalación y ejecución

### 1. Backend 

#### Ingresar a la carpeta del backend
cd backend

#### Crear entorno virtual
python -m venv venv

#### Activar entorno virtual (Windows)
venv\Scripts\activate

#### Instalar dependencias
pip install fastapi uvicorn python-multipart

#### Ejecutar el servidor
python -m uvicorn app.main:app --reload

### 2. Frontend

#### Abrir una nueva terminal e ingresar a la carpeta del frontend
cd frontend

#### Instalar dependencias
npm install

#### Ejecutar la aplicación
npm run dev



