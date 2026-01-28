import React from "react";
import Input from "./Input";
import Button from "./Button";
import { Lock } from "lucide-react";

const RoomDetailPanel = ({
  room = null,
}) => {
  // Empty state (no rooms at all)
  if (!room) {
    return (
      <section className="flex-1 flex items-center justify-center">
        <p className="text-white/40 text-lg">
          Create a new room to start
        </p>
      </section>
    );
  }

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
          {room.created_at_label}
        </p>

        <p>
          <span className="text-white/50">Owner:</span>{" "}
          {room.owner_name}
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
        />

        <div className="mt-4">
          <Button>
            Join Room
          </Button>
        </div>
      </div>
    </section>
  );
};

export default RoomDetailPanel;
