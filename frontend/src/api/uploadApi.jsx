import axios from "axios";

const BASE_URL = import.meta.env.VITE_BACKEND_BASEURL;

/**
 * Axios instance for upload APIs
 */
const uploadClient = axios.create({
  baseURL: BASE_URL,
});

/**
 * Attach auth token automatically
 */
uploadClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/* =========================================================
   Upload API
========================================================= */

const uploadApi = {
  /**
   * Upload PDF to room
   * POST /rooms/{room_id}/upload
   */
  async uploadPdf(roomId, file) {
    const formData = new FormData();
    formData.append("file", file);

    const res = await uploadClient.post(
      `/rooms/${roomId}/upload`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return res.data;
  },
};

export default uploadApi;
