import { useState } from "react";
import { predecirSolicitante } from "../api/Api";

function PredictionForm() {
  const [formData, setFormData] = useState({
    ingresos_mensuales: 5000,
    deuda_activa: 12000,
    historial_pagos: 75,
    antiguedad_laboral: 3,
    creditos_activos: 2,
    monto_solicitado: 25000,
    atrasos_previos: 1,
    dependientes_economicos: 2,
    utilizacion_credito: 60,
  });

  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const [resultado, setResultado] = useState(null);

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((prev) => ({
      ...prev,
      [name]: Number(value),
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      setCargando(true);
      setError("");
      setResultado(null);

      const data = await predecirSolicitante(formData);
      setResultado(data);
    } catch (err) {
      setError(
        err.message ||
          "No se pudo realizar la predicción. Primero debes entrenar el modelo."
      );
    } finally {
      setCargando(false);
    }
  };

  const hayResultado = resultado !== null;
  const esRiesgo = resultado?.riesgo === true;
  const esSinRiesgo = resultado?.riesgo === false;

  return (
    <>
      <section className="card">
        <div className="card-header">
          <div>
            <h2>Datos del Solicitante</h2>
            <p>Información crediticia</p>
          </div>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="prediction-form-grid">
            <div className="form-group">
              <label>Ingresos mensuales (Q)</label>
              <input
                type="number"
                name="ingresos_mensuales"
                value={formData.ingresos_mensuales}
                onChange={handleChange}
                min="1"
                step="0.01"
                placeholder="Ej. 5000"
                required
              />
            </div>

            <div className="form-group">
              <label>Monto solicitado (Q)</label>
              <input
                type="number"
                name="monto_solicitado"
                value={formData.monto_solicitado}
                onChange={handleChange}
                min="1"
                step="0.01"
                placeholder="Ej. 25000"
                required
              />
            </div>

            <div className="form-group">
              <label>Deuda activa (Q)</label>
              <input
                type="number"
                name="deuda_activa"
                value={formData.deuda_activa}
                onChange={handleChange}
                min="0"
                step="0.01"
                placeholder="Ej. 12000"
                required
              />
            </div>

            <div className="form-group">
              <label>Atrasos previos últimos 12 m</label>
              <input
                type="number"
                name="atrasos_previos"
                value={formData.atrasos_previos}
                onChange={handleChange}
                min="0"
                step="1"
                placeholder="Ej. 1"
                required
              />
            </div>

            <div className="form-group">
              <label>Historial de pagos (0-100)</label>
              <input
                type="number"
                name="historial_pagos"
                value={formData.historial_pagos}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.01"
                placeholder="Ej. 75"
                required
              />
            </div>

            <div className="form-group">
              <label>Dependientes económicos</label>
              <input
                type="number"
                name="dependientes_economicos"
                value={formData.dependientes_economicos}
                onChange={handleChange}
                min="0"
                step="1"
                placeholder="Ej. 2"
                required
              />
            </div>

            <div className="form-group">
              <label>Antigüedad laboral (años)</label>
              <input
                type="number"
                name="antiguedad_laboral"
                value={formData.antiguedad_laboral}
                onChange={handleChange}
                min="0"
                step="0.01"
                placeholder="Ej. 3"
                required
              />
            </div>

            <div className="form-group">
              <label>Utilización del crédito (%)</label>
              <input
                type="number"
                name="utilizacion_credito"
                value={formData.utilizacion_credito}
                onChange={handleChange}
                min="0"
                max="100"
                step="0.01"
                placeholder="Ej. 60"
                required
              />
            </div>

            <div className="form-group">
              <label>Créditos activos</label>
              <input
                type="number"
                name="creditos_activos"
                value={formData.creditos_activos}
                onChange={handleChange}
                min="0"
                step="1"
                placeholder="Ej. 2"
                required
              />
            </div>
          </div>

          {error && <p className="error-message">{error}</p>}

          <div className="prediction-button-wrapper">
            <button className="btn btn-primary" type="submit" disabled={cargando}>
              {cargando ? "Calculando..." : "Realizar Predicción"}
            </button>
          </div>
        </form>
      </section>

      <section className="card">
        <div className="card-header">
          <div>
            <h2>Resultado de la Predicción</h2>
            <p>
              Los dos estados son mutuamente excluyentes. Se muestra uno según
              el resultado calculado por el modelo.
            </p>
          </div>
        </div>

        {!hayResultado && (
          <p className="info-message">
            Ingresa los datos del solicitante y presiona “Realizar Predicción”.
          </p>
        )}

        <div className="prediction-result-layout">
          <div
            className={
              esRiesgo
                ? "prediction-state-card risk active"
                : "prediction-state-card risk"
            }
          >
            <div className="prediction-state-label">ESTADO A — Riesgo</div>

            <div className="prediction-state-icon">!</div>

            <h3>EN RIESGO DE INCUMPLIMIENTO</h3>

            <p>
              El modelo estima que este solicitante tiene una alta probabilidad
              de no cumplir con sus obligaciones crediticias.
            </p>

            <div className="prediction-state-note">
              Se recomienda revisar manualmente el expediente antes de aprobar.
            </div>

            {esRiesgo && (
              <div className="prediction-confidence">
                Confianza: <strong>{resultado.confianza}%</strong>
              </div>
            )}
          </div>

          <div
            className={
              esSinRiesgo
                ? "prediction-state-card no-risk active"
                : "prediction-state-card no-risk"
            }
          >
            <div className="prediction-state-label">
              ESTADO B — Posible resultado alterno
            </div>

            <div className="prediction-state-icon">✓</div>

            <h3>SIN RIESGO DETECTADO</h3>

            <p>
              El modelo estima que este solicitante tiene un bajo perfil de
              riesgo crediticio.
            </p>

            <div className="prediction-state-note">
              El perfil es apto para continuar con el proceso de aprobación.
            </div>

            {esSinRiesgo && (
              <div className="prediction-confidence">
                Confianza: <strong>{resultado.confianza}%</strong>
              </div>
            )}
          </div>
        </div>

        {resultado && (
          <div className="prediction-raw-summary">
            <span>Clase del modelo: {resultado.clase}</span>
            <span>Resultado: {resultado.mensaje}</span>
          </div>
        )}
      </section>
    </>
  );
}

export default PredictionForm;