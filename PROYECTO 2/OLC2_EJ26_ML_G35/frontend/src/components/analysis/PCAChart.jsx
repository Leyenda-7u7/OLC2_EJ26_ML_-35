import {
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

import Card from "../ui/Card";

const CLUSTER_COLORS = [
  "#2563eb",
  "#16a34a",
  "#dc2626",
  "#9333ea",
  "#f59e0b",
  "#0891b2",
  "#be123c",
];

function groupPointsByCluster(points) {
  const groups = {};

  points.forEach((point) => {
    const cluster = String(point.cluster);

    if (!groups[cluster]) {
      groups[cluster] = [];
    }

    groups[cluster].push({
      pc1: point.pc1,
      pc2: point.pc2,
      id: point.id,
      cluster: point.cluster,
    });
  });

  return groups;
}

function getClusterColor(cluster) {
  const clusterNumber = Number(cluster);

  if (clusterNumber === -1) {
    return "#64748b";
  }

  return CLUSTER_COLORS[
    Math.abs(clusterNumber) % CLUSTER_COLORS.length
  ];
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload || payload.length === 0) {
    return null;
  }

  const point = payload[0].payload;

  return (
    <div className="chart-tooltip">
      <strong>Cluster {point.cluster}</strong>
      <p>ID: {point.id ?? "N/A"}</p>
      <p>PC1: {Number(point.pc1).toFixed(4)}</p>
      <p>PC2: {Number(point.pc2).toFixed(4)}</p>
    </div>
  );
}

function PCAChart({ data }) {
  if (!data || !data.points || data.points.length === 0) {
    return (
      <Card title="Visualización PCA/SVD">
        <p className="muted">No hay puntos para graficar.</p>
      </Card>
    );
  }

  const groupedPoints = groupPointsByCluster(data.points);
  const sortedClusters = Object.entries(groupedPoints).sort(
    ([clusterA], [clusterB]) => Number(clusterA) - Number(clusterB)
  );

  return (
    <Card
      title="Visualización PCA/SVD"
      description="Representación en 2 dimensiones de los registros agrupados por cluster."
    >
      <div className="chart-meta">
        <span>
          Dataset: <strong>{data.dataset_type}</strong>
        </span>

        <span>
          Varianza total explicada:{" "}
          <strong>
            {Number(data.total_explained_variance || 0).toFixed(4)}
          </strong>
        </span>
      </div>

      <div className="chart-box">
        <ResponsiveContainer width="100%" height={380}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="pc1"
              name="PC1"
              type="number"
              tick={{ fontSize: 12 }}
            />
            <YAxis
              dataKey="pc2"
              name="PC2"
              type="number"
              tick={{ fontSize: 12 }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend />

            {sortedClusters.map(([cluster, points]) => (
              <Scatter
                key={cluster}
                name={`Cluster ${cluster}`}
                data={points}
                fill={getClusterColor(cluster)}
              />
            ))}
          </ScatterChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

export default PCAChart;
