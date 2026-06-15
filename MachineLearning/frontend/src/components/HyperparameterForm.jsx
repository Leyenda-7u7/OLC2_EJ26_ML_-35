import { useState } from "react";
import { reentrenarModelo } from "../api/Api";

function HyperparameterForm() {
  const [hiperparametros, setHiperparametros] = useState({
    n_arboles: 120,
    max_depth: 12,
    max_leaves: 60,
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

  const handleReentrenar = async () => {
    try {
      setCargando(true);
      setError("");
      setRespuesta(null);

      const data = await reentrenarModelo(hiperparametros);

      setRespuesta(data);
    } catch (err) {
      setError(
        err.message ||
          "No se pudo reentrenar el modelo. Primero debes cargar un CSV y entrenar el modelo."
      );
    } finally {
      setCargando(false);
    }
  };

  return (
    <section className="card">
      <div className="card-header">
        <div>
          <h2>Ajuste de hiperparámetros</h2>
          <p>
            Modifica los parámetros principales del Random Forest y reentrena el
            modelo.
          </p>
        </div>
      </div>

      <div className="form-grid">
        <div className="form-group">
          <label>Cantidad de árboles de decisión</label>
          <input
            type="number"
            name="n_arboles"
            value={hiperparametros.n_arboles}
            onChange={handleChange}
            min="1"
          />
        </div>

        <div className="form-group">
          <label>Profundidad máxima de los árboles</label>
          <input
            type="number"
            name="max_depth"
            value={hiperparametros.max_depth}
            onChange={handleChange}
            min="1"
          />
        </div>

        <div className="form-group">
          <label>Número máximo de hojas por árbol</label>
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

      <button
        className="btn btn-primary"
        onClick={handleReentrenar}
        disabled={cargando}
      >
        {cargando ? "Reentrenando..." : "Reentrenar modelo"}
      </button>

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

          {respuesta.metricas.matriz && (
            <div className="confusion-section">
              <h3>Matriz de confusión actualizada</h3>

              <div className="confusion-grid">
                <div className="confusion-cell true-cell">
                  <span>Verdaderos positivos</span>
                  <strong>{respuesta.metricas.matriz.VP}</strong>
                </div>

                <div className="confusion-cell false-cell">
                  <span>Falsos positivos</span>
                  <strong>{respuesta.metricas.matriz.FP}</strong>
                </div>

                <div className="confusion-cell false-cell">
                  <span>Falsos negativos</span>
                  <strong>{respuesta.metricas.matriz.FN}</strong>
                </div>

                <div className="confusion-cell true-cell">
                  <span>Verdaderos negativos</span>
                  <strong>{respuesta.metricas.matriz.VN}</strong>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </section>
  );
}

export default HyperparameterForm;