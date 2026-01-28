import React from "react";

const Input = ({
  type = "text",
  name,
  placeholder,
  value,
  onChange,
  icon: Icon,
  required = false,
  minLength,
}) => {
  return (
    <div
      className="
        flex items-center
        w-full h-12
        mt-4
        rounded-full
        bg-white/5
        ring-2 ring-white/10
        focus-within:ring-indigo-500/60
        transition-all
        overflow-hidden
        px-5 gap-3
      "
    >
      {Icon && (
        <Icon className="text-white/70 w-4 h-4 shrink-0" />
      )}

      <input
        type={type}
        name={name}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        required={required}
        minLength={minLength}
        autoComplete="off"
        className="
          w-full
          bg-transparent
          text-white
          placeholder-white/60
          outline-none
          border-none
          autofill:bg-transparent
        "
      />
    </div>
  );
};

export default Input;
