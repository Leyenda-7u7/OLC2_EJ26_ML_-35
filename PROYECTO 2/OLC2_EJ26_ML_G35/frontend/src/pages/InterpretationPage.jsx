import { useState } from "react";

import PageContainer from "../components/layouts/PageContainer";
import Card from "../components/ui/Card";
import Input from "../components/ui/Input";
import Button from "../components/ui/Button";
import Alert from "../components/ui/Alert";

import PCAChart from "../components/analysis/PCAChart";
import ClusterProfiles from "../components/analysis/ClusterProfiles";
import CrossSegmentTable from "../components/analysis/CrossSegmentTable";
import FrequentTermsCard from "../components/analysis/FrequentTermsCard";

import {
  getPcaAnalysis,
  getClusterProfiles,
  getCrossSegmentTable,
} from "../api/analysisApi";

import { useModelStore } from "../hooks/useModelStore";

function InterpretationPage() {
  const { lastModel, models } = useModelStore();

  const [modelId, setModelId] = useState(lastModel?.model_id || "");
  const [freelancerModelId, setFreelancerModelId] = useState("");
  const [reviewsModelId, setReviewsModelId] = useState("");

  const [pcaData, setPcaData] = useState(null);
  const [profilesData, setProfilesData] = useState(null);
  const [crossTableData, setCrossTableData] = useState(null);

  const [loading, setLoading] = useState(false);
  const [alert, setAlert] = useState({
    type: "",
    message: "",
  });

  const handleLoadAnalysis = async () => {
    if (!modelId.trim()) {
      setAlert({
        type: "error",
        message: "Debes ingresar un model_id.",
      });
      return;
    }

    try {
      setLoading(true);
      setAlert({
        type: "info",
        message: "Cargando análisis del modelo...",
      });

      const [pca, profiles] = await Promise.all([
        getPcaAnalysis(modelId),
        getClusterProfiles(modelId),
      ]);

      setPcaData(pca);
      setProfilesData(profiles);

      setAlert({
        type: "success",
        message: "Análisis cargado correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Error al cargar la interpretación del modelo.",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleLoadCrossTable = async () => {
    if (!freelancerModelId.trim() || !reviewsModelId.trim()) {
      setAlert({
        type: "error",
        message:
          "Debes ingresar el model_id de freelancers y el model_id de reseñas.",
      });
      return;
    }

    try {
      setLoading(true);
      setAlert({
        type: "info",
        message: "Generando tabla cruzada...",
      });

      const table = await getCrossSegmentTable(
        freelancerModelId,
        reviewsModelId
      );

      setCrossTableData(table);

      setAlert({
        type: "success",
        message: "Tabla cruzada generada correctamente.",
      });
    } catch (error) {
      setAlert({
        type: "error",
        message:
          error.response?.data?.detail ||
          "Error al generar la tabla cruzada.",
      });
    } finally {
      setLoading(false);
    }
  };

  const loadModelFromHistory = (selectedModelId) => {
    setModelId(selectedModelId);
  };

  return (
    <PageContainer
      title="Interpretación de los segmentos"
      description="Visualiza los clusters en 2D, revisa perfiles, nombres de segmentos, términos relevantes y cruces entre modelos."
    >
      <Card
        title="Seleccionar modelo"
        description="Ingresa un model_id entrenado o selecciona uno del historial local."
      >
        <div className="form-grid-2">
          <Input
            label="Model ID"
            value={modelId}
            onChange={(event) => setModelId(event.target.value)}
            placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
          />

          <div className="form-control">
            <span>Modelos recientes</span>
            <select
              value={modelId}
              onChange={(event) => loadModelFromHistory(event.target.value)}
            >
              <option value="">Selecciona un modelo</option>

              {models.map((model) => (
                <option key={model.model_id} value={model.model_id}>
                  {model.dataset_type} · {model.algorithm} · {model.filename}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="actions-row">
          <Button onClick={handleLoadAnalysis} disabled={loading}>
            {loading ? "Cargando..." : "Cargar interpretación"}
          </Button>
        </div>

        <Alert type={alert.type} message={alert.message} />
      </Card>

      <div className="grid-2">
        <PCAChart data={pcaData} />
        <ClusterProfiles data={profilesData} />
      </div>

      {profilesData?.dataset_type === "reviews" && (
        <FrequentTermsCard data={profilesData} />
      )}

      <Card
        title="Cruce entre segmentos"
        description="Compara clusters del modelo de freelancers contra clusters del modelo de reseñas."
      >
        <div className="form-grid-2">
          <Input
            label="Model ID freelancers"
            value={freelancerModelId}
            onChange={(event) => setFreelancerModelId(event.target.value)}
            placeholder="model_id de freelancers"
          />

          <Input
            label="Model ID reseñas"
            value={reviewsModelId}
            onChange={(event) => setReviewsModelId(event.target.value)}
            placeholder="model_id de reseñas"
          />
        </div>

        <div className="actions-row">
          <Button
            variant="secondary"
            onClick={handleLoadCrossTable}
            disabled={loading}
          >
            Generar tabla cruzada
          </Button>
        </div>
      </Card>

      <CrossSegmentTable data={crossTableData} />
    </PageContainer>
  );
}

export default InterpretationPage;
