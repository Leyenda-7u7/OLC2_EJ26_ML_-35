import { useState } from "react";
import Sidebar from "../components/Sidebar";
import TrainingPage from "./TrainingPage";
import EvaluationPage from "./EvaluationPage";
import HyperparametersPage from "./HyperparametersPage";
import PredictionPage from "./PredictionPage";

function PlaceholderPage({ title, description }) {
  return (
    <div className="page-content">
      <div className="page-title">
        <h1>{title}</h1>
        <p>{description}</p>
      </div>

      <section className="card">
        <h2>Sección en construcción</h2>
        <p>
          Esta sección se conectará con el backend en el siguiente paso del
          desarrollo.
        </p>
      </section>
    </div>
  );
}

function Dashboard() {
  const [activePage, setActivePage] = useState("training");
  const [refreshKey, setRefreshKey] = useState(0);

  const actualizarSistema = () => {
    setRefreshKey((prev) => prev + 1);
  };

  const renderPage = () => {
    switch (activePage) {
      case "training":
        return (
          <TrainingPage
            key={refreshKey}
            onSystemChange={actualizarSistema}
          />
        );

      case "evaluation":
        return <EvaluationPage />;

      case "hyperparameters":
        return <HyperparametersPage />;

      case "prediction":
        return <PredictionPage />;

      default:
        return (
          <TrainingPage
            key={refreshKey}
            onSystemChange={actualizarSistema}
          />
        );
    }
  };

  return (
    <div className="dashboard-layout">
      <Sidebar activePage={activePage} onChangePage={setActivePage} />

      <main className="dashboard-main">{renderPage()}</main>
    </div>
  );
}

export default Dashboard;