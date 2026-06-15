import MetricsPanel from "../components/MetricsPanel";

function EvaluationPage() {
  return (
    <div className="page-content">
      <div className="page-title">
        <h1>Evaluación de Rendimiento</h1>
        <p>
          Consulta las métricas obtenidas después del entrenamiento del modelo.
        </p>
      </div>

      <MetricsPanel />
    </div>
  );
}

export default EvaluationPage;