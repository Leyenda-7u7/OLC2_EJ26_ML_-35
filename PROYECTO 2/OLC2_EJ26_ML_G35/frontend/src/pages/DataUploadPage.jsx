import PageContainer from "../components/layouts/PageContainer";
import Card from "../components/ui/Card";
import FileUploader from "../components/data/FileUploader";

function DataUploadPage() {
  return (
    <PageContainer
      title="Carga y preprocesamiento"
      description="Sube los archivos CSV de freelancers y reseñas, realiza limpieza básica y visualiza una muestra de los datos."
    >
      <div className="grid-2">
        <Card>
          <FileUploader
            datasetType="freelancers"
            title="Freelancers"
            description="Carga y limpia el dataset de perfiles de freelancers."
          />
        </Card>

        <Card>
          <FileUploader
            datasetType="reviews"
            title="Reseñas de clientes"
            description="Carga y limpia el dataset de reseñas textuales."
          />
        </Card>
      </div>
    </PageContainer>
  );
}

export default DataUploadPage;