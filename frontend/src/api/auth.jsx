import axios from "axios";

// Create axios instance
const API = axios.create({
  baseURL: import.meta.env.VITE_BACKEND_BASEURL, // backend base URL
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * LOGIN
 * POST /auth/login
 */
export const login = (email, password) => {
  return API.post("/auth/login", {
    email,
    password,
  });
};

/**
 * SIGNUP
 * POST /auth/signup
 */
export const signup = (email, username, password) => {
  return API.post("/auth/signup", {
    email,
    username,
    password,
  });
};

/**
 * GET CURRENT USER
 * GET /auth/me
 */
export const getMe = (token) => {
  return API.get("/auth/me", {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};
