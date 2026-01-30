import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_BASEURL;

/**
 * Axios instance for room APIs
 */
const roomClient = axios.create({
  baseURL: BASE_URL,
});

/**
 * Attach auth token automatically
 */
roomClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/* =========================================================
   Rooms API
========================================================= */

const roomApi = {
  /**
   * Get all rooms (Home left panel)
   * GET /rooms
   */
  async listRooms() {
    const res = await roomClient.get("/rooms");
    return res.data;
  },

  /**
   * Create a new room
   * POST /rooms
   */
  async createRoom(payload) {
    /**
     * payload = {
     *   name,
     *   has_llm,
     *   llm_username,
     *   password
     * }
     */
    const res = await roomClient.post("/rooms", payload);
    return res.data;
  },

  /**
   * Check room access (membership + metadata)
   * GET /rooms/{room_id}/access
   *
   * Returns:
   * {
   *   is_member: boolean,
   *   room: {...room metadata...}
   * }
   */
  async checkAccess(roomId) {
    const res = await roomClient.get(`/rooms/${roomId}/access`);
    return res.data;
  },

  /**
   * Join a room (password validation)
   * POST /rooms/{room_id}/join
   */
  async joinRoom(roomId, payload) {
    /**
     * payload = { password }
     */
    const res = await roomClient.post(
      `/rooms/${roomId}/join`,
      payload
    );
    return res.data;
  },

  /**
   * Delete a room (owner only)
   * DELETE /rooms/{room_id}
   */
  async deleteRoom(roomId) {
    await roomClient.delete(`/rooms/${roomId}`);
  },
};

export default roomApi;
