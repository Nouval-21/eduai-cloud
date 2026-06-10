# EduAI — API Contract

Base URL development : `http://localhost:8000`
Base URL production : `http://IP_EC2_BACKEND:8000`

## Endpoints

| Method | Endpoint                    | Fungsi                 |
| ------ | --------------------------- | ---------------------- |
| GET    | `/health`                   | Cek status server      |
| POST   | `/api/ai/ask`               | Tanya AI tutor         |
| POST   | `/api/ai/quiz/generate`     | Generate quiz otomatis |
| POST   | `/api/ai/summarize`         | Ringkas materi         |
| GET    | `/api/ai/history/{user_id}` | Riwayat chat user      |
| GET    | `/api/materials/`           | Daftar materi          |
| POST   | `/api/materials/upload`     | Upload file materi     |
| DELETE | `/api/materials/{id}`       | Hapus materi           |

## Contoh Request

### POST /api/ai/ask

```json
{
  "question": "Apa itu integral?",
  "subject": "Matematika",
  "user_id": 1
}
```

### POST /api/ai/quiz/generate

```json
{
  "subject": "Fisika",
  "topic": "Gerak Lurus",
  "num_questions": 5
}
```

### POST /api/materials/upload

Form-data:

- title: "Materi Integral"
- subject: "Matematika"
- description: "Bab 3"
- file: (file PDF/JPG/PNG)
