function DataPreviewTable({ data }) {
  if (!data || !data.preview || data.preview.length === 0) {
    return (
      <p className="muted">
        No hay datos para mostrar todavía.
      </p>
    );
  }

  return (
    <div className="table-wrapper">
      <div className="table-summary">
        <span>
          Filas: <strong>{data.total_rows}</strong>
        </span>

        <span>
          Columnas: <strong>{data.total_columns}</strong>
        </span>
      </div>

      <table className="data-table">
        <thead>
          <tr>
            {data.columns.map((column) => (
              <th key={column}>{column}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.preview.map((row, index) => (
            <tr key={index}>
              {data.columns.map((column) => (
                <td key={column}>
                  {row[column] === null || row[column] === undefined
                    ? "-"
                    : String(row[column])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataPreviewTable;