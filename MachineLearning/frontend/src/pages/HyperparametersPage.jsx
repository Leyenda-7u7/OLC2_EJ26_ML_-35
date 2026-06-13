import HyperparameterForm from "../components/HyperparameterForm";

function HyperparametersPage() {
  return (
    <div className="page-content">
      <div className="page-title">
        <h1>Ajuste de Hiperparámetros</h1>
        <p>
          Configura los hiperparámetros del modelo y vuelve a entrenarlo para
          comparar su rendimiento.
        </p>
      </div>

      <HyperparameterForm />
    </div>
  );
}

export default HyperparametersPage;