import axios from "axios";
import { useAuth } from "../store/auth";

// Axios instance ready to wire to a real FastAPI backend.
// Set VITE_API_BASE_URL to enable real network calls; otherwise the
// React Query hooks in ./hooks fall back to local mocks.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? "/api",
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = useAuth.getState().token;
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (r) => r,
  (error) => {
    if (error?.response?.status === 401) {
      useAuth.getState().logout();
    }
    return Promise.reject(error);
  },
);

export const USE_MOCKS = !import.meta.env.VITE_API_BASE_URL;
