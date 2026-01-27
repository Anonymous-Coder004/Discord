import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { signup } from "../api/auth";

export default function Signup() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (formData.password.length < 8) {
      setError("Password must be at least 8 characters long");
      return;
    }

    try {
      await signup(
        formData.email,
        formData.username,
        formData.password
      );

      // After successful signup → go to login
      navigate("/login");
    } catch (err) {
      setError("Signup failed. Email or username already exists.");
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-[#0b0b14] relative overflow-hidden">

      {/* SIGNUP FORM */}
      <form
        onSubmit={handleSubmit}
        className="relative z-10 w-full sm:w-87.5 text-center bg-white/6 border border-white/10 rounded-2xl px-8 backdrop-blur-xl"
      >
        <h1 className="text-white text-3xl mt-10 font-medium">
          Sign up
        </h1>

        <p className="text-gray-400 text-sm mt-2">
          Please sign in to continue
        </p>

        {/* Username (same UI as Name field, only logic changed) */}
        <div className="flex items-center mt-6 w-full bg-white/5 ring-2 ring-white/10 focus-within:ring-indigo-500/60 h-12 rounded-full overflow-hidden pl-6 gap-2 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" className="text-white/60" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <circle cx="12" cy="8" r="5" />
            <path d="M20 21a8 8 0 0 0-16 0" />
          </svg>
          <input
            type="text"
            name="username"
            placeholder="Username"
            className="w-full bg-transparent text-white placeholder-white/60 border-none outline-none"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        {/* Email */}
        <div className="flex items-center w-full mt-4 bg-white/5 ring-2 ring-white/10 focus-within:ring-indigo-500/60 h-12 rounded-full overflow-hidden pl-6 gap-2 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" className="text-white/75" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7" />
            <rect x="2" y="4" width="20" height="16" rx="2" />
          </svg>
          <input
            type="email"
            name="email"
            placeholder="Email id"
            className="w-full bg-transparent text-white placeholder-white/60 border-none outline-none"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        {/* Password */}
        <div className="flex items-center mt-4 w-full bg-white/5 ring-2 ring-white/10 focus-within:ring-indigo-500/60 h-12 rounded-full overflow-hidden pl-6 gap-2 transition-all">
          <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" className="text-white/75" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <rect width="18" height="11" x="3" y="11" rx="2" ry="2" />
            <path d="M7 11V7a5 5 0 0 1 10 0v4" />
          </svg>
          <input
            type="password"
            name="password"
            placeholder="Password"
            minLength={8}
            className="w-full bg-transparent text-white placeholder-white/60 border-none outline-none"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && (
          <p className="text-red-400 text-sm mt-3">
            {error}
          </p>
        )}

        <div className="mt-4 text-left">
          <button
            type="button"
            className="text-sm text-indigo-400 hover:underline"
          >
            Forget password?
          </button>
        </div>

        <button
          type="submit"
          className="mt-2 w-full h-11 rounded-full text-white bg-indigo-600 hover:bg-indigo-500 transition"
        >
          Sign up
        </button>

        <p className="text-gray-400 text-sm mt-3 mb-11">
          Already have an account?
          <Link to="/login" className="text-indigo-400 hover:underline ml-1">
            click here
          </Link>
        </p>
      </form>

      {/* BACKDROP (same pattern as login) */}
      <div className="absolute inset-0 -z-0 pointer-events-none">
        <div className="absolute left-1/2 top-24 -translate-x-1/2 w-[900px] h-[420px] bg-gradient-to-tr from-indigo-900/50 to-transparent rounded-full blur-3xl" />
        <div className="absolute right-16 bottom-16 w-[420px] h-[260px] bg-gradient-to-bl from-purple-900/40 to-transparent rounded-full blur-3xl" />
      </div>

    </div>
  );
}
