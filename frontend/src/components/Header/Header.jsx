import React from "react";
import Button from "../Button";

const Header = ({
  onHome,
  onCreateRoom,
  onDeleteRoom,
  onLeaveRoom,
  onLogout,

  showHome = false,
  showCreate = false,
  showDelete = false,
  showLeave = false,
  canDeleteRoom = false,
}) => {
  return (
    <header
      className="
        w-full h-16
        px-6
        flex items-center justify-between
        bg-black/40
        backdrop-blur-xl
        border-b border-white/10
      "
    >
      {/* Left: Logo + Home */}
      <div className="flex items-center gap-4">
        <div className="w-9 h-9 flex items-center justify-center rounded-lg bg-indigo-600">
          <span className="text-white font-bold text-lg">D</span>
        </div>

        <span className="text-white text-xl font-semibold tracking-wide">
          Devcord
        </span>

        {showHome && (
          <Button
            variant="ghost"
            className="ml-4 text-white/70 hover:text-white"
            onClick={onHome}
          >
            Home
          </Button>
        )}
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-3">
        {showCreate && (
          <Button
            variant="primary"
            className="px-5"
            onClick={onCreateRoom}
          >
            Create Room
          </Button>
        )}

        {showLeave && (
          <Button
            variant="danger"
            className="px-5"
            onClick={onLeaveRoom}
          >
            Leave Room
          </Button>
        )}

        {showDelete && (
          <Button
            variant="danger"
            className="px-5"
            disabled={!canDeleteRoom}
            onClick={onDeleteRoom}
          >
            Delete Room
          </Button>
        )}

        {/* subtle divider */}
        <div className="w-px h-6 bg-white/10 mx-2" />

        <Button
          variant="ghost"
          className="text-white/60 hover:text-white"
          onClick={onLogout}
        >
          Logout
        </Button>
      </div>
    </header>
  );
};

export default Header;
