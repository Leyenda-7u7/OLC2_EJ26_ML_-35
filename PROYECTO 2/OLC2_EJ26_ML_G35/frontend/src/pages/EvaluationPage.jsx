import { useMemo, useState } from "react";

import PageContainer from "../components/layouts/PageContainer";
import Card from "../components/ui/Card";
import Button from "../components/ui/Button";
import Badge from "../components/ui/Badge";

import MetricsCards from "../components/evaluation/MetricsCards";
import MetricsExplanation from "../components/evaluation/MetricsExplanation";
import MetricsComparisonChart from "../components/evaluation/MetricsComparisonChart";

import { useModelStore } from "../hooks/useModelStore";

function formatMetric(value) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  return Number(value).toFixed(4);
}

function EvaluationPage() {
  const { lastModel, models, clearModels } = useModelStore();

  const [selectedModelId, setSelectedModelId] = useState(
    lastModel?.model_id || ""
  );

  const selectedModel = useMemo(() => {
    return models.find((model) => model.model_id === selectedModelId) || null;
  }, [models, selectedModelId]);

  return (
    <PageContainer
      title="Evaluación y validación"
      description="Consulta métricas internas del clustering y compara modelos entrenados para justificar la configuración seleccionada."
    >
      <Card
        title="Seleccionar modelo"
        description="El historial se guarda localmente con los modelos que has entrenado desde el frontend."
      >
        <div className="form-grid-2">
          <label className="form-control">
            <span>Modelo entrenado</span>

            <select
              value={selectedModelId}
              onChange={(event) => setSelectedModelId(event.target.value)}
            >
              <option value="">Selecciona un modelo</option>

              {models.map((model) => (
                <option key={model.model_id} value={model.model_id}>
                  {model.dataset_type} · {model.algorithm} · {model.filename}
                </option>
              ))}
            </select>
          </label>

          <div className="evaluation-actions">
            <Button
              variant="secondary"
              onClick={clearModels}
              disabled={models.length === 0}
            >
              Limpiar historial
            </Button>
          </div>
        </div>
      </Card>

      <div className="grid-2">
        <MetricsCards model={selectedModel} />
        <MetricsExplanation />
      </div>

      <MetricsComparisonChart models={models} />

      <Card
        title="Comparación de modelos entrenados"
        description="Usa esta tabla para comparar configuraciones y decidir cuál modelo tiene mejor comportamiento."
      >
        {models.length === 0 ? (
          <p className="muted">
            Aún no hay modelos entrenados en el historial local.
          </p>
        ) : (
          <div className="table-wrapper">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Dataset</th>
                  <th>Algoritmo</th>
                  <th>Archivo</th>
                  <th>Clusters</th>
                  <th>Ruido</th>
                  <th>Silhouette</th>
                  <th>Davies-Bouldin</th>
                  <th>Calinski-Harabasz</th>
                  <th>Model ID</th>
                </tr>
              </thead>

              <tbody>
                {models.map((model) => (
                  <tr key={model.model_id}>
                    <td>
                      <Badge variant="success">{model.dataset_type}</Badge>
                    </td>
                    <td>{model.algorithm}</td>
                    <td>{model.filename}</td>
                    <td>{model.clusters_found}</td>
                    <td>{model.noise_points}</td>
                    <td>{formatMetric(model.metrics?.silhouette_score)}</td>
                    <td>{formatMetric(model.metrics?.davies_bouldin_score)}</td>
                    <td>
                      {formatMetric(model.metrics?.calinski_harabasz_score)}
                    </td>
                    <td className="model-id-cell">{model.model_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </PageContainer>
  );
}

export default EvaluationPage;