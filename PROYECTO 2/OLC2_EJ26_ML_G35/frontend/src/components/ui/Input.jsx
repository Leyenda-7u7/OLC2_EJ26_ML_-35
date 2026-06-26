function Input({ label, type = "text", value, onChange, placeholder, name }) {
  return (
    <label className="form-control">
      {label && <span>{label}</span>}

      <input
        name={name}
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={onChange}
      />
    </label>
  );
}

export default Input;