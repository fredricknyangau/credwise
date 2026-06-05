import axios from "axios";
import { useAuth } from "../store/auth";

// Axios instance ready to wire to a real FastAPI backend.
// Set VITE_API_BASE_URL to enable real network calls; otherwise the
// React Query hooks in ./hooks fall back to local mocks.

let base = import.meta.env.VITE_API_BASE_URL ?? "/api/v1";
if (base && !base.endsWith("/api/v1") && !base.endsWith("/api") && base.startsWith("http")) {
  // If the user pasted the Render URL without /api/v1, append it automatically
  base = base.replace(/\/$/, "") + "/api/v1";
}

export const api = axios.create({
  baseURL: base,
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
