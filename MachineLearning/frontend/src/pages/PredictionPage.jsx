import PredictionForm from "../components/PredictionForm";

function PredictionPage() {
  return (
    <div className="page-content">
      <div className="page-title">
        <h1>Predicción Individual</h1>
        <p>
          Ingresa los datos del solicitante para determinar su nivel de riesgo
          crediticio.
        </p>
      </div>

      <PredictionForm />
    </div>
  );
}

export default PredictionPage;