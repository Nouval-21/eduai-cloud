import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "",
  headers: { "Content-Type": "application/json" },
});

// === AI Tutor ===
export const askTutor = (question, subject, userId = 1) =>
  api.post("/api/ai/ask", { question, subject, user_id: userId });

export const generateQuiz = (subject, topic, numQuestions = 5) =>
  api.post("/api/ai/quiz/generate", {
    subject,
    topic,
    num_questions: numQuestions,
  });

export const summarizeMaterial = (text) =>
  api.post("/api/ai/summarize", null, { params: { text } });

// === Materials ===
export const getMaterials = (subject = null) =>
  api.get("/api/materials/", {
    params: subject ? { subject } : {},
  });

export const uploadMaterial = (formData) =>
  api.post("/api/materials/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
