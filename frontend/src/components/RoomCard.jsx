import React from "react";
import { formatDate } from "../utils/formatDate";
const RoomCard = ({
  name,
  llmUsername,
  createdAtLabel, // already formatted: "2 hours ago"
  selected = false,
  onClick,
}) => {
  return (
    <div
      onClick={onClick}
      className={`
        cursor-pointer
        rounded-xl
        px-4 py-3
        mb-3
        transition-all
        border
        ${
          selected
            ? "border-indigo-500/60 bg-white/10"
            : "border-white/10 bg-white/5 hover:bg-white/10"
        }
      `}
    >
      <div className="flex items-start justify-between gap-3">
        {/* Left content */}
        <div className="flex flex-col">
          <span className="text-white font-medium text-sm truncate">
            {name}
          </span>

          <span className="text-white/60 text-xs mt-0.5">
            {llmUsername ? llmUsername : "No LLM"}
          </span>
        </div>

        {/* Right time */}
        <span className="text-white/40 text-xs whitespace-nowrap">
          {formatDate(createdAtLabel)}
        </span>
      </div>
    </div>
  );
};

export default RoomCard;
