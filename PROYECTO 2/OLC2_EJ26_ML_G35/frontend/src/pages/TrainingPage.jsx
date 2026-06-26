import { useState } from "react";

import PageContainer from "../components/layouts/PageContainer";
import TrainingForm from "../components/training/TrainingForm";
import TrainingResult from "../components/training/TrainingResult";

import { useModelStore } from "../hooks/useModelStore";

function TrainingPage() {
  const { lastModel, saveModel } = useModelStore();
  const [trainingResult, setTrainingResult] = useState(lastModel);

  const handleTrainingSuccess = (result) => {
    setTrainingResult(result);
    saveModel(result);
  };

  return (
    <PageContainer
      title="Configuración y entrenamiento"
      description="Selecciona el dataset, algoritmo y parámetros para entrenar el modelo de clustering."
    >
      <div className="grid-2">
        <TrainingForm onTrainingSuccess={handleTrainingSuccess} />
        <TrainingResult result={trainingResult} />
      </div>
    </PageContainer>
  );
}

export default TrainingPage;