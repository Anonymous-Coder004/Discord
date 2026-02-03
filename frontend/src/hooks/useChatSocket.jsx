import { useEffect, useRef, useState } from "react";

export default function useChatSocket({ roomId, token }) {
  const socketRef = useRef(null);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    if (!roomId || !token) return;

    // reset messages when room changes
    setMessages([]);

    const wsUrl = `ws://127.0.0.1:8000/ws/rooms/${roomId}?token=${token}&limit=50`;
    const socket = new WebSocket(wsUrl);
    socketRef.current = socket;

    socket.onopen = () => {
      console.log("WS connected");
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        setMessages((prev) => [...prev, payload]);
      } catch (err) {
        console.warn("Invalid WS payload", err);
      }
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
