function Alert({ type = "info", title, message }) {
  if (!message) return null;

  return (
    <div className={`alert alert-${type}`}>
      {title && <strong>{title}</strong>}
      <p>{message}</p>
    </div>
  );
}

export default Alert;