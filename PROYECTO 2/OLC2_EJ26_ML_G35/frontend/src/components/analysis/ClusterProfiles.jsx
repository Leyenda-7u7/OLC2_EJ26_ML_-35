import Card from "../ui/Card";
import Badge from "../ui/Badge";

function renderNumericSummary(numericSummary) {
  if (!numericSummary || Object.keys(numericSummary).length === 0) {
    return <p className="muted">No hay resumen numérico disponible.</p>;
  }

  return (
    <div className="profile-table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Variable</th>
            <th>Promedio</th>
            <th>Mínimo</th>
            <th>Máximo</th>
          </tr>
        </thead>

        <tbody>
          {Object.entries(numericSummary).map(([column, values]) => (
            <tr key={column}>
              <td>{column}</td>
              <td>{Number(values.mean).toFixed(3)}</td>
              <td>{Number(values.min).toFixed(3)}</td>
              <td>{Number(values.max).toFixed(3)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function renderCategoricalSummary(categoricalSummary) {
  if (!categoricalSummary || Object.keys(categoricalSummary).length === 0) {
    return null;
  }

  return (
    <div className="categorical-list">
      {Object.entries(categoricalSummary).map(([column, value]) => (
        <div key={column} className="categorical-item">
          <span>{column}</span>
          <strong>{String(value)}</strong>
        </div>
      ))}
    </div>
  );
}

function renderTopTerms(topTerms) {
  if (!topTerms || topTerms.length === 0) {
    return null;
  }

  return (
    <div className="top-terms">
      <h4>Términos relevantes</h4>

      <div className="badges-row">
        {topTerms.map((item) => (
          <Badge key={item.term}>
            {item.term} · {Number(item.weight).toFixed(3)}
          </Badge>
        ))}
      </div>
    </div>
  );
}

function ClusterProfiles({ data }) {
  if (!data || !data.profiles || data.profiles.length === 0) {
    return (
      <Card title="Perfiles de segmentos">
        <p className="muted">No hay perfiles para mostrar.</p>
      </Card>
    );
  }

  return (
    <Card
      title="Perfiles de segmentos"
      description="Resumen interpretativo de cada cluster encontrado por el modelo."
    >
      <div className="profiles-list">
        {data.profiles.map((profile) => {
          const summary = profile.summary || {};
          const clusterName =
            summary.cluster_name || `Segmento ${profile.cluster}`;

          return (
            <div key={profile.cluster} className="profile-card">
              <div className="profile-header">
                <div>
                  <h3>{clusterName}</h3>
                  <p>Cluster {profile.cluster}</p>
                </div>

                <Badge variant="success">{profile.count} registros</Badge>
              </div>

              {renderTopTerms(summary.top_terms)}
              {renderCategoricalSummary(summary.categorical)}
              {renderNumericSummary(summary.numeric)}
            </div>
          );
        })}
      </div>
    </Card>
  );
}

export default ClusterProfiles;