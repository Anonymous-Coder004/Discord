import { useEffect, useRef, useState } from "react";

export default function useChatSocket({ roomId, token }) {
  const socketRef = useRef(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!roomId || !token) return;

    // reset messages when room changes
    setMessages([]);
    const WS_BASE = import.meta.env.VITE_WS_BASEURL;
    const wsUrl = `${WS_BASE}/ws/rooms/${roomId}?token=${token}&limit=50`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WS connected");
    };
 
    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type === "system" && payload.action === "room_deleted") {
          alert("Room was deleted by owner");
          socket.close();
          window.location.href = "/";
          return;
        }

        setMessages((prev) => [...prev, payload]);
      } catch {}
    };


    socket.onerror = (err) => {
      console.warn("WS error", err);
    };

    socket.onclose = () => {
      console.log("WS disconnected");
    };

    return () => {
      socket.close(); // always close on cleanup
    };
  }, [roomId, token]);

  const sendMessage = (text) => {
    if (!socketRef.current) return;
    if (socketRef.current.readyState !== WebSocket.OPEN) return;

    socketRef.current.send(
      JSON.stringify({
        type: "chat",
        content: text,
      })
    );
  };

  const disconnect = () => {
    socketRef.current?.close();
  };

  return {
    messages,
    sendMessage,
    disconnect,
  };
}
