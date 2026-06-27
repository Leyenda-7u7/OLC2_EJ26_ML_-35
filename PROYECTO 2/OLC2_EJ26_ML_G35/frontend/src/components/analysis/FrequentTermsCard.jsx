import Card from "../ui/Card";

function extractTopTerms(data) {
  if (!data?.profiles || data.dataset_type !== "reviews") {
    return [];
  }

  const aggregatedTerms = new Map();

  data.profiles.forEach((profile) => {
    const possibleTerms = [
      profile?.top_terms,
      profile?.summary?.top_terms,
      profile?.summary?.terms,
      profile?.summary?.frequent_terms,
    ].find((value) => Array.isArray(value));

    if (!possibleTerms) {
      return;
    }

    possibleTerms.forEach((item) => {
      const term = typeof item === "string" ? item : item?.term;
      const rawWeight =
        typeof item === "object" ? item?.weight ?? item?.score : 1;
      const weight = Number(rawWeight);

      if (!term) {
        return;
      }

      const normalizedTerm = String(term).trim();
      const safeWeight =
        Number.isFinite(weight) && weight > 0 ? weight : 1;

      const currentTerm = aggregatedTerms.get(normalizedTerm);

      if (!currentTerm) {
        aggregatedTerms.set(normalizedTerm, {
          term: normalizedTerm,
          weight: safeWeight,
        });
        return;
      }

      aggregatedTerms.set(normalizedTerm, {
        term: normalizedTerm,
        weight: currentTerm.weight + safeWeight,
      });
    });
  });

  return Array.from(aggregatedTerms.values()).sort(
    (termA, termB) => termB.weight - termA.weight
  );
}

function getTermFontSize(weight, minWeight, maxWeight) {
  if (maxWeight <= minWeight) {
    return 18;
  }

  const ratio = (weight - minWeight) / (maxWeight - minWeight);

  return 14 + ratio * 18;
}

function FrequentTermsCard({ data }) {
  if (!data || data.dataset_type !== "reviews") {
    return null;
  }

  const terms = extractTopTerms(data);
  const maxWeight = terms[0]?.weight ?? 1;
  const minWeight = terms[terms.length - 1]?.weight ?? 1;

  return (
    <Card
      title="Terminos frecuentes"
      description="Vista visual para modelos de resenas usando la informacion disponible en frontend."
    >
      {terms.length === 0 ? (
        <div className="terms-fallback">
          <p className="muted">
            No hay terminos frecuentes disponibles para este modelo.
          </p>
          <p className="muted">
            El backend actual no expone top_terms en el endpoint de perfiles,
            asi que esta seccion queda en modo informativo.
          </p>
        </div>
      ) : (
        <div className="word-cloud">
          {terms.slice(0, 24).map((term) => (
            <span
              key={term.term}
              className="word-cloud-item"
              style={{
                fontSize: `${getTermFontSize(
                  term.weight,
                  minWeight,
                  maxWeight
                )}px`,
              }}
            >
              {term.term}
            </span>
          ))}
        </div>
      )}
    </Card>
  );
}

export default FrequentTermsCard;
