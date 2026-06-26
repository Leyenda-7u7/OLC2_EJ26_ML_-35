import Card from "../ui/Card";

function MetricsExplanation() {
  return (
    <Card
      title="Interpretación de métricas"
      description="Guía rápida para explicar los resultados durante la defensa."
    >
      <div className="explanation-list">
        <div className="explanation-item">
          <h4>Silhouette Score</h4>
          <p>
            Evalúa qué tan parecido es un registro a su propio cluster en
            comparación con otros clusters. Su valor suele estar entre -1 y 1.
            Mientras más cercano a 1, mejor separación existe.
          </p>
        </div>

        <div className="explanation-item">
          <h4>Davies-Bouldin Score</h4>
          <p>
            Evalúa la relación entre compactación interna y separación entre
            clusters. En esta métrica, un valor menor normalmente indica mejor
            agrupamiento.
          </p>
        </div>

        <div className="explanation-item">
          <h4>Calinski-Harabasz Score</h4>
          <p>
            Compara la dispersión entre clusters contra la dispersión dentro de
            cada cluster. Mientras más alto sea, mejor suele ser la separación.
            Es útil principalmente para comparar varias configuraciones.
          </p>
        </div>

        <div className="explanation-item">
          <h4>Validación práctica</h4>
          <p>
            Además de las métricas, se debe revisar si los segmentos tienen una
            interpretación útil: por ejemplo, freelancers premium, perfiles de
            bajo costo, reseñas positivas, reseñas con problemas de entrega o
            comunicación.
          </p>
        </div>
      </div>
    </Card>
  );
}

export default MetricsExplanation;