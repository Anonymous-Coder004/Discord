import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "./Input";
import Button from "./Button";
import { Lock } from "lucide-react";
import { formatDate } from "../utils/formatDate";
import roomApi from "../api/rooms";

const RoomDetailPanel = ({ room = null }) => {
  const navigate = useNavigate();

  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Empty state (no room selected)
  if (!room) {
    return (
      <section className="flex-1 flex items-center justify-center">
        <p className="text-white/40 text-lg">
          Create a new room to start
        </p>
      </section>
    );
  }

  const handleJoinRoom = async () => {
    try {
      setLoading(true);
      setError("");

      await roomApi.joinRoom(room.id, {
        password: password || null,
      });

      // ✅ redirect to chat page
      navigate(`/rooms/${room.id}/Chat`);
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.detail || "Failed to join room"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="flex-1 px-12 py-10 overflow-y-auto">
      {/* Room Name */}
      <h1 className="text-white text-3xl font-semibold">
        {room.name}
      </h1>

      {/* Metadata */}
      <div className="mt-4 space-y-2 text-white/70">
        <p>
          <span className="text-white/50">Created At:</span>{" "}
          {formatDate(room.created_at)}
        </p>

        <p>
          <span className="text-white/50">Owner:</span>{" "}
          {room.owner_username}
        </p>
      </div>

      {/* LLM Info */}
      <div className="mt-6 space-y-3">
        <div className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={room.has_llm}
            readOnly
            className="accent-indigo-500"
          />
          <span className="text-white/70">
            LLM Enabled
          </span>
        </div>

        {room.has_llm && (
          <p className="text-white/70">
            <span className="text-white/50">LLM Name:</span>{" "}
            {room.llm_username}
          </p>
        )}
      </div>

      {/* Join Section */}
      <div className="mt-10 max-w-md">
        <Input
          type="password"
          placeholder="Enter Password"
          icon={Lock}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        {error && (
          <p className="text-red-400 text-sm mt-3">
            {error}
          </p>
        )}

        <div className="mt-4">
          <Button
            onClick={handleJoinRoom}
            disabled={loading}
          >
            {loading ? "Joining..." : "Join Room"}
          </Button>
        </div>
      </div>
    </section>
  );
};

export default RoomDetailPanel;
