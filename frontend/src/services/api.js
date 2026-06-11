import axios from "axios";

// Base URL: baca dari environment variable, fallback ke localhost
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

// === AI Tutor ===

// Kirim pertanyaan ke AI tutor
export const askTutor = (question, subject, userId = 1) =>
  api.post("/api/ai/ask", {
    question,
    subject,
    user_id: userId,
  });

// Generate quiz otomatis
export const generateQuiz = (subject, topic, numQuestions = 5) =>
  api.post("/api/ai/quiz/generate", {
    subject,
    topic,
    num_questions: numQuestions,
  });

// Ringkas materi
export const summarizeMaterial = (text) =>
  api.post("/api/ai/summarize", null, { params: { text } });

// === Materials ===

// Ambil daftar materi (bisa filter per subject)
export const getMaterials = (subject = null) =>
  api.get("/api/materials/", {
    params: subject ? { subject } : {},
  });

// Upload file materi
export const uploadMaterial = (formData) =>
  api.post("/api/materials/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });