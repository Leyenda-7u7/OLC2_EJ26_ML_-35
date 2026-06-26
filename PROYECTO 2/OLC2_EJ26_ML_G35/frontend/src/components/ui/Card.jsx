function Card({ title, description, children, footer }) {
  return (
    <div className="card">
      {(title || description) && (
        <div className="card-header">
          {title && <h3>{title}</h3>}
          {description && <p>{description}</p>}
        </div>
      )}

      <div className="card-content">{children}</div>

      {footer && <div className="card-footer">{footer}</div>}
    </div>
  );
}

export default Card;