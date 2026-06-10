from groq import Groq
from app.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)

TUTOR_SYSTEM_PROMPT = """Kamu adalah EduAI, asisten tutor cerdas untuk platform pembelajaran Indonesia.
Tugasmu membantu siswa SMA memahami materi pelajaran dengan cara:
- Penjelasan yang jelas, bertahap, dan mudah dipahami
- Gunakan analogi atau contoh nyata yang relevan dengan kehidupan siswa Indonesia
- Berikan pertanyaan balik untuk mendorong siswa berpikir kritis
- Gunakan Bahasa Indonesia yang baik, ramah, dan tidak kaku
Jika siswa bertanya di luar konteks pelajaran, arahkan kembali dengan sopan."""

async def ask_tutor(question: str, subject: str, chat_history: list = []) -> str:
    messages = [{"role": "system", "content": TUTOR_SYSTEM_PROMPT}]
    for h in chat_history[-6:]:
        messages.append({"role": "user", "content": h["question"]})
        messages.append({"role": "assistant", "content": h["answer"]})
    messages.append({
        "role": "user",
        "content": f"Mata pelajaran: {subject}\n\nPertanyaan siswa: {question}"
    })
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        max_tokens=1024,
        temperature=0.7,
    )
    return response.choices[0].message.content

async def generate_quiz(subject: str, topic: str, num_questions: int = 5) -> dict:
    prompt = f"""Buat {num_questions} soal pilihan ganda untuk:
- Mata pelajaran: {subject}
- Topik: {topic}
- Tingkat: SMA

PENTING: Kembalikan HANYA JSON murni, tanpa teks pengantar, tanpa markdown, tanpa backtick.

Format JSON:
{{
    "subject": "{subject}",
    "topic": "{topic}",
    "questions": [
        {{
            "id": 1,
            "question": "teks soal",
            "options": {{"A": "...", "B": "...", "C": "...", "D": "..."}},
            "correct_answer": "A",
            "explanation": "penjelasan"
        }}
    ]
}}"""
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2048,
        temperature=0.3,
    )
    import json
    raw_text = response.choices[0].message.content.strip()
    if raw_text.startswith("```"):
        raw_text = raw_text.split("```")[1]
        if raw_text.startswith("json"):
            raw_text = raw_text[4:]
    return json.loads(raw_text)

async def summarize_material(text: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[{
            "role": "user",
            "content": f"Ringkas materi berikut dalam poin penting (Bahasa Indonesia):\n\n{text}"
        }],
        max_tokens=512,
        temperature=0.5,
    )
    return response.choices[0].message.content