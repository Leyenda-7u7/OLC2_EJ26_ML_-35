import { useMemo, useState } from "react";

import Card from "../ui/Card";
import Button from "../ui/Button";
import Alert from "../ui/Alert";
import Select from "../ui/Select";
import Input from "../ui/Input";
import Badge from "../ui/Badge";

import { DATASET_TYPES } from "../../utils/constants";
import { classifyRecord } from "../../api/classificationApi";
import { useModelStore } from "../../hooks/useModelStore";

const FREELANCER_INITIAL_VALUES = {
  proyectos_completados: 40,
  ingresos_totales: 50000,
  tarifa_hora_promedio: 80,
  anios_experiencia: 5,
  tiempo_respuesta_horas: 8,
  tasa_finalizacion: 90,
  calificacion_promedio: 4.5,
  categoria_principal: "Desarrollo de Software",
  clientes_recurrentes: 6,
  horas_trabajadas_mes: 120,
};

const REVIEW_INITIAL_VALUES = {
  "texto_reseña": "Excelente comunicación, buena calidad y entrega rápida.",
};

function ClassificationResult({ result }) {
  if (!result) {
    return (
      <Card
        title="Resultado de clasificación"
        description="Cuando clasifiques un registro, aquí aparecerá el segmento asignado."
      >
        <p className="muted">Todavía no se ha clasificado ningún registro.</p>
      </Card>
    );
  }

  return (
    <Card
      title="Registro clasificado"
      description="Resultado obtenido usando el modelo previamente entrenado."
    >
      <div className="classification-result">
        <div className="classification-cluster">
          <span>Cluster asignado</span>
          <strong>{result.cluster}</strong>
        </div>

        <div className="classification-segment-name">
          <span>Segmento interpretado</span>
          <strong>{result.segment_name || `Segmento ${result.cluster}`}</strong>
        </div>

        <div className="badges-row">
          <Badge variant="success">{result.dataset_type}</Badge>
          <Badge>{result.model_id}</Badge>
        </div>

        {result.description && (
          <div className="classification-description">
            <h4>Descripción interpretativa</h4>
            <p>{result.description}</p>
          </div>
        )}
      </div>
    </Card>
  );
}

function ClassificationForm() {
  const { lastModel, models } = useModelStore();

  const [datasetType, setDatasetType] = useState(
    lastModel?.dataset_type || "freelancers"
  );

  const [modelId, setModelId] = useState(lastModel?.model_id || "");

  const [freelancerValues, setFreelancerValues] = useState(
    FREELANCER_INITIAL_VALUES
  );

  const [reviewValues, setReviewValues] = useState(REVIEW_INITIAL_VALUES);

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const filteredModels = useMemo(() => {
    return models.filter((model) => model.dataset_type === datasetType);
  }, [models, datasetType]);

  const isFreelancer = datasetType === "freelancers";
  const isReview = datasetType === "reviews";

  const hasModelsForDataset = filteredModels.length > 0;

  const handleDatasetChange = (event) => {
    const selectedDataset = event.target.value;

    setDatasetType(selectedDataset);

    const firstMatchingModel = models.find(
      (model) => model.dataset_type === selectedDataset
    );

    setModelId(firstMatchingModel?.model_id || "");
    setResult(null);

    setAlert({
      type: firstMatchingModel ? "info" : "error",
      message: firstMatchingModel
        ? "Modelo encontrado para el tipo de registro seleccionado."
        : "No hay modelos entrenados en el historial para este tipo de registro. Puedes entrenar uno primero o pegar manualmente un model_id válido.",
    });
  };

  const handleModelChange = (event) => {
    setModelId(event.target.value);
    setResult(null);
  };

  const handleFreelancerChange = (event) => {
    const { name, value, type } = event.target;

    setFreelancerValues((current) => ({
      ...current,
      [name]: type === "number" ? Number(value) : value,
    }));
  };

  const handleReviewChange = (event) => {
    const { name, value } = event.target;

    setReviewValues((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const buildPayload = () => {
    return {
      model_id: modelId,
      dataset_type: datasetType,
      values: isFreelancer ? freelancerValues : reviewValues,
    };
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!modelId.trim()) {
      setAlert({
        type: "error",
        message: "Debes ingresar o seleccionar un model_id.",
      });
      return;
    }

    if (isReview && !reviewValues["texto_reseña"].trim()) {
      setAlert({
        type: "error",
        message: "Debes ingresar el texto de la reseña.",
      });
      return;
    }

    try {
      setLoading(true);

      setAlert({
        type: "info",
        message: "Asignando segmento al registro...",
      });

      const response = await classifyRecord(buildPayload());

      setResult(response);

      setAlert({
        type: "success",
        message: "Registro clasificado correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Ocurrió un error al clasificar el registro.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid-2">
      <Card
        title="Nuevo registro"
        description="Ingresa los datos del freelancer o la reseña que deseas clasificar."
      >
        <form className="classification-form" onSubmit={handleSubmit}>
          <div className="form-grid-2">
            <Select
              label="Tipo de registro"
              value={datasetType}
              onChange={handleDatasetChange}
              options={DATASET_TYPES}
            />

            <label className="form-control">
              <span>Modelo entrenado</span>

              <select value={modelId} onChange={handleModelChange}>
                <option value="">Selecciona un modelo</option>

                {filteredModels.map((model) => (
                  <option key={model.model_id} value={model.model_id}>
                    {model.algorithm} · {model.filename}
                  </option>
                ))}
              </select>
            </label>
          </div>

          {!hasModelsForDataset && (
            <Alert
              type="error"
              message="Esta vista requiere al menos un modelo entrenado para el tipo de registro seleccionado. Puedes entrenarlo en Configuración y entrenamiento."
            />
          )}

          <Input
            label="Model ID"
            value={modelId}
            onChange={(event) => setModelId(event.target.value)}
            placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          />

          {isFreelancer && (
            <>
              <div className="section-subtitle">
                <h4>Datos del freelancer</h4>
                <p>
                  Campos alineados con freelancers_dev.csv, excluyendo
                  freelancer_id.
                </p>
              </div>

              <div className="form-grid-2">
                <Input
                  label="Proyectos completados"
                  name="proyectos_completados"
                  type="number"
                  value={freelancerValues.proyectos_completados}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Ingresos totales"
                  name="ingresos_totales"
                  type="number"
                  value={freelancerValues.ingresos_totales}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Tarifa por hora promedio"
                  name="tarifa_hora_promedio"
                  type="number"
                  value={freelancerValues.tarifa_hora_promedio}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Años de experiencia"
                  name="anios_experiencia"
                  type="number"
                  value={freelancerValues.anios_experiencia}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Tiempo de respuesta (horas)"
                  name="tiempo_respuesta_horas"
                  type="number"
                  value={freelancerValues.tiempo_respuesta_horas}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Tasa de finalización"
                  name="tasa_finalizacion"
                  type="number"
                  value={freelancerValues.tasa_finalizacion}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Calificación promedio"
                  name="calificacion_promedio"
                  type="number"
                  value={freelancerValues.calificacion_promedio}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Categoría principal"
                  name="categoria_principal"
                  value={freelancerValues.categoria_principal}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Clientes recurrentes"
                  name="clientes_recurrentes"
                  type="number"
                  value={freelancerValues.clientes_recurrentes}
                  onChange={handleFreelancerChange}
                />

                <Input
                  label="Horas trabajadas al mes"
                  name="horas_trabajadas_mes"
                  type="number"
                  value={freelancerValues.horas_trabajadas_mes}
                  onChange={handleFreelancerChange}
                />
              </div>
            </>
          )}

          {isReview && (
            <>
              <div className="section-subtitle">
                <h4>Texto de la reseña</h4>
                <p>
                  La reseña nueva se transformará usando el mismo vectorizador
                  ajustado durante el entrenamiento.
                </p>
              </div>

              <label className="form-control">
                <span>Contenido de la reseña</span>

                <textarea
                  name="texto_reseña"
                  value={reviewValues["texto_reseña"]}
                  onChange={handleReviewChange}
                  rows={6}
                  placeholder="Escribe una reseña para clasificar..."
                />
              </label>
            </>
          )}

          <Alert type={alert.type} message={alert.message} />

          <div className="actions-row">
            <Button type="submit" disabled={loading || !modelId.trim()}>
              {loading ? "Asignando..." : "Asignar segmento"}
            </Button>
          </div>
        </form>
      </Card>

      <ClassificationResult result={result} />
    </div>
  );
}

export default ClassificationForm;