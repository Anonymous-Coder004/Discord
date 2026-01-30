import React from "react";
import { useParams, Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Chat = () => {
  const { user, loading } = useAuth();
  const { roomId } = useParams();

  // Auth guard
  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center text-white">
        Loading...
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-black via-slate-900 to-black">
      <div className="text-center space-y-4">
        <h1 className="text-white text-3xl font-semibold">
          Chat Page
        </h1>

        <p className="text-white/70 text-lg">
          Room ID: <span className="text-indigo-400">{roomId}</span>
        </p>

        <p className="text-white/40 text-sm">
          (Temporary page – chat UI coming later)
        </p>
      </div>
    </div>
  );
};

export default Chat;
