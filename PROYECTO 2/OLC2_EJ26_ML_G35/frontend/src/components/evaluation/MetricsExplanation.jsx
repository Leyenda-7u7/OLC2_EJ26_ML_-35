import Card from "../ui/Card";

function getSilhouetteMessage(value) {
  if (value === null || value === undefined) {
    return "No fue posible calcular el Silhouette del modelo seleccionado.";
  }

  if (value >= 0.7) {
    return "Los segmentos presentan una separacion muy buena.";
  }

  if (value >= 0.5) {
    return "Los segmentos presentan una buena separacion.";
  }

  if (value >= 0.25) {
    return "Los segmentos presentan una separacion moderada.";
  }

  return "Los segmentos presentan una separacion debil.";
}

function MetricsExplanation({ model }) {
  const silhouette = model?.metrics?.silhouette_score;

  return (
    <Card
      title="Interpretacion"
      description="Lectura rapida del modelo seleccionado basada en el Silhouette Score."
    >
      <div className="interpretation-box">
        <div className="interpretation-value">
          <span>Silhouette del modelo</span>
          <strong>
            {silhouette === null || silhouette === undefined
              ? "No disponible"
              : Number(silhouette).toFixed(4)}
          </strong>
        </div>

        <p className="interpretation-message">
          {getSilhouetteMessage(silhouette)}
        </p>

        <p className="interpretation-note">
          Esta lectura complementa las metricas actuales y sirve como resumen
          rapido para la seleccion final del modelo.
        </p>
      </div>
    </Card>
  );
}

export default MetricsExplanation;
