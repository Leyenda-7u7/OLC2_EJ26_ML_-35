import PageContainer from "../components/layouts/PageContainer";
import ExportButtons from "../components/export/ExportButtons";

function ExportPage() {
  return (
    <PageContainer
      title="Exportación de reportes"
      description="Descarga los resultados del clustering en CSV o un reporte PDF con gráficas, métricas y perfiles básicos."
    >
      <ExportButtons />
    </PageContainer>
  );
}

export default ExportPage;