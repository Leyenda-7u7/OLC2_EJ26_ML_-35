import { useMemo, useState } from "react";
import { FileDown, FileText } from "lucide-react";

import Card from "../ui/Card";
import Button from "../ui/Button";
import Alert from "../ui/Alert";
import Badge from "../ui/Badge";
import Input from "../ui/Input";

import { useModelStore } from "../../hooks/useModelStore";

import {
  downloadCsvReport,
  downloadPdfReport,
  triggerFileDownload,
} from "../../api/exportApi";

function ExportButtons() {
  const { lastModel, models } = useModelStore();

  const [modelId, setModelId] = useState(lastModel?.model_id || "");
  const [loading, setLoading] = useState(false);

  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const selectedModel = useMemo(() => {
    return models.find((model) => model.model_id === modelId) || null;
  }, [models, modelId]);

  const handleModelChange = (event) => {
    setModelId(event.target.value);
    setAlert({
      type: "",
      message: "",
    });
  };

  const validateModelId = () => {
    if (!modelId.trim()) {
      setAlert({
        type: "error",
        message: "Debes seleccionar o ingresar un model_id.",
      });

      return false;
    }

    return true;
  };

  const handleDownloadCsv = async () => {
    if (!validateModelId()) return;

    try {
      setLoading(true);

      setAlert({
        type: "info",
        message: "Generando CSV de resultados...",
      });

      const blob = await downloadCsvReport(modelId);

      triggerFileDownload(
        blob,
        `${modelId}_clusters.csv`
      );

      setAlert({
        type: "success",
        message: "CSV descargado correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "No se pudo descargar el CSV. Verifica que el modelo exista.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!validateModelId()) return;

    try {
      setLoading(true);

      setAlert({
        type: "info",
        message: "Generando reporte PDF...",
      });

      const blob = await downloadPdfReport(modelId);

      triggerFileDownload(
        blob,
        `${modelId}_report.pdf`
      );

      setAlert({
        type: "success",
        message: "PDF descargado correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "No se pudo descargar el PDF. Verifica que el modelo exista.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid-2">
      <Card
        title="Seleccionar modelo"
        description="Elige un modelo entrenado para exportar sus resultados."
      >
        <div className="export-form">
          <label className="form-control">
            <span>Modelo entrenado</span>

            <select value={modelId} onChange={handleModelChange}>
              <option value="">Selecciona un modelo</option>

              {models.map((model) => (
                <option key={model.model_id} value={model.model_id}>
                  {model.dataset_type} · {model.algorithm} · {model.filename}
                </option>
              ))}
            </select>
          </label>

          <Input
            label="Model ID"
            value={modelId}
            onChange={(event) => setModelId(event.target.value)}
            placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          />

          {selectedModel && (
            <div className="export-model-summary">
              <span>Modelo seleccionado</span>

              <strong>{selectedModel.model_id}</strong>

              <div className="badges-row">
                <Badge variant="success">{selectedModel.dataset_type}</Badge>
                <Badge>{selectedModel.algorithm}</Badge>
                <Badge>{selectedModel.filename}</Badge>
              </div>

              <div className="export-stats">
                <div>
                  <span>Registros</span>
                  <strong>{selectedModel.total_records}</strong>
                </div>

                <div>
                  <span>Clusters</span>
                  <strong>{selectedModel.clusters_found}</strong>
                </div>

                <div>
                  <span>Ruido</span>
                  <strong>{selectedModel.noise_points}</strong>
                </div>
              </div>
            </div>
          )}

          <Alert type={alert.type} message={alert.message} />
        </div>
      </Card>

      <Card
        title="Reportes disponibles"
        description="Descarga los resultados del modelo en CSV o PDF."
      >
        <div className="export-actions">
          <button
            type="button"
            className="export-action-card"
            onClick={handleDownloadCsv}
            disabled={loading || !modelId.trim()}
          >
            <div className="export-action-icon">
              <FileDown size={26} />
            </div>

            <div>
              <h3>Exportar CSV</h3>
              <p>
                Descarga las columnas originales junto con el cluster asignado,
                nombre del segmento y coordenadas PCA/SVD.
              </p>
            </div>
          </button>

          <button
            type="button"
            className="export-action-card"
            onClick={handleDownloadPdf}
            disabled={loading || !modelId.trim()}
          >
            <div className="export-action-icon">
              <FileText size={26} />
            </div>

            <div>
              <h3>Exportar PDF</h3>
              <p>
                Genera un reporte con información general, métricas,
                distribución de clusters y visualización PCA/SVD.
              </p>
            </div>
          </button>

          <div className="actions-row">
            <Button
              variant="secondary"
              onClick={handleDownloadCsv}
              disabled={loading || !modelId.trim()}
            >
              Descargar CSV
            </Button>

            <Button
              onClick={handleDownloadPdf}
              disabled={loading || !modelId.trim()}
            >
              Descargar PDF
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default ExportButtons;