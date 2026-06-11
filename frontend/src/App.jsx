import { useState, useRef, useEffect } from "react";
import {
  askTutor,
  generateQuiz,
  summarizeMaterial,
  getMaterials,
  uploadMaterial,
} from "./services/api";
import "./App.css";

function App() {
  const [activePanel, setActivePanel] = useState("chat");
  const [chatMessages, setChatMessages] = useState([
    {
      role: "ai",
      text: "Halo! Saya AI Tutor EduAI. Tanya apa saja tentang pelajaranmu 📚",
    },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [subject, setSubject] = useState("");

  const [quizSubject, setQuizSubject] = useState("");
  const [quizTopic, setQuizTopic] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [quizLoading, setQuizLoading] = useState(false);
  const [selectedAnswers, setSelectedAnswers] = useState({});

  const [summarizeText, setSummarizeText] = useState("");
  const [summary, setSummary] = useState("");
  const [summarizeLoading, setSummarizeLoading] = useState(false);

  const [materials, setMaterials] = useState([]);
  const [uploading, setUploading] = useState(false);
  const fileRef = useRef();
  const chatEndRef = useRef();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  useEffect(() => {
    if (activePanel === "materials") fetchMaterials();
  }, [activePanel]);

  const fetchMaterials = async () => {
    try {
      const res = await getMaterials();
      setMaterials(res.data.materials || []);
    } catch (e) {
      setMaterials([]);
    }
  };

  const sendChat = async () => {
    if (!chatInput.trim() || chatLoading) return;
    const question = chatInput.trim();
    setChatInput("");
    setChatMessages((prev) => [...prev, { role: "user", text: question }]);
    setChatLoading(true);
    try {
      const res = await askTutor(question, subject || "Umum", 1);
      const answer =
        res.data.answer || res.data.response || JSON.stringify(res.data);
      setChatMessages((prev) => [...prev, { role: "ai", text: answer }]);
    } catch (e) {
      setChatMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "❌ Gagal terhubung ke AI. Pastikan backend berjalan.",
        },
      ]);
    }
    setChatLoading(false);
  };

  const handleGenerateQuiz = async () => {
    if (!quizSubject || !quizTopic)
      return alert("Isi mata pelajaran dan topik dulu!");
    setQuizLoading(true);
    setQuizData(null);
    setSelectedAnswers({});
    try {
      const res = await generateQuiz(quizSubject, quizTopic, 5);
      setQuizData(res.data);
    } catch (e) {
      alert("Gagal generate quiz. Cek koneksi backend.");
    }
    setQuizLoading(false);
  };

  const handleSummarize = async () => {
    if (!summarizeText.trim()) return;
    setSummarizeLoading(true);
    setSummary("");
    try {
      const res = await summarizeMaterial(summarizeText);
      setSummary(
        res.data.summary || res.data.result || JSON.stringify(res.data),
      );
    } catch (e) {
      setSummary("❌ Gagal meringkas. Cek koneksi backend.");
    }
    setSummarizeLoading(false);
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);
    try {
      await uploadMaterial(formData);
      alert("File berhasil diupload!");
      fetchMaterials();
    } catch (e) {
      alert("Gagal upload file.");
    }
    setUploading(false);
  };

  const navItems = [
    { id: "chat", icon: "💬", label: "AI Tutor" },
    { id: "quiz", icon: "📝", label: "Quiz" },
    { id: "materials", icon: "📁", label: "Materi" },
    { id: "summarize", icon: "📄", label: "Ringkasan" },
  ];

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="sidebar-brand">
          <span className="brand-icon">🎓</span>
          <span className="brand-name">EduAI</span>
        </div>
        <nav className="sidebar-nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-item ${activePanel === item.id ? "active" : ""}`}
              onClick={() => setActivePanel(item.id)}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-footer">
          <span className="status-dot"></span> Backend Online
        </div>
      </aside>

      <main className="main">
        {activePanel === "chat" && (
          <div className="panel">
            <div className="panel-header">
              <div>
                <h2>AI Tutor</h2>
                <p className="panel-sub">Powered by Groq LLaMA 3.3 70B</p>
              </div>
              <input
                className="subject-input"
                placeholder="Mata pelajaran..."
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
              />
            </div>
            <div className="chat-content">
              {chatMessages.map((msg, i) => (
                <div key={i} className={`bubble ${msg.role}`}>
                  <div className="bubble-label">
                    {msg.role === "ai" ? "EduAI" : "Kamu"}
                  </div>
                  <div className="bubble-text">{msg.text}</div>
                </div>
              ))}
              {chatLoading && (
                <div className="bubble ai">
                  <div className="bubble-label">EduAI</div>
                  <div className="bubble-text typing">Mengetik...</div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="chat-input-area">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && sendChat()}
                placeholder="Tanya sesuatu tentang pelajaranmu..."
                disabled={chatLoading}
              />
              <button onClick={sendChat} disabled={chatLoading}>
                Kirim
              </button>
            </div>
          </div>
        )}

        {activePanel === "quiz" && (
          <div className="panel">
            <div className="panel-header">
              <div>
                <h2>Generate Quiz</h2>
                <p className="panel-sub">AI akan membuat soal otomatis</p>
              </div>
            </div>
            <div className="panel-body">
              <div className="form-row">
                <input
                  placeholder="Mata pelajaran (e.g. Matematika)"
                  value={quizSubject}
                  onChange={(e) => setQuizSubject(e.target.value)}
                />
                <input
                  placeholder="Topik (e.g. Aljabar Linear)"
                  value={quizTopic}
                  onChange={(e) => setQuizTopic(e.target.value)}
                />
                <button onClick={handleGenerateQuiz} disabled={quizLoading}>
                  {quizLoading ? "Generating..." : "Generate Quiz"}
                </button>
              </div>
              {quizData && (
                <div className="quiz-container">
                  {(quizData.questions || []).map((q, qi) => (
                    <div key={qi} className="quiz-card">
                      <p className="quiz-question">
                        {qi + 1}. {q.question}
                      </p>
                      <div className="quiz-options">
                        {Object.entries(q.options || {}).map(([key, opt], oi) => (
                          <button
                            key={oi}
                            className={`quiz-option ${selectedAnswers[qi] === oi ? (key === q.correct_answer ? "correct" : "wrong") : ""}`}
                            onClick={() =>
                              setSelectedAnswers((prev) => ({
                                ...prev,
                                [qi]: oi,
                              }))
                            }
                          >
                            {opt}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activePanel === "materials" && (
          <div className="panel">
            <div className="panel-header">
              <div>
                <h2>Materi Pembelajaran</h2>
                <p className="panel-sub">Upload dan kelola materi belajar</p>
              </div>
              <button
                onClick={() => fileRef.current.click()}
                disabled={uploading}
              >
                {uploading ? "Uploading..." : "+ Upload Materi"}
              </button>
              <input
                ref={fileRef}
                type="file"
                style={{ display: "none" }}
                onChange={handleUpload}
              />
            </div>
            <div className="panel-body">
              {materials.length === 0 ? (
                <div className="empty-state">
                  <div className="empty-icon">📂</div>
                  <p>Belum ada materi. Upload file pertamamu!</p>
                </div>
              ) : (
                <div className="materials-list">
                  {materials.map((m, i) => (
                    <div key={i} className="material-item">
                      <span>📄 {m.filename || m.key || "File"}</span>
                      <a href={m.url} target="_blank" rel="noreferrer">
                        Download
                      </a>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {activePanel === "summarize" && (
          <div className="panel">
            <div className="panel-header">
              <div>
                <h2>Ringkas Materi</h2>
                <p className="panel-sub">AI akan meringkas teks panjang</p>
              </div>
            </div>
            <div className="panel-body">
              <textarea
                placeholder="Paste teks materi yang ingin diringkas di sini..."
                value={summarizeText}
                onChange={(e) => setSummarizeText(e.target.value)}
                rows={8}
                style={{
                  width: "100%",
                  padding: "12px",
                  borderRadius: "8px",
                  border: "0.5px solid var(--border)",
                  fontSize: "14px",
                  resize: "vertical",
                  background: "var(--bg-secondary)",
                  color: "var(--text-primary)",
                }}
              />
              <button
                onClick={handleSummarize}
                disabled={summarizeLoading}
                style={{ marginTop: "12px" }}
              >
                {summarizeLoading ? "Meringkas..." : "Ringkas Sekarang"}
              </button>
              {summary && (
                <div className="summary-result">
                  <div className="summary-label">Hasil Ringkasan</div>
                  <p>{summary}</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
