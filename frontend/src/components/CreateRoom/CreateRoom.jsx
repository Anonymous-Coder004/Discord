import React, { useState } from "react";
import Input from "../Input";
import Button from "../Button";

const CreateRoom = ({ onSubmit }) => {
  const [form, setForm] = useState({
    name: "",
    password: "",
    has_llm: false,
    llm_username: "",
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    // UI-only for now
    onSubmit?.(form);
  };

  return (
    <div className="flex flex-1 items-center justify-center">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md bg-white/5 border border-white/10 rounded-2xl px-8 py-10 backdrop-blur-md"
      >
        <h2 className="text-white text-2xl font-semibold text-center mb-6">
          Create a New Room
        </h2>

        {/* Room Name */}
        <div className="mb-4">
          <label className="text-sm text-gray-300 mb-1 block">
            Room Name
          </label>
          <Input
            name="name"
            placeholder="Room Name"
            value={form.name}
            onChange={handleChange}
            required
          />
        </div>

        {/* Password */}
        <div className="mb-4">
          <label className="text-sm text-gray-300 mb-1 block">
            Password
          </label>
          <Input
            type="password"
            name="password"
            placeholder="Optional"
            value={form.password}
            onChange={handleChange}
          />
        </div>

        {/* Enable LLM */}
        <div className="flex items-center gap-2 mb-4">
          <input
            type="checkbox"
            name="has_llm"
            checked={form.has_llm}
            onChange={handleChange}
            className="accent-indigo-500"
          />
          <span className="text-sm text-gray-300">
            Enable LLM
          </span>
        </div>

        {/* LLM Username */}
        {form.has_llm && (
          <div className="mb-6">
            <label className="text-sm text-gray-300 mb-1 block">
              LLM Username
            </label>
            <Input
              name="llm_username"
              placeholder="LLM Username"
              value={form.llm_username}
              onChange={handleChange}
              required
            />
          </div>
        )}

        {/* Submit */}
        <Button type="submit" className="w-full">
          Create Room
        </Button>
      </form>
    </div>
  );
};

export default CreateRoom;
