function PageContainer({ title, description, children }) {
  return (
    <main className="page-container">
      <section className="page-header">
        <h2>{title}</h2>
        <p>{description}</p>
      </section>

      <section className="page-content">{children}</section>
    </main>
  );
}

export default PageContainer;