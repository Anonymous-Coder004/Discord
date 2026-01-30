import React, { useEffect, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import Header from "../components/Header/Header";
import RoomListPanel from "../components/RoomListPanel";
import RoomDetailPanel from "../components/RoomDetailPanel";
import AboutSection from "../components/AboutSection";
import { useAuth } from "../context/AuthContext";
import roomApi from "../api/rooms";

const Home = () => {
  const { user, loading, logout } = useAuth();
  const navigate = useNavigate();

  const [rooms, setRooms] = useState([]);
  const [selectedRoom, setSelectedRoom] = useState(null);
  const [viewMode, setViewMode] = useState("ABOUT"); 
  // ABOUT | JOIN

  /* ───────────── AUTH GUARD ───────────── */
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

  /* ───────────── FETCH ROOMS ───────────── */
  useEffect(() => {
    const fetchRooms = async () => {
      try {
        const data = await roomApi.listRooms();
        setRooms(data);
      } catch (err) {
        console.error("Failed to fetch rooms", err);
      }
    };

    fetchRooms();
  }, []);

  /* ───────────── ROOM CLICK ───────────── */
  const handleRoomSelect = async (roomId) => {
    try {
      const res = await roomApi.checkAccess(roomId);

      if (res.is_member) {
        navigate(`/rooms/${roomId}/Chat`);
      } else {
        setSelectedRoom(res.room);
        setViewMode("JOIN");
      }
    } catch (err) {
      console.error("Room access check failed", err);
    }
  };

  /* ───────────── HEADER ACTIONS ───────────── */
  const handleCreateRoom = () => {
    navigate("/rooms/create");
  };

const handleDeleteRoom = async () => {
  if (!selectedRoom) return;

  const confirmDelete = window.confirm(
    "Are you sure you want to delete this room?"
  );

  if (!confirmDelete) return;

  try {
    await roomApi.deleteRoom(selectedRoom.id);

    // Refresh room list
    const updatedRooms = await roomApi.listRooms();
    setRooms(updatedRooms);

    // Reset right panel to About section
    setSelectedRoom(null);
    setViewMode("ABOUT");
  } catch (err) {
    console.error("Failed to delete room", err);
    alert("Failed to delete room");
  }
};

  const handleLogout = () => {
    logout();
  };

  const canDeleteRoom =
    selectedRoom && selectedRoom.owner_id === user.id;

  return (
    <div className="h-screen flex flex-col bg-gradient-to-br from-black via-slate-900 to-black">
      <Header
        showCreate
        onCreateRoom={handleCreateRoom}
        onLogout={handleLogout}
      />

      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar */}
        <RoomListPanel
          rooms={rooms}
          onRoomSelect={handleRoomSelect}
        />

        {/* Right Panel */}
        {viewMode === "ABOUT" && <AboutSection />}

        {viewMode === "JOIN" && (
          <RoomDetailPanel room={selectedRoom} />
        )}
      </div>
    </div>
  );
};

export default Home;
