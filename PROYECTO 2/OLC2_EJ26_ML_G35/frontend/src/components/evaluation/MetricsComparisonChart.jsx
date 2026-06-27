import { useMemo } from "react";
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

import Card from "../ui/Card";

const SUPPORTED_ALGORITHMS = new Set(["kmeans", "gmm"]);

function CustomTooltip({ active, payload }) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const point = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>k = {point.k}</strong>
      <p>Silhouette: {Number(point.silhouette).toFixed(4)}</p>
      <p>Dataset: {point.dataset_type}</p>
      <p>Algoritmo: {point.algorithm}</p>
      <p>Archivo: {point.filename}</p>
    </div>
  );
}

function MetricsComparisonChart({ models }) {
  const chartData = useMemo(() => {
    if (!models || models.length === 0) {
      return [];
    }

    return models
      .filter((model) =>
        SUPPORTED_ALGORITHMS.has(String(model.algorithm).toLowerCase())
      )
      .map((model) => {
        const k = Number(model.clusters_found);
        const silhouette = model.metrics?.silhouette_score;

        return {
          k,
          kLabel: String(k),
          silhouette:
            silhouette === null || silhouette === undefined
              ? null
              : Number(silhouette),
          dataset_type: model.dataset_type,
          algorithm: model.algorithm,
          filename: model.filename,
          model_id: model.model_id,
        };
      })
      .filter(
        (point) =>
          Number.isFinite(point.k) &&
          point.k > 0 &&
          point.silhouette !== null &&
          Number.isFinite(point.silhouette)
      )
      .sort((pointA, pointB) => pointA.k - pointB.k);
  }, [models]);

  const kRangeLabel = useMemo(() => {
    if (chartData.length === 0) {
      return "k";
    }

    const minK = chartData[0].k;
    const maxK = chartData[chartData.length - 1].k;

    if (minK === maxK) {
      return `k (${minK})`;
    }

    return `k (${minK} a ${maxK})`;
  }, [chartData]);

  if (!models || models.length === 0) {
    return (
      <Card
        title="Seleccion del Numero de Clusters"
        description="Compara la relacion entre k y el Silhouette usando modelos KMeans y GMM del historial local."
      >
        <p className="muted">
          Aun no hay modelos en el historial para construir la grafica.
        </p>
      </Card>
    );
  }

  if (chartData.length === 0) {
    return (
      <Card
        title="Seleccion del Numero de Clusters"
        description="Compara la relacion entre k y el Silhouette usando modelos KMeans y GMM del historial local."
      >
        <p className="muted">
          No hay datos suficientes para construir la curva. Entrena modelos
          KMeans o GMM con metricas disponibles en el historial local.
        </p>
      </Card>
    );
  }

  return (
    <Card
      title="Seleccion del Numero de Clusters"
      description="Visualizacion tipo linea construida con el historial local de modelos entrenados."
    >
      <div className="metric-helper-box">
        <strong>Que representa esta grafica</strong>
        <p>
          Los picos aparecen al comparar varios modelos entrenados con
          diferentes valores de k. No representan clusters individuales.
        </p>
      </div>

      <div className="pdf-line-chart-shell">
        <div className="pdf-line-chart-frame">
          <ResponsiveContainer width="100%" height={260}>
            <LineChart
              data={chartData}
              margin={{ top: 14, right: 18, bottom: 28, left: 6 }}
            >
              <YAxis
                dataKey="silhouette"
                tick={false}
                axisLine={{ stroke: "#9ca3af", strokeWidth: 1 }}
                tickLine={false}
                width={22}
                label={{
                  value: "Silueta / Inercia",
                  angle: -90,
                  position: "insideLeft",
                  offset: -2,
                  style: {
                    fill: "#6b7280",
                    fontSize: 12,
                  },
                }}
              />
              <XAxis
                dataKey="kLabel"
                tick={false}
                axisLine={{ stroke: "#9ca3af", strokeWidth: 1 }}
                tickLine={false}
                label={{
                  value: kRangeLabel,
                  position: "insideBottom",
                  offset: -8,
                  style: {
                    fill: "#6b7280",
                    fontSize: 12,
                  },
                }}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line
                type="linear"
                dataKey="silhouette"
                stroke="#4b5563"
                strokeWidth={2}
                dot={
                  chartData.length === 1
                    ? { r: 6, fill: "#4b5563", stroke: "#4b5563" }
                    : false
                }
                activeDot={{ r: 4, fill: "#4b5563", stroke: "#4b5563" }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {chartData.length === 1 && (
        <p className="line-chart-hint">
          Solo existe un modelo con k = {chartData[0].k}. Para ver una curva
          con picos como la del PDF, necesitas entrenar varios modelos con
          diferentes valores de k, por ejemplo 2, 3, 4, 5 y 6.
        </p>
      )}
    </Card>
  );
}

export default MetricsComparisonChart;
