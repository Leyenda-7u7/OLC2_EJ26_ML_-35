function Sidebar({ activePage, onChangePage }) {
  const menuItems = [
    {
      id: "training",
      label: "Carga y Entrenamiento",
    },
    {
      id: "evaluation",
      label: "Evaluación de Rendimiento",
    },
    {
      id: "hyperparameters",
      label: "Ajuste de Hiperparámetros",
    },
    {
      id: "prediction",
      label: "Predicciones",
    },
  ];

  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div>
          <h2>CreditGuard</h2>
          <span>Sistema de riesgo crediticio</span>
        </div>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <button
            key={item.id}
            className={
              activePage === item.id
                ? "sidebar-link sidebar-link-active"
                : "sidebar-link"
            }
            onClick={() => onChangePage(item.id)}
          >
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span>Proyecto 1</span>
      </div>
    </aside>
  );
}

export default Sidebar;