from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routers import ai, materials

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EduAI API",
    description="Platform pembelajaran adaptif dengan AI tutor (Groq LLaMA)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://18.143.96.4",
                   "http://18.143.96.4:80", 
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router)
app.include_router(materials.router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "EduAI Backend",
        "ai_provider": "Groq (LLaMA 3.3 70B)"
    }