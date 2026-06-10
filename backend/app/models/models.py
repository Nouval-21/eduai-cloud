from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chat_histories = relationship("ChatHistory", back_populates="user")
    quiz_attempts = relationship("QuizAttempt", back_populates="user")

class Material(Base):
    __tablename__ = "materials"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    description = Column(Text)
    file_key = Column(String)
    file_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class ChatHistory(Base):
    __tablename__ = "chat_histories"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="chat_histories")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(String)
    score = Column(Float)
    total_questions = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="quiz_attempts")