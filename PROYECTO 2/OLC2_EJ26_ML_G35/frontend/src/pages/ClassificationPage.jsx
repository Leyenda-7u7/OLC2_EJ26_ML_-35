import PageContainer from "../components/layouts/PageContainer";
import ClassificationForm from "../components/classification/ClassificationForm";

function ClassificationPage() {
  return (
    <PageContainer
      title="Clasificación de nuevo registro"
      description="Asigna un freelancer o una reseña nueva al segmento existente que mejor le corresponde, sin reentrenar el modelo."
    >
      <ClassificationForm />
    </PageContainer>
  );
}

export default ClassificationPage;