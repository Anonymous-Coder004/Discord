import React from "react";
import Button from "../Button";

const Header = ({
  onCreateRoom,
  onDeleteRoom,
  onLogout,
  canDeleteRoom = false,
}) => {
  return (
    <header
      className="
        w-full h-16
        px-6
        flex items-center justify-between
        bg-black/30
        backdrop-blur-xl
        border-b border-white/10
      "
    >
      {/* Left: Logo */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 flex items-center justify-center rounded-lg bg-indigo-600">
          {/* Discord-like icon placeholder */}
          <span className="text-white font-bold text-lg">D</span>
        </div>

        <span className="text-white text-xl font-semibold tracking-wide">
          Discord
        </span>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-3">
        <Button
          variant="primary"
          className="px-6"
          onClick={onCreateRoom}
        >
          Create Room
        </Button>

        <Button
          variant="danger"
          className="px-6"
          disabled={!canDeleteRoom}
          onClick={onDeleteRoom}
        >
          Delete Room
        </Button>

        <Button
          variant="ghost"
          className="px-6"
          onClick={onLogout}
        >
          Logout
        </Button>
      </div>
    </header>
  );
};

export default Header;
