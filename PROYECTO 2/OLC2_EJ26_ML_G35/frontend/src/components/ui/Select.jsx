function Select({ label, value, onChange, options = [], name }) {
  return (
    <label className="form-control">
      {label && <span>{label}</span>}

      <select name={name} value={value} onChange={onChange}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

export default Select;