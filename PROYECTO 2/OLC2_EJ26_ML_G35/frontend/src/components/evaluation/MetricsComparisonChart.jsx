import { useMemo, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

import Card from "../ui/Card";

const METRIC_OPTIONS = [
  {
    value: "silhouette_score",
    label: "Silhouette Score",
    help: "Más alto es mejor.",
  },
  {
    value: "davies_bouldin_score",
    label: "Davies-Bouldin Score",
    help: "Más bajo es mejor.",
  },
  {
    value: "calinski_harabasz_score",
    label: "Calinski-Harabasz Score",
    help: "Más alto es mejor.",
  },
];

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const point = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>{label}</strong>
      <p>Valor: {Number(point.metric_value).toFixed(4)}</p>
      <p>Dataset: {point.dataset_type}</p>
      <p>Algoritmo: {point.algorithm}</p>
      <p>Archivo: {point.filename}</p>
    </div>
  );
}

function MetricsComparisonChart({ models }) {
  const [selectedMetric, setSelectedMetric] = useState("silhouette_score");

  const selectedMetricMeta = METRIC_OPTIONS.find(
    (option) => option.value === selectedMetric
  );

  const chartData = useMemo(() => {
    if (!models || models.length === 0) {
      return [];
    }

    return models.map((model, index) => ({
      name: `${model.dataset_type}-${index + 1}`,
      dataset_type: model.dataset_type,
      algorithm: model.algorithm,
      filename: model.filename,
      model_id: model.model_id,
      metric_value: Number(model.metrics?.[selectedMetric] ?? 0),
    }));
  }, [models, selectedMetric]);

  if (!models || models.length === 0) {
    return (
      <Card
        title="Gráfica comparativa"
        description="Aquí se mostrará una comparación visual entre los modelos entrenados."
      >
        <p className="muted">
          Aún no hay modelos en el historial para graficar.
        </p>
      </Card>
    );
  }

  return (
    <Card
      title="Gráfica comparativa de métricas"
      description="Compara visualmente el comportamiento de los modelos entrenados."
    >
      <div className="chart-controls">
        <label className="form-control">
          <span>Métrica a comparar</span>
          <select
            value={selectedMetric}
            onChange={(event) => setSelectedMetric(event.target.value)}
          >
            {METRIC_OPTIONS.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <div className="metric-helper-box">
          <strong>{selectedMetricMeta?.label}</strong>
          <p>{selectedMetricMeta?.help}</p>
        </div>
      </div>

      <div className="chart-box">
        <ResponsiveContainer width="100%" height={360}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="metric_value" name={selectedMetricMeta?.label} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default MetricsComparisonChart;