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



# TalentMosaic - Proyecto 2

TalentMosaic es una aplicación web para segmentación inteligente de freelancers y reseñas de clientes mediante técnicas de Machine Learning no supervisado.

El sistema permite cargar archivos CSV, limpiar datos, entrenar modelos de clustering, interpretar segmentos, evaluar métricas internas, clasificar nuevos registros y exportar reportes.

---

## 1. Requisitos del sistema

Antes de ejecutar el proyecto, asegúrate de tener instalado:

### Backend

* Python 3.11 recomendado
* pip
* Entorno virtual de Python

### Frontend

* Node.js 20.19 o superior recomendado
* npm

### Tecnologías principales

Backend:

* FastAPI
* Uvicorn
* Pandas
* NumPy
* Scikit-learn
* SciPy
* Matplotlib
* ReportLab
* Joblib

Frontend:

* React
* Vite
* Axios
* React Router DOM
* Recharts
* Lucide React

---

## 2. Estructura general del proyecto

txt
Proyecto2/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── app.py
│       ├── config.py
│       ├── routers/
│       ├── services/
│       ├── schemas/
│       ├── ml/
│       └── storage/
│
└── frontend/
    ├── package.json
    ├── index.html
    └── src/
        ├── api/
        ├── components/
        ├── pages/
        ├── hooks/
        └── utils/


---

## 3. Instalación del backend

Desde la raíz del proyecto, entrar a la carpeta backend:

bash
cd backend


Crear entorno virtual:

### Windows PowerShell

bash
python -m venv .venv
.\.venv\Scripts\activate


### Linux / macOS

bash
python3 -m venv .venv
source .venv/bin/activate


Instalar dependencias:

bash
pip install -r requirements.txt


El archivo requirements.txt debe contener como mínimo:

txt
fastapi
uvicorn[standard]
python-multipart
pandas
numpy
scikit-learn
scipy
matplotlib
reportlab
joblib


---

## 4. Ejecución del backend

Desde la carpeta backend, ejecutar:

bash
python -m uvicorn app.app:app --reload


El backend quedará disponible en:

txt
http://127.0.0.1:8000


Documentación automática de la API:

txt
http://127.0.0.1:8000/docs


Respuesta esperada al abrir la raíz del backend:

json
{
  "message": "TalentMosaic API funcionando correctamente."
}


---

## 5. Instalación del frontend

Desde la raíz del proyecto, entrar a la carpeta frontend:

bash
cd frontend


Instalar dependencias:

bash
npm install


Instalar dependencias adicionales si no están instaladas:

bash
npm install axios react-router-dom recharts lucide-react


---

## 6. Ejecución del frontend

Desde la carpeta frontend, ejecutar:

bash
npm run dev


El frontend quedará disponible en:

txt
http://localhost:5173


Importante: evitar que la ruta del proyecto contenga caracteres especiales como #, porque Vite puede tener problemas para resolver archivos. Por ejemplo, usar:

txt
OLC2_EJ26_ML_G35


en lugar de:

txt
OLC2_EJ26_ML_#35


---

## 7. Flujo de uso del sistema

El sistema cuenta con las siguientes vistas principales:

1. Carga y preprocesamiento
2. Configuración y entrenamiento
3. Interpretación de los segmentos
4. Evaluación y validación
5. Clasificación de nuevo registro
6. Exportación de reportes

Flujo recomendado:

txt
1. Cargar CSV de freelancers.
2. Limpiar CSV de freelancers.
3. Cargar CSV de reseñas.
4. Limpiar CSV de reseñas.
5. Entrenar modelo de freelancers.
6. Entrenar modelo de reseñas.
7. Interpretar segmentos.
8. Revisar métricas de evaluación.
9. Clasificar nuevos registros.
10. Exportar reportes.


---

## 8. Formato de archivos CSV requeridos

El sistema trabaja con dos tipos de archivos CSV:

* Dataset de freelancers
* Dataset de reseñas de clientes

Los nombres de los archivos pueden variar, pero deben respetar las columnas requeridas.

---

## 8.1 CSV de freelancers

Archivo sugerido:

txt
freelancers_dev.csv


Columnas requeridas:

txt
freelancer_id
proyectos_completados
ingresos_totales
tarifa_hora_promedio
anios_experiencia
tiempo_respuesta_horas
tasa_finalizacion
calificacion_promedio
categoria_principal
clientes_recurrentes
horas_trabajadas_mes


Descripción de columnas:

| Columna                | Descripción                                     |
| ---------------------- | ----------------------------------------------- |
| freelancer_id          | Identificador único del freelancer.             |
| proyectos_completados  | Cantidad de proyectos completados.              |
| ingresos_totales       | Ingresos totales generados por el freelancer.   |
| tarifa_hora_promedio   | Tarifa promedio por hora.                       |
| anios_experiencia      | Años de experiencia del freelancer.             |
| tiempo_respuesta_horas | Tiempo promedio de respuesta en horas.          |
| tasa_finalizacion      | Porcentaje o tasa de finalización de proyectos. |
| calificacion_promedio  | Calificación promedio recibida.                 |
| categoria_principal    | Categoría principal del freelancer.             |
| clientes_recurrentes   | Cantidad de clientes recurrentes.               |
| horas_trabajadas_mes   | Horas trabajadas al mes.                        |

Ejemplo:

csv
freelancer_id,proyectos_completados,ingresos_totales,tarifa_hora_promedio,anios_experiencia,tiempo_respuesta_horas,tasa_finalizacion,calificacion_promedio,categoria_principal,clientes_recurrentes,horas_trabajadas_mes
1,60,50000,80,5,8,90,4.5,Desarrollo de Software,6,120


---

## 8.2 CSV de reseñas de clientes

Archivo sugerido:

txt
resenas_clientes_dev.csv


Columnas requeridas:

txt
reseña_id
freelancer_id
texto_reseña
fecha_reseña
categoria_servicio


Descripción de columnas:

| Columna            | Descripción                                        |
| ------------------ | -------------------------------------------------- |
| reseña_id          | Identificador único de la reseña.                  |
| freelancer_id      | Identificador del freelancer asociado a la reseña. |
| texto_reseña       | Texto de la reseña escrita por el cliente.         |
| fecha_reseña       | Fecha en la que se registró la reseña.             |
| categoria_servicio | Categoría del servicio evaluado.                   |

Ejemplo:

csv
reseña_id,freelancer_id,texto_reseña,fecha_reseña,categoria_servicio
1,1,"Excelente comunicación, buena calidad y entrega rápida.","2026-06-01","Desarrollo de Software"


---

## 9. Parámetros de entrenamiento

Al entrenar un modelo, se debe seleccionar:

* Tipo de dataset: freelancers o reviews
* Archivo CSV
* Algoritmo de clustering
* Número de clusters, cuando aplique
* Parámetros específicos del algoritmo
* Columna de texto para reseñas
* Vectorizador de texto para reseñas

Algoritmos disponibles:

txt
kmeans
dbscan
gmm
agglomerative


Para reseñas, la columna de texto debe ser:

txt
texto_reseña


Vectorizadores disponibles:

txt
tfidf
bow


---

## 10. Clasificación de nuevo registro

La vista de clasificación permite asignar un nuevo freelancer o una nueva reseña a un segmento existente sin reentrenar el modelo.

Para clasificar un freelancer, se ingresan los mismos campos del CSV de freelancers, excepto:

txt
freelancer_id


Para clasificar una reseña, se ingresa un texto libre. El sistema transforma esa reseña usando el mismo vectorizador utilizado durante el entrenamiento.

La salida incluye:

txt
Cluster asignado
Nombre interpretativo del segmento
Descripción interpretativa del segmento


---

## 11. Exportación de reportes

La vista de exportación permite descargar:

txt
CSV con resultados del clustering
PDF con reporte del modelo


El CSV exportado incluye las columnas originales junto con:

txt
cluster
cluster_name
pc1
pc2


El PDF incluye información general del modelo, métricas, distribución de clusters y visualización PCA/SVD.

---

## 12. Comandos rápidos

Levantar backend:

bash
cd backend
python -m uvicorn app.app:app --reload


Levantar frontend:

bash
cd frontend
npm run dev


Backend:

txt
http://127.0.0.1:8000


Frontend:

txt
http://localhost:5173


Documentación API:

txt
http://127.0.0.1:8000/docs


---

## 13. Notas importantes

* Primero deben cargarse y limpiarse los CSV antes de entrenar.
* Para reseñas, usar la columna texto_reseña.
* Para la tabla cruzada, ambos datasets deben compartir la columna freelancer_id.
* El número del cluster no representa por sí mismo que un segmento sea bueno o malo.
* La interpretación útil está en el nombre del segmento y la descripción generada.
* Si se elimina la carpeta storage, se pierden los modelos entrenados y archivos procesados.


