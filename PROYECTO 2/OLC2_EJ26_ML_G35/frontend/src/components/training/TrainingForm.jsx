import { useState } from "react";

import Button from "../ui/Button";
import Alert from "../ui/Alert";
import Select from "../ui/Select";
import Input from "../ui/Input";
import Card from "../ui/Card";

import {
  ALGORITHMS,
  DATASET_TYPES,
  VECTORIZERS,
} from "../../utils/constants";

import { trainModel } from "../../api/trainingApi";

function TrainingForm({ onTrainingSuccess }) {
  const [form, setForm] = useState({
    dataset_type: "freelancers",
    filename: "freelancers_dev.csv",
    algorithm: "kmeans",
    n_clusters: 3,
    eps: 0.5,
    min_samples: 5,
    linkage: "ward",
    text_column: "",
    vectorizer: "tfidf",
    random_state: 42,
  });

  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const isReviews = form.dataset_type === "reviews";
  const isDbscan = form.algorithm === "dbscan";

  const usesClusters =
    form.algorithm === "kmeans" ||
    form.algorithm === "agglomerative" ||
    form.algorithm === "gmm";

  const handleChange = (event) => {
    const { name, value } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleDatasetChange = (event) => {
    const datasetType = event.target.value;

    setForm((current) => ({
      ...current,
      dataset_type: datasetType,
      filename:
        datasetType === "freelancers"
          ? "freelancers_dev.csv"
          : "resenas_clientes_dev.csv",
      text_column: datasetType === "reviews" ? "texto_reseña" : "",
      vectorizer: "tfidf",
    }));

    setAlert({
      type: "info",
      message:
        datasetType === "reviews"
          ? "Para reseñas se usará la columna de texto: texto_reseña."
          : "Para freelancers se usarán las variables numéricas y categóricas del CSV.",
    });
  };

  const buildPayload = () => {
    return {
      dataset_type: form.dataset_type,
      filename: form.filename,
      algorithm: form.algorithm,
      n_clusters: Number(form.n_clusters),
      eps: Number(form.eps),
      min_samples: Number(form.min_samples),
      linkage: form.linkage,
      text_column: isReviews ? form.text_column : null,
      vectorizer: isReviews ? form.vectorizer : "tfidf",
      random_state: Number(form.random_state),
    };
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!form.filename.trim()) {
      setAlert({
        type: "error",
        message: "Debes indicar el nombre del archivo CSV.",
      });
      return;
    }

    if (isReviews && !form.text_column.trim()) {
      setAlert({
        type: "error",
        message: "Para reseñas debes indicar la columna de texto.",
      });
      return;
    }

    try {
      setLoading(true);

      setAlert({
        type: "info",
        message: "Entrenando modelo, espera un momento...",
      });

      const payload = buildPayload();
      const result = await trainModel(payload);

      setAlert({
        type: "success",
        message: "Modelo entrenado correctamente.",
      });

      onTrainingSuccess(result);
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Ocurrió un error durante el entrenamiento.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card
      title="Parámetros de entrenamiento"
      description="Configura el dataset, algoritmo y parámetros del modelo de clustering."
    >
      <form className="training-form" onSubmit={handleSubmit}>
        <div className="form-grid-2">
          <Select
            label="Tipo de dataset"
            name="dataset_type"
            value={form.dataset_type}
            onChange={handleDatasetChange}
            options={DATASET_TYPES}
          />

          <Input
            label="Nombre del archivo"
            name="filename"
            value={form.filename}
            onChange={handleChange}
            placeholder={
              isReviews
                ? "resenas_clientes_dev.csv"
                : "freelancers_dev.csv"
            }
          />

          <Select
            label="Algoritmo"
            name="algorithm"
            value={form.algorithm}
            onChange={handleChange}
            options={ALGORITHMS}
          />

          <Input
            label="Random state"
            name="random_state"
            type="number"
            value={form.random_state}
            onChange={handleChange}
          />
        </div>

        {usesClusters && (
          <div className="form-grid-2">
            <Input
              label="Número de clusters"
              name="n_clusters"
              type="number"
              value={form.n_clusters}
              onChange={handleChange}
            />

            {form.algorithm === "agglomerative" && (
              <label className="form-control">
                <span>Linkage</span>

                <select
                  name="linkage"
                  value={form.linkage}
                  onChange={handleChange}
                >
                  <option value="ward">ward</option>
                  <option value="complete">complete</option>
                  <option value="average">average</option>
                  <option value="single">single</option>
                </select>
              </label>
            )}
          </div>
        )}

        {isDbscan && (
          <div className="form-grid-2">
            <Input
              label="EPS"
              name="eps"
              type="number"
              value={form.eps}
              onChange={handleChange}
            />

            <Input
              label="Min samples"
              name="min_samples"
              type="number"
              value={form.min_samples}
              onChange={handleChange}
            />
          </div>
        )}

        {isReviews && (
          <div className="form-grid-2">
            <Input
              label="Columna de texto"
              name="text_column"
              value={form.text_column}
              onChange={handleChange}
              placeholder="texto_reseña"
            />

            <Select
              label="Vectorizador"
              name="vectorizer"
              value={form.vectorizer}
              onChange={handleChange}
              options={VECTORIZERS}
            />
          </div>
        )}

        <Alert type={alert.type} message={alert.message} />

        <div className="actions-row">
          <Button type="submit" disabled={loading}>
            {loading ? "Entrenando..." : "Entrenar modelo"}
          </Button>
        </div>
      </form>
    </Card>
  );
}

export default TrainingForm;