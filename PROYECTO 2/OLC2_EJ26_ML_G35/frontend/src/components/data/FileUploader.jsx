import { useState } from "react";

import Button from "../ui/Button";
import Alert from "../ui/Alert";
import DataPreviewTable from "./DataPreviewTable";

import {
  uploadDataset,
  cleanDataset,
  getDatasetPreview,
} from "../../api/dataApi";

function FileUploader({ datasetType, title, description }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [filename, setFilename] = useState("");
  const [preview, setPreview] = useState(null);

  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const handleFileChange = (event) => {
    const file = event.target.files[0];

    setSelectedFile(file || null);
    setFilename(file?.name || "");
    setPreview(null);
    setAlert({
      type: "",
      message: "",
    });
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setAlert({
        type: "error",
        message: "Selecciona un archivo CSV antes de cargar.",
      });
      return;
    }

    try {
      setLoading(true);

      const data = await uploadDataset(datasetType, selectedFile);

      setFilename(data.filename);
      setPreview({
        dataset_type: data.dataset_type,
        filename: data.filename,
        total_rows: data.total_rows,
        total_columns: data.total_columns,
        columns: data.columns,
        preview: data.preview,
      });

      setAlert({
        type: "success",
        message: `Archivo ${data.filename} cargado correctamente.`,
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Error al cargar el archivo.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleClean = async () => {
    if (!filename) {
      setAlert({
        type: "error",
        message: "Primero carga un archivo o escribe un nombre de archivo.",
      });
      return;
    }

    try {
      setLoading(true);

      const data = await cleanDataset(datasetType, filename);

      setAlert({
        type: "success",
        message: `Dataset limpiado correctamente. Duplicados removidos: ${data.removed_duplicates}.`,
      });

      const previewData = await getDatasetPreview(datasetType, filename, true);
      setPreview(previewData);
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Error al limpiar el dataset.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handlePreview = async () => {
    if (!filename) {
      setAlert({
        type: "error",
        message: "Debes indicar el nombre del archivo.",
      });
      return;
    }

    try {
      setLoading(true);

      const data = await getDatasetPreview(datasetType, filename, true);

      setPreview(data);

      setAlert({
        type: "success",
        message: "Preview cargado correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Error al obtener preview.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="uploader-section">
      <div className="uploader-header">
        <div>
          <h3>{title}</h3>
          <p>{description}</p>
        </div>

        <span className="dataset-pill">{datasetType}</span>
      </div>

      <div className="form-grid">
        <label className="form-control">
          <span>Archivo CSV</span>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
          />
        </label>

        <label className="form-control">
          <span>Nombre del archivo</span>
          <input
            type="text"
            value={filename}
            placeholder="freelancers.csv"
            onChange={(event) => setFilename(event.target.value)}
          />
        </label>
      </div>

      <div className="actions-row">
        <Button onClick={handleUpload} disabled={loading}>
          {loading ? "Procesando..." : "Cargar CSV"}
        </Button>

        <Button variant="secondary" onClick={handleClean} disabled={loading}>
          Limpiar dataset
        </Button>

        <Button variant="outline" onClick={handlePreview} disabled={loading}>
          Ver preview
        </Button>
      </div>

      <Alert
        type={alert.type}
        message={alert.message}
      />

      <DataPreviewTable data={preview} />
    </div>
  );
}

export default FileUploader;