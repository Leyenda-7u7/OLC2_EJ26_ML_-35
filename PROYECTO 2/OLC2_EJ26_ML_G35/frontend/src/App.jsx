import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/layouts/Navbar";

import DataUploadPage from "./pages/DataUploadPage";
import TrainingPage from "./pages/TrainingPage";
import InterpretationPage from "./pages/InterpretationPage";
import EvaluationPage from "./pages/EvaluationPage";
import ClassificationPage from "./pages/ClassificationPage";
import ExportPage from "./pages/ExportPage";

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Navbar />

        <Routes>
          <Route path="/" element={<DataUploadPage />} />
          <Route path="/training" element={<TrainingPage />} />
          <Route path="/interpretation" element={<InterpretationPage />} />
          <Route path="/evaluation" element={<EvaluationPage />} />
          <Route path="/classification" element={<ClassificationPage />} />
          <Route path="/export" element={<ExportPage />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;