import { useMemo, useState } from "react";

import Card from "../ui/Card";
import Button from "../ui/Button";
import Alert from "../ui/Alert";
import Badge from "../ui/Badge";
import Input from "../ui/Input";

import { useModelStore } from "../../hooks/useModelStore";
import { getClusterProfiles } from "../../api/analysisApi";

import {
  downloadCsvReport,
  downloadPdfReport,
  triggerFileDownload,
} from "../../api/exportApi";

const EXPORT_OPTIONS = [
  {
    key: "freelancersDataset",
    label: "Dataset de freelancers segmentado",
    description: "Descarga el CSV segmentado del modelo de freelancers.",
  },
  {
    key: "reviewsDataset",
    label: "Dataset de resenas segmentado",
    description: "Descarga el CSV segmentado del modelo de resenas.",
  },
  {
    key: "segmentSummary",
    label: "Resumen estadistico por segmento",
    description: "Genera un CSV desde el endpoint de perfiles disponible.",
  },
  {
    key: "evaluationMetrics",
    label: "Metricas de evaluacion del modelo",
    description: "Genera un CSV desde el historial local del frontend.",
  },
  {
    key: "visualReport",
    label: "Reporte grafico generado en Interpretacion de Segmentos",
    description: "Descarga el PDF del reporte disponible para cada modelo.",
  },
];

function escapeCsvValue(value) {
  if (value === null || value === undefined) {
    return "";
  }

  return `"${String(value).replace(/"/g, '""')}"`;
}

function rowsToCsv(rows) {
  if (!rows || rows.length === 0) {
    return "";
  }

  const headers = Object.keys(rows[0]);
  const headerRow = headers.map(escapeCsvValue).join(",");
  const dataRows = rows.map((row) =>
    headers.map((header) => escapeCsvValue(row[header])).join(",")
  );

  return [headerRow, ...dataRows].join("\n");
}

function downloadGeneratedCsv(rows, filename) {
  const csvBlob = new Blob([rowsToCsv(rows)], {
    type: "text/csv;charset=utf-8;",
  });

  triggerFileDownload(csvBlob, filename);
}

function buildSegmentSummaryRows(profileData, modelId) {
  const rows = [];

  (profileData?.profiles || []).forEach((profile) => {
    const numericSummary = profile.summary?.numeric || {};
    const categoricalSummary = profile.summary?.categorical || {};

    Object.entries(numericSummary).forEach(([column, values]) => {
      rows.push({
        model_id: modelId,
        dataset_type: profileData.dataset_type,
        cluster: profile.cluster,
        total_registros: profile.count,
        tipo_resumen: "numeric",
        variable: column,
        promedio: values.mean,
        minimo: values.min,
        maximo: values.max,
        valor_representativo: "",
      });
    });

    Object.entries(categoricalSummary).forEach(([column, value]) => {
      rows.push({
        model_id: modelId,
        dataset_type: profileData.dataset_type,
        cluster: profile.cluster,
        total_registros: profile.count,
        tipo_resumen: "categorical",
        variable: column,
        promedio: "",
        minimo: "",
        maximo: "",
        valor_representativo: value,
      });
    });

    if (
      Object.keys(numericSummary).length === 0 &&
      Object.keys(categoricalSummary).length === 0
    ) {
      rows.push({
        model_id: modelId,
        dataset_type: profileData.dataset_type,
        cluster: profile.cluster,
        total_registros: profile.count,
        tipo_resumen: "empty",
        variable: "",
        promedio: "",
        minimo: "",
        maximo: "",
        valor_representativo: "",
      });
    }
  });

  return rows;
}

function buildMetricsRows(models) {
  return models.map((model) => ({
    model_id: model.model_id,
    dataset_type: model.dataset_type,
    algorithm: model.algorithm,
    filename: model.filename,
    clusters_found: model.clusters_found,
    noise_points: model.noise_points,
    silhouette_score: model.metrics?.silhouette_score ?? "",
    davies_bouldin_score: model.metrics?.davies_bouldin_score ?? "",
    calinski_harabasz_score: model.metrics?.calinski_harabasz_score ?? "",
  }));
}

function ExportButtons() {
  const { lastModel, models } = useModelStore();

  const freelancerModels = useMemo(
    () => models.filter((model) => model.dataset_type === "freelancers"),
    [models]
  );

  const reviewsModels = useMemo(
    () => models.filter((model) => model.dataset_type === "reviews"),
    [models]
  );

  const [freelancerModelId, setFreelancerModelId] = useState(
    lastModel?.dataset_type === "freelancers" ? lastModel.model_id : ""
  );
  const [reviewsModelId, setReviewsModelId] = useState(
    lastModel?.dataset_type === "reviews" ? lastModel.model_id : ""
  );
  const [selection, setSelection] = useState({
    freelancersDataset: false,
    reviewsDataset: false,
    segmentSummary: false,
    evaluationMetrics: false,
    visualReport: false,
  });
  const [loading, setLoading] = useState(false);
  const [generatedFiles, setGeneratedFiles] = useState([]);

  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const selectedFreelancerModel = useMemo(() => {
    return (
      models.find((model) => model.model_id === freelancerModelId) || null
    );
  }, [models, freelancerModelId]);

  const selectedReviewsModel = useMemo(() => {
    return models.find((model) => model.model_id === reviewsModelId) || null;
  }, [models, reviewsModelId]);

  const hasSelectedItems = Object.values(selection).some(Boolean);

  const toggleSelection = (key) => {
    setSelection((currentSelection) => ({
      ...currentSelection,
      [key]: !currentSelection[key],
    }));
    setGeneratedFiles([]);
  };

  const resetMessages = () => {
    setAlert({
      type: "",
      message: "",
    });
    setGeneratedFiles([]);
  };

  const getMetricModels = () => {
    const uniqueModels = new Map();

    [selectedFreelancerModel, selectedReviewsModel]
      .filter(Boolean)
      .forEach((model) => {
        uniqueModels.set(model.model_id, model);
      });

    return Array.from(uniqueModels.values());
  };

  const validateSelection = () => {
    if (!hasSelectedItems) {
      return "Debes seleccionar al menos un elemento para exportar.";
    }

    if (selection.freelancersDataset && !freelancerModelId.trim()) {
      return "El dataset de freelancers segmentado requiere un modelo de freelancers.";
    }

    if (selection.reviewsDataset && !reviewsModelId.trim()) {
      return "El dataset de resenas segmentado requiere un modelo de resenas.";
    }

    if (
      selection.segmentSummary &&
      !freelancerModelId.trim() &&
      !reviewsModelId.trim()
    ) {
      return "El resumen por segmento requiere al menos un modelo seleccionado.";
    }

    if (selection.evaluationMetrics && getMetricModels().length === 0) {
      return "Las metricas de evaluacion requieren al menos un modelo presente en el historial local.";
    }

    if (
      selection.visualReport &&
      !freelancerModelId.trim() &&
      !reviewsModelId.trim()
    ) {
      return "El reporte grafico requiere al menos un modelo seleccionado.";
    }

    return null;
  };

  const handleExportSelection = async () => {
    const validationError = validateSelection();

    if (validationError) {
      setAlert({
        type: "error",
        message: validationError,
      });
      return;
    }

    try {
      setLoading(true);
      setGeneratedFiles([]);

      setAlert({
        type: "info",
        message: "Generando archivos seleccionados...",
      });

      const createdFiles = [];

      if (selection.freelancersDataset) {
        const freelancerBlob = await downloadCsvReport(freelancerModelId);
        const freelancerFilename = "freelancers_segmentado.csv";

        triggerFileDownload(freelancerBlob, freelancerFilename);
        createdFiles.push(freelancerFilename);
      }

      if (selection.reviewsDataset) {
        const reviewsBlob = await downloadCsvReport(reviewsModelId);
        const reviewsFilename = "resenas_segmentado.csv";

        triggerFileDownload(reviewsBlob, reviewsFilename);
        createdFiles.push(reviewsFilename);
      }

      if (selection.segmentSummary) {
        const summaryModelId =
          freelancerModelId.trim() || reviewsModelId.trim();
        const profileData = await getClusterProfiles(summaryModelId);
        const summaryRows = buildSegmentSummaryRows(
          profileData,
          summaryModelId
        );
        const summaryFilename = "resumen_segmentos.csv";

        downloadGeneratedCsv(summaryRows, summaryFilename);
        createdFiles.push(summaryFilename);
      }

      if (selection.evaluationMetrics) {
        const metricsFilename = "metricas_evaluacion.csv";
        const metricRows = buildMetricsRows(getMetricModels());

        downloadGeneratedCsv(metricRows, metricsFilename);
        createdFiles.push(metricsFilename);
      }

      if (selection.visualReport && freelancerModelId.trim()) {
        const freelancerPdfBlob = await downloadPdfReport(freelancerModelId);
        const freelancerPdfFilename = "reporte_visual_freelancers.pdf";

        triggerFileDownload(freelancerPdfBlob, freelancerPdfFilename);
        createdFiles.push(freelancerPdfFilename);
      }

      if (selection.visualReport && reviewsModelId.trim()) {
        const reviewsPdfBlob = await downloadPdfReport(reviewsModelId);
        const reviewsPdfFilename = "reporte_visual_resenas.pdf";

        triggerFileDownload(reviewsPdfBlob, reviewsPdfFilename);
        createdFiles.push(reviewsPdfFilename);
      }

      setGeneratedFiles(createdFiles);
      setAlert({
        type: "success",
        message: `Archivos generados: ${createdFiles.join(", ")}`,
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Ocurrio un error durante la exportacion. Verifica los modelos seleccionados.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="export-layout">
      <Card
        title="Elementos a Exportar"
        description="Selecciona que artefactos deseas descargar o generar desde el frontend."
      >
        <div className="export-form">
          <div className="export-option-list">
            {EXPORT_OPTIONS.map((option) => (
              <label key={option.key} className="export-option-item">
                <div className="checkbox-row">
                  <input
                    type="checkbox"
                    checked={selection[option.key]}
                    onChange={() => toggleSelection(option.key)}
                  />

                  <div>
                    <strong>{option.label}</strong>
                    <p>{option.description}</p>
                  </div>
                </div>
              </label>
            ))}
          </div>
        </div>
      </Card>

      <Card
        title="Configuracion de Exportacion"
        description="Asocia los elementos a los modelos disponibles y al formato generado."
      >
        <div className="export-actions">
          <div className="export-model-grid">
            <div className="export-panel-card">
              <label className="form-control">
                <span>Modelo de freelancers</span>
                <select
                  value={freelancerModelId}
                  onChange={(event) => {
                    setFreelancerModelId(event.target.value);
                    resetMessages();
                  }}
                >
                  <option value="">Selecciona un modelo</option>

                  {freelancerModels.map((model) => (
                    <option key={model.model_id} value={model.model_id}>
                      {model.algorithm} · {model.filename}
                    </option>
                  ))}
                </select>
              </label>

              <Input
                label="Model ID freelancers"
                value={freelancerModelId}
                onChange={(event) => {
                  setFreelancerModelId(event.target.value);
                  resetMessages();
                }}
                placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
              />
            </div>

            <div className="export-panel-card">
              <label className="form-control">
                <span>Modelo de resenas</span>
                <select
                  value={reviewsModelId}
                  onChange={(event) => {
                    setReviewsModelId(event.target.value);
                    resetMessages();
                  }}
                >
                  <option value="">Selecciona un modelo</option>

                  {reviewsModels.map((model) => (
                    <option key={model.model_id} value={model.model_id}>
                      {model.algorithm} · {model.filename}
                    </option>
                  ))}
                </select>
              </label>

              <Input
                label="Model ID resenas"
                value={reviewsModelId}
                onChange={(event) => {
                  setReviewsModelId(event.target.value);
                  resetMessages();
                }}
                placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
              />
            </div>
          </div>

          <div className="export-model-grid">
            {selectedFreelancerModel && (
              <div className="export-model-summary">
                <span>Modelo freelancers</span>
                <strong>{selectedFreelancerModel.model_id}</strong>

                <div className="badges-row">
                  <Badge variant="success">
                    {selectedFreelancerModel.dataset_type}
                  </Badge>
                  <Badge>{selectedFreelancerModel.algorithm}</Badge>
                  <Badge>{selectedFreelancerModel.filename}</Badge>
                </div>
              </div>
            )}

            {selectedReviewsModel && (
              <div className="export-model-summary">
                <span>Modelo resenas</span>
                <strong>{selectedReviewsModel.model_id}</strong>

                <div className="badges-row">
                  <Badge variant="success">
                    {selectedReviewsModel.dataset_type}
                  </Badge>
                  <Badge>{selectedReviewsModel.algorithm}</Badge>
                  <Badge>{selectedReviewsModel.filename}</Badge>
                </div>
              </div>
            )}
          </div>

          <div className="export-format-box">
            <h4>Formato</h4>
            <p>
              CSV: usa endpoints existentes para datasets segmentados y genera
              archivos locales para resumenes y metricas.
            </p>
            <p>
              PDF: usa el endpoint <code>/export/pdf/{`{model_id}`}</code> para
              cada modelo seleccionado.
            </p>
          </div>

          <div className="actions-row">
            <Button
              onClick={handleExportSelection}
              disabled={loading || !hasSelectedItems}
            >
              {loading ? "Exportando..." : "Exportar Seleccion"}
            </Button>
          </div>

          <Alert type={alert.type} message={alert.message} />

          {generatedFiles.length > 0 && (
            <div className="export-confirmation-box">
              <strong>Archivos generados</strong>
              <p>{generatedFiles.join(", ")}</p>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}

export default ExportButtons;
