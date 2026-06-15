import { useEffect, useState } from "react";
import { obtenerEstadoModelo } from "../api/Api";

function StatusPanel() {
  const [estado, setEstado] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");

  const cargarEstado = async () => {
    try {
      setCargando(true);
      setError("");

      const data = await obtenerEstadoModelo();
      setEstado(data);
    } catch (err) {
      setError(err.message || "No se pudo obtener el estado del modelo.");
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarEstado();
  }, []);

  return (
    <section className="card">
      <div className="card-header">
        <div>
          <h2>Estado del sistema</h2>
          <p>Verifica el estado actual del motor de Machine Learning.</p>
        </div>

        <button className="btn btn-secondary" onClick={cargarEstado}>
          Actualizar
        </button>
      </div>

      {cargando && <p className="info-message">Consultando estado...</p>}

      {error && <p className="error-message">{error}</p>}

      {estado && (
        <div className="status-grid">
          <div className="status-item">
            <span className="status-label">Datos cargados</span>
            <span className={estado.datos_cargados ? "badge success" : "badge warning"}>
              {estado.datos_cargados ? "Sí" : "No"}
            </span>
          </div>

          <div className="status-item">
            <span className="status-label">Datos limpios</span>
            <span className={estado.datos_limpios ? "badge success" : "badge warning"}>
              {estado.datos_limpios ? "Sí" : "No"}
            </span>
          </div>

          <div className="status-item">
            <span className="status-label">Modelo entrenado</span>
            <span className={estado.modelo_entrenado ? "badge success" : "badge warning"}>
              {estado.modelo_entrenado ? "Sí" : "No"}
            </span>
          </div>

          <div className="status-item">
            <span className="status-label">Registros limpios</span>
            <strong>{estado.total_limpio ?? 0}</strong>
          </div>
        </div>
      )}

      {estado?.metricas && (
        <div className="metrics-mini">
          <h3>Métricas actuales</h3>

          <div className="metrics-grid">
            <div>
              <span>Exactitud</span>
              <strong>{(estado.metricas.exactitud * 100).toFixed(2)}%</strong>
            </div>

            <div>
              <span>Precisión</span>
              <strong>{(estado.metricas.precision * 100).toFixed(2)}%</strong>
            </div>

            <div>
              <span>Recall</span>
              <strong>{(estado.metricas.recall * 100).toFixed(2)}%</strong>
            </div>

            <div>
              <span>F1 Score</span>
              <strong>{(estado.metricas.f1 * 100).toFixed(2)}%</strong>
            </div>
          </div>
        </div>
      )}

      {estado?.reporte_limpieza && (
        <div className="cleaning-summary">
          <h3>Resumen de limpieza</h3>

          <p>
            Total original: <strong>{estado.reporte_limpieza.total_original}</strong>
          </p>
          <p>
            Total limpio: <strong>{estado.reporte_limpieza.total_limpio}</strong>
          </p>
          <p>
            Filas eliminadas: <strong>{estado.reporte_limpieza.filas_eliminadas}</strong>
          </p>
          <p>
            Valores imputados: <strong>{estado.reporte_limpieza.valores_imputados}</strong>
          </p>
        </div>
      )}
    </section>
  );
}

export default StatusPanel;