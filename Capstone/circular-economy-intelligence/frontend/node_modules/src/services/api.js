import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000",
});

// ============================================================
// AUTHENTICATION INTERCEPTOR
// ============================================================

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// ============================================================
// WASTE ANALYSIS
// ============================================================

export const analyzeWaste = (file, weight_kg, quality_factor = 1.0) => {
  const form = new FormData();

  form.append("file", file);
  form.append("weight_kg", weight_kg);
  form.append("quality_factor", quality_factor);

  return api.post("/api/waste/analyze", form).then((response) => response.data);
};

// ============================================================
// WASTE HISTORY
// ============================================================

export const getWasteHistory = (limit = 100) =>
  api
    .get("/api/waste/history", {
      params: { limit },
    })
    .then((response) => response.data);

// ============================================================
// OBJECT DETECTION
// ============================================================

export const detectWaste = (file) => {
  const form = new FormData();

  form.append("file", file);

  return api
    .post("/api/detection/analyze", form)
    .then((response) => response.data);
};

// ============================================================
// VALUATION
// ============================================================

export const estimateValue = (material, weight_kg, quality_factor = 1) =>
  api
    .post("/api/valuation/estimate", {
      material,
      weight_kg,
      quality_factor,
    })
    .then((response) => response.data);

// ============================================================
// VALUATION MODEL METRICS
// ============================================================

export const getValuationMetrics = () =>
  api.get("/api/valuation/metrics").then((response) => response.data);

// ============================================================
// RECOMMENDATION
// ============================================================

export const getRecommendation = (material) =>
  api
    .post("/api/recommendations", {
      material,
    })
    .then((response) => response.data);

// ============================================================
// DASHBOARD
// ============================================================

export const getDashboardStats = () =>
  api.get("/api/dashboard/stats").then((response) => response.data);

// ============================================================
// AUTH
// ============================================================

export const login = (email, password) =>
  api
    .post("/api/auth/login", {
      email,
      password,
    })
    .then((response) => response.data);

export const register = (name, email, password) =>
  api
    .post("/api/auth/register", {
      name,
      email,
      password,
    })
    .then((response) => response.data);

export default api;
