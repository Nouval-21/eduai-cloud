from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import ChatHistory
from app.services.ai_service import ask_tutor, generate_quiz, summarize_material

router = APIRouter(prefix="/api/ai", tags=["AI Tutor"])

class AskRequest(BaseModel):
    question: str
    subject: str
    user_id: int = 1

class QuizRequest(BaseModel):
    subject: str
    topic: str
    num_questions: int = 5

class SummarizeRequest(BaseModel):
    text: str

@router.post("/ask")
async def ask_question(req: AskRequest, db: Session = Depends(get_db)):
    from app.models.models import User
    user = db.query(User).filter(User.id == req.user_id).first()
    if not user:
        user = User(id=req.user_id, username=f"user_{req.user_id}", email=f"user_{req.user_id}@eduai.com", hashed_password="dummy_hash")
        db.add(user)
        db.commit()

    history = db.query(ChatHistory)\
        .filter(ChatHistory.user_id == req.user_id)\
        .order_by(ChatHistory.created_at.desc())\
        .limit(6).all()
    history_list = [
        {"question": h.question, "answer": h.answer}
        for h in reversed(history)
    ]
    try:
        answer = await ask_tutor(req.question, req.subject, history_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Error: {str(e)}")
    chat = ChatHistory(
        user_id=req.user_id,
        subject=req.subject,
        question=req.question,
        answer=answer
    )
    db.add(chat)
    db.commit()
    return {"answer": answer, "subject": req.subject, "question": req.question}

@router.post("/quiz/generate")
async def create_quiz(req: QuizRequest):
    try:
        quiz = await generate_quiz(req.subject, req.topic, req.num_questions)
        return quiz
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {str(e)}")

@router.post("/summarize")
async def summarize(req: SummarizeRequest):
    try:
        summary = await summarize_material(req.text)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}")
def get_history(user_id: int, db: Session = Depends(get_db)):
    history = db.query(ChatHistory)\
        .filter(ChatHistory.user_id == user_id)\
        .order_by(ChatHistory.created_at.desc())\
        .limit(20).all()
    return [
        {"id": h.id, "subject": h.subject, "question": h.question,
         "answer": h.answer, "created_at": h.created_at}
        for h in history
    ]