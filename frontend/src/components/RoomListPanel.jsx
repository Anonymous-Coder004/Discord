import React from "react";
import RoomCard from "./RoomCard";

const RoomListPanel = ({
  rooms = [],
  selectedRoomId,
  onRoomSelect,
}) => {
  return (
    <aside
      className="
        w-72
        h-full
        px-3 py-4
        border-r border-white/10
        overflow-y-auto
        scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent
      "
    >
      {rooms.length === 0 ? (
        <div className="text-center text-white/40 text-sm mt-10">
          No rooms available
        </div>
      ) : (
        rooms.map((room) => (
          <RoomCard
            key={room.id}
            name={room.name}
            llmUsername={room.llm_username}
            createdAtLabel={room.created_at}
            selected={room.id === selectedRoomId}
            onClick={() => onRoomSelect(room.id)}
          />
        ))
      )}
    </aside>
  );
};

export default RoomListPanel;
