import { useState } from "react";
import StatusPanel from "../components/StatusPanel";
import CsvUploader from "../components/CsvUploader";
import { entrenarModelo } from "../api/Api";

function TrainingPage({ onSystemChange }) {
  const [hiperparametros, setHiperparametros] = useState({
    n_arboles: 80,
    max_depth: 10,
    max_leaves: 50,
  });

  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const [respuesta, setRespuesta] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setHiperparametros((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  const handleEntrenar = async () => {
    try {
      setCargando(true);
      setError("");
      setRespuesta(null);

      const data = await entrenarModelo(hiperparametros);

      setRespuesta(data);

      if (onSystemChange) {
        onSystemChange();
      }
    } catch (err) {
      setError(err.message || "No se pudo entrenar el modelo.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="page-content">
      <div className="page-title">
        <h1>Carga y Entrenamiento</h1>
        <p>
          Sube el archivo CSV, limpia los datos y entrena el modelo de riesgo
          crediticio.
        </p>
      </div>

      <StatusPanel />

      <CsvUploader onCsvLoaded={onSystemChange} />

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Entrenamiento del modelo</h2>
            <p>
              Configura los parámetros iniciales y entrena el Random Forest del
              sistema.
            </p>
          </div>
        </div>

        <div className="form-grid">
          <div className="form-group">
            <label>Cantidad de árboles</label>
            <input
              type="number"
              name="n_arboles"
              value={hiperparametros.n_arboles}
              onChange={handleChange}
              min="1"
            />
          </div>

          <div className="form-group">
            <label>Profundidad máxima</label>
            <input
              type="number"
              name="max_depth"
              value={hiperparametros.max_depth}
              onChange={handleChange}
              min="1"
            />
          </div>

          <div className="form-group">
            <label>Número máximo de hojas</label>
            <input
              type="number"
              name="max_leaves"
              value={hiperparametros.max_leaves}
              onChange={handleChange}
              min="2"
            />
          </div>
        </div>

        {error && <p className="error-message">{error}</p>}

        {respuesta && (
          <div className="success-box">
            <h3>{respuesta.mensaje}</h3>

            <div className="metrics-grid">
              <div>
                <span>Exactitud</span>
                <strong>{(respuesta.metricas.exactitud * 100).toFixed(2)}%</strong>
              </div>

              <div>
                <span>Precisión</span>
                <strong>{(respuesta.metricas.precision * 100).toFixed(2)}%</strong>
              </div>

              <div>
                <span>Recall</span>
                <strong>{(respuesta.metricas.recall * 100).toFixed(2)}%</strong>
              </div>

              <div>
                <span>F1 Score</span>
                <strong>{(respuesta.metricas.f1 * 100).toFixed(2)}%</strong>
              </div>
            </div>

            {respuesta.resumen_datos && (
              <div className="cleaning-summary">
                <h3>Resumen de datos</h3>
                <p>
                  Entrenamiento:{" "}
                  <strong>{respuesta.resumen_datos.entrenamiento}</strong>
                </p>
                <p>
                  Prueba: <strong>{respuesta.resumen_datos.prueba}</strong>
                </p>
                <p>
                  Clase 0 entrenamiento:{" "}
                  <strong>{respuesta.resumen_datos.clase_0_train}</strong>
                </p>
                <p>
                  Clase 1 entrenamiento:{" "}
                  <strong>{respuesta.resumen_datos.clase_1_train}</strong>
                </p>
              </div>
            )}
          </div>
        )}

        <button
          className="btn btn-primary"
          onClick={handleEntrenar}
          disabled={cargando}
        >
          {cargando ? "Entrenando..." : "Entrenar modelo"}
        </button>
      </section>
    </div>
  );
}

export default TrainingPage;