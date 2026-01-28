import React from "react";
import clsx from "clsx";

const Button = ({
  children,
  onClick,
  variant = "primary", // primary | danger | ghost
  disabled = false,
  className = "",
}) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className={clsx(
        "px-5 py-2 text-sm font-medium",
        "whitespace-nowrap",              // 👈 single line text
        "rounded-lg",                     // 👈 flatter corners (not pill)
        "transition-all duration-200",
        "focus:outline-none",
        disabled && "opacity-50 cursor-not-allowed",

        // Variants
        variant === "primary" &&
          "bg-indigo-600 text-white hover:bg-indigo-500",
        variant === "danger" &&
          "bg-slate-700 text-slate-300 hover:bg-red-600 hover:text-white",
        variant === "ghost" &&
          "bg-transparent text-slate-300 hover:bg-white/10",

        className
      )}
    >
      {children}
    </button>
  );
};

export default Button;
