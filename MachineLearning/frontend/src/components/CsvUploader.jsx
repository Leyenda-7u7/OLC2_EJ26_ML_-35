import { useState } from "react";
import { cargarCsv } from "../api/Api";

function CsvUploader({ onCsvLoaded }) {
  const [archivo, setArchivo] = useState(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState("");
  const [respuesta, setRespuesta] = useState(null);

  const handleFileChange = (event) => {
    setArchivo(event.target.files?.[0] ?? null);
    setError("");
    setRespuesta(null);
  };

  const handleUpload = async () => {
    if (!archivo) {
      setError("Selecciona un archivo CSV antes de continuar.");
      return;
    }

    try {
      setCargando(true);
      setError("");
      setRespuesta(null);

      const data = await cargarCsv(archivo);
      setRespuesta(data);

      if (onCsvLoaded) {
        onCsvLoaded();
      }
    } catch (err) {
      setError(err.message || "No se pudo cargar el archivo CSV.");
    } finally {
      setCargando(false);
    }
  };

  return (
    <section className="card">
      <div className="card-header">
        <div>
          <h2>Carga de datos</h2>
          <p>Selecciona el archivo CSV que usara el backend para preparar los datos.</p>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="csv-file">Archivo CSV</label>
        <input
          id="csv-file"
          type="file"
          accept=".csv,text/csv"
          onChange={handleFileChange}
          disabled={cargando}
        />
      </div>

      {error && <p className="error-message">{error}</p>}

      {respuesta && (
        <div className="success-box">
          <h3>{respuesta.mensaje || "Archivo cargado correctamente."}</h3>

          {respuesta.reporte_limpieza && (
            <div className="cleaning-summary">
              <p>
                Total original:{" "}
                <strong>{respuesta.reporte_limpieza.total_original}</strong>
              </p>
              <p>
                Total limpio:{" "}
                <strong>{respuesta.reporte_limpieza.total_limpio}</strong>
              </p>
              <p>
                Filas eliminadas:{" "}
                <strong>{respuesta.reporte_limpieza.filas_eliminadas}</strong>
              </p>
              <p>
                Valores imputados:{" "}
                <strong>{respuesta.reporte_limpieza.valores_imputados}</strong>
              </p>
            </div>
          )}
        </div>
      )}

      <button
        className="btn btn-primary"
        type="button"
        onClick={handleUpload}
        disabled={cargando}
      >
        {cargando ? "Cargando..." : "Cargar CSV"}
      </button>
    </section>
  );
}

export default CsvUploader;
