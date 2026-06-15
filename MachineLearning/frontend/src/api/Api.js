const API_BASE_URL = "http://127.0.0.1:8000";

/**
 * Función auxiliar para manejar respuestas del backend.
 */
async function handleResponse(response) {
  const data = await response.json();

  if (!response.ok) {
    const message = data.detail || "Ocurrió un error en la petición.";
    throw new Error(message);
  }

  return data;
}

/**
 * Verifica si la API está funcionando.
 * GET /
 */
export async function verificarApi() {
  const response = await fetch(`${API_BASE_URL}/`);
  return handleResponse(response);
}

/**
 * Obtiene el estado actual del motor ML.
 * GET /modelo/estado
 */
export async function obtenerEstadoModelo() {
  const response = await fetch(`${API_BASE_URL}/modelo/estado`);
  return handleResponse(response);
}

/**
 * Carga un archivo CSV al backend.
 * POST /csv/cargar
 */
export async function cargarCsv(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/csv/cargar`, {
    method: "POST",
    body: formData,
  });

  return handleResponse(response);
}

/**
 * Entrena el modelo con hiperparámetros.
 * POST /modelo/entrenar
 */
export async function entrenarModelo(hiperparametros) {
  const response = await fetch(`${API_BASE_URL}/modelo/entrenar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(hiperparametros),
  });

  return handleResponse(response);
}

/**
 * Reentrena el modelo con nuevos hiperparámetros.
 * POST /modelo/reentrenar
 */
export async function reentrenarModelo(hiperparametros) {
  const response = await fetch(`${API_BASE_URL}/modelo/reentrenar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(hiperparametros),
  });

  return handleResponse(response);
}

/**
 * Obtiene las métricas actuales del modelo.
 * GET /modelo/metricas
 */
export async function obtenerMetricas() {
  const response = await fetch(`${API_BASE_URL}/modelo/metricas`);
  return handleResponse(response);
}

/**
 * Obtiene el reporte de limpieza.
 * GET /modelo/reporte-limpieza
 */
export async function obtenerReporteLimpieza() {
  const response = await fetch(`${API_BASE_URL}/modelo/reporte-limpieza`);
  return handleResponse(response);
}

/**
 * Realiza una predicción individual.
 * POST /predicciones/predecir
 */
export async function predecirSolicitante(datosSolicitante) {
  const response = await fetch(`${API_BASE_URL}/predicciones/predecir`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(datosSolicitante),
  });

  return handleResponse(response);
}