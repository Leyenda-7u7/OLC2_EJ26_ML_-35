import Card from "../ui/Card";

function getOrderedColumns(rows) {
  if (!rows || rows.length === 0) {
    return [];
  }

  const columns = Object.keys(rows[0]);

  const firstColumns = [
    "freelancer_cluster",
    "review_cluster",
  ];

  const orderedFirst = firstColumns.filter((column) =>
    columns.includes(column)
  );

  const remainingColumns = columns.filter(
    (column) => !orderedFirst.includes(column)
  );

  return [...orderedFirst, ...remainingColumns];
}

function formatCellValue(value) {
  if (value === null || value === undefined) {
    return "-";
  }

  if (typeof value === "number") {
    return Number.isInteger(value) ? value : value.toFixed(2);
  }

  const numericValue = Number(value);

  if (!Number.isNaN(numericValue) && String(value).trim() !== "") {
    return Number.isInteger(numericValue)
      ? numericValue
      : numericValue.toFixed(2);
  }

  return String(value);
}

function formatColumnName(column) {
  if (column === "freelancer_cluster") {
    return "Segmento freelancer";
  }

  if (column === "review_cluster") {
    return "Segmento reseña";
  }

  return `Reseña cluster ${column}`;
}

function SimpleTable({ title, rows, isPercentage = false }) {
  if (!rows || rows.length === 0) {
    return (
      <div>
        <h4>{title}</h4>
        <p className="muted">No hay datos para mostrar.</p>
      </div>
    );
  }

  const columns = getOrderedColumns(rows);

  return (
    <div className="profile-table-wrapper">
      <h4>{title}</h4>

      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{formatColumnName(column)}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => {
                const value = formatCellValue(row[column]);

                return (
                  <td key={column}>
                    {isPercentage && column !== "freelancer_cluster"
                      ? `${value}%`
                      : value}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function CrossSegmentTable({ data }) {
  if (!data) {
    return (
      <Card
        title="Tabla cruzada"
        description="Cruza los clusters de freelancers con los clusters de reseñas usando freelancer_id."
      >
        <p className="muted">
          Ingresa ambos model_id y genera la tabla cruzada.
        </p>
      </Card>
    );
  }

  return (
    <Card
      title="Tabla cruzada de segmentos"
      description={`Registros cruzados: ${data.merged_rows ?? 0}`}
    >
      {data.message && <p className="muted">{data.message}</p>}

      <div className="profiles-list">
        <SimpleTable title="Conteos absolutos" rows={data.counts} />

        <SimpleTable
          title="Porcentajes por fila"
          rows={data.percentages}
          isPercentage
        />
      </div>
    </Card>
  );
}

export default CrossSegmentTable;