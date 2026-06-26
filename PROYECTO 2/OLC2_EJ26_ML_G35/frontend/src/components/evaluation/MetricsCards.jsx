import Card from "../ui/Card";
import Badge from "../ui/Badge";

function formatMetric(value) {
  if (value === null || value === undefined) {
    return "No disponible";
  }

  return Number(value).toFixed(4);
}

function getSilhouetteInterpretation(value) {
  if (value === null || value === undefined) {
    return {
      label: "No disponible",
      variant: "warning",
      description: "No fue posible calcular esta métrica.",
    };
  }

  if (value >= 0.7) {
    return {
      label: "Muy bueno",
      variant: "success",
      description: "Los clusters están bien separados.",
    };
  }

  if (value >= 0.5) {
    return {
      label: "Bueno",
      variant: "success",
      description: "Existe una separación aceptable entre clusters.",
    };
  }

  if (value >= 0.25) {
    return {
      label: "Moderado",
      variant: "warning",
      description: "Los clusters tienen cierta separación, pero podrían mejorar.",
    };
  }

  return {
    label: "Débil",
    variant: "danger",
    description: "Los clusters están poco separados o se mezclan entre sí.",
  };
}

function getDaviesInterpretation(value) {
  if (value === null || value === undefined) {
    return {
      label: "No disponible",
      variant: "warning",
      description: "No fue posible calcular esta métrica.",
    };
  }

  if (value <= 1) {
    return {
      label: "Bueno",
      variant: "success",
      description: "Los clusters son compactos y están relativamente separados.",
    };
  }

  if (value <= 2) {
    return {
      label: "Aceptable",
      variant: "warning",
      description: "La separación es razonable, aunque puede mejorar.",
    };
  }

  return {
    label: "Alto",
    variant: "danger",
    description: "Puede existir solapamiento entre clusters.",
  };
}

function getCalinskiInterpretation(value) {
  if (value === null || value === undefined) {
    return {
      label: "No disponible",
      variant: "warning",
      description: "No fue posible calcular esta métrica.",
    };
  }

  return {
    label: "Referencia comparativa",
    variant: "default",
    description:
      "Esta métrica se usa mejor para comparar modelos: mientras mayor sea, mejor.",
  };
}

function MetricCard({ title, value, interpretation, helper }) {
  return (
    <div className="evaluation-metric-card">
      <div className="evaluation-metric-header">
        <span>{title}</span>
        <Badge variant={interpretation.variant}>{interpretation.label}</Badge>
      </div>

      <strong>{formatMetric(value)}</strong>

      <p>{helper}</p>

      <small>{interpretation.description}</small>
    </div>
  );
}

function MetricsCards({ model }) {
  if (!model) {
    return (
      <Card
        title="Métricas del modelo"
        description="Selecciona un modelo entrenado para visualizar sus métricas."
      >
        <p className="muted">
          Todavía no hay un modelo seleccionado para evaluar.
        </p>
      </Card>
    );
  }

  const metrics = model.metrics || {};

  const silhouette = metrics.silhouette_score;
  const davies = metrics.davies_bouldin_score;
  const calinski = metrics.calinski_harabasz_score;

  return (
    <Card
      title="Métricas del modelo seleccionado"
      description="Estas métricas permiten validar la calidad interna del agrupamiento."
    >
      <div className="selected-model-box">
        <span>Modelo seleccionado</span>
        <strong>{model.model_id}</strong>

        <div className="badges-row">
          <Badge variant="success">{model.dataset_type}</Badge>
          <Badge>{model.algorithm}</Badge>
          <Badge>{model.filename}</Badge>
        </div>
      </div>

      <div className="evaluation-grid">
        <MetricCard
          title="Silhouette Score"
          value={silhouette}
          interpretation={getSilhouetteInterpretation(silhouette)}
          helper="Mide qué tan bien separado está cada punto de otros clusters. Más alto es mejor."
        />

        <MetricCard
          title="Davies-Bouldin Score"
          value={davies}
          interpretation={getDaviesInterpretation(davies)}
          helper="Mide similitud entre clusters. Más bajo es mejor."
        />

        <MetricCard
          title="Calinski-Harabasz Score"
          value={calinski}
          interpretation={getCalinskiInterpretation(calinski)}
          helper="Mide separación entre clusters contra compactación interna. Más alto es mejor."
        />
      </div>
    </Card>
  );
}

export default MetricsCards;