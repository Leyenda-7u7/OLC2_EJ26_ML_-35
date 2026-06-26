import Badge from "../ui/Badge";
import Card from "../ui/Card";

function formatMetric(value) {
  if (value === null || value === undefined) {
    return "No disponible";
  }

  return Number(value).toFixed(4);
}

function TrainingResult({ result }) {
  if (!result) {
    return (
      <Card
        title="Resultado del entrenamiento"
        description="Cuando entrenes un modelo, aquí aparecerá el identificador, métricas y detalles principales."
      >
        <p className="muted">Todavía no se ha entrenado ningún modelo.</p>
      </Card>
    );
  }

  return (
    <Card
      title="Modelo entrenado correctamente"
      description="Guarda el model_id para análisis, evaluación, clasificación y exportación."
    >
      <div className="result-section">
        <div className="model-id-box">
          <span>Model ID</span>
          <strong>{result.model_id}</strong>
        </div>

        <div className="badges-row">
          <Badge variant="success">{result.dataset_type}</Badge>
          <Badge>{result.algorithm}</Badge>
          <Badge>{result.filename}</Badge>
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <span>Registros</span>
            <strong>{result.total_records}</strong>
          </div>

          <div className="stat-card">
            <span>Features</span>
            <strong>{result.total_features}</strong>
          </div>

          <div className="stat-card">
            <span>Clusters</span>
            <strong>{result.clusters_found}</strong>
          </div>

          <div className="stat-card">
            <span>Ruido</span>
            <strong>{result.noise_points}</strong>
          </div>
        </div>

        <div className="metrics-grid">
          <div className="metric-card">
            <span>Silhouette Score</span>
            <strong>{formatMetric(result.metrics?.silhouette_score)}</strong>
            <p>Más alto es mejor.</p>
          </div>

          <div className="metric-card">
            <span>Davies-Bouldin</span>
            <strong>{formatMetric(result.metrics?.davies_bouldin_score)}</strong>
            <p>Más bajo es mejor.</p>
          </div>

          <div className="metric-card">
            <span>Calinski-Harabasz</span>
            <strong>{formatMetric(result.metrics?.calinski_harabasz_score)}</strong>
            <p>Más alto es mejor.</p>
          </div>
        </div>

        {result.pca_explained_variance && (
          <div className="variance-box">
            <span>Varianza explicada PCA/SVD</span>
            <p>
              {result.pca_explained_variance
                .map((value) => Number(value).toFixed(4))
                .join(" + ")}
            </p>
          </div>
        )}
      </div>
    </Card>
  );
}

export default TrainingResult;