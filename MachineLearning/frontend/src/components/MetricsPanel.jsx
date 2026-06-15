import { useEffect, useState } from "react";
import { obtenerMetricas } from "../api/Api";

function MetricsPanel() {
  const [metricas, setMetricas] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const cargarMetricas = async () => {
    try {
      setCargando(true);
      setError("");

      const data = await obtenerMetricas();

      setMetricas(data.metricas);
    } catch (err) {
      setMetricas(null);
      setError(
        err.message ||
          "No se pudieron obtener las métricas. Primero debes entrenar el modelo."
      );
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarMetricas();
  }, []);

  return (
    <section className="card">
      <div className="card-header">
        <div>
          <h2>Evaluación de rendimiento</h2>
          <p>
            Métricas obtenidas a partir del conjunto de prueba del modelo
            entrenado.
          </p>
        </div>

        <button className="btn btn-secondary" onClick={cargarMetricas}>
          Actualizar
        </button>
      </div>

      {cargando && <p className="info-message">Consultando métricas...</p>}

      {error && <p className="error-message">{error}</p>}

      {metricas && (
        <>
          <div className="metrics-grid">
            <div>
              <span>Exactitud</span>
              <strong>{(metricas.exactitud * 100).toFixed(2)}%</strong>
              <small>Predicciones correctas sobre el total.</small>
            </div>

            <div>
              <span>Precisión</span>
              <strong>{(metricas.precision * 100).toFixed(2)}%</strong>
              <small>Casos de riesgo predichos correctamente.</small>
            </div>

            <div>
              <span>Recall</span>
              <strong>{(metricas.recall * 100).toFixed(2)}%</strong>
              <small>Capacidad para detectar solicitantes en riesgo.</small>
            </div>

            <div>
              <span>F1 Score</span>
              <strong>{(metricas.f1 * 100).toFixed(2)}%</strong>
              <small>Balance entre precisión y recall.</small>
            </div>
          </div>

          {metricas.matriz && (
            <div className="confusion-section">
              <h3>Matriz de confusión</h3>

              <div className="confusion-grid">
                <div className="confusion-cell true-cell">
                  <span>Verdaderos positivos</span>
                  <strong>{metricas.matriz.VP}</strong>
                  <small>Riesgo real predicho como riesgo</small>
                </div>

                <div className="confusion-cell false-cell">
                  <span>Falsos positivos</span>
                  <strong>{metricas.matriz.FP}</strong>
                  <small>Sin riesgo predicho como riesgo</small>
                </div>

                <div className="confusion-cell false-cell">
                  <span>Falsos negativos</span>
                  <strong>{metricas.matriz.FN}</strong>
                  <small>Riesgo real predicho como sin riesgo</small>
                </div>

                <div className="confusion-cell true-cell">
                  <span>Verdaderos negativos</span>
                  <strong>{metricas.matriz.VN}</strong>
                  <small>Sin riesgo predicho como sin riesgo</small>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </section>
  );
}

export default MetricsPanel;