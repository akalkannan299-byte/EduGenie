from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Float
from .database import Base

def utc_now():
    return datetime.now(timezone.utc)

class HistoryItem(Base):
    __tablename__ = "history_items"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(String(50), index=True)  # qa, explain, quiz, summarize, learn
    input_text = Column(Text, nullable=False)
    output_result = Column(Text, nullable=False)
    is_bookmarked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "task_type": self.task_type,
            "input_text": self.input_text,
            "output_result": self.output_result,
            "is_bookmarked": self.is_bookmarked,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
        }

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    percentage = Column(Float, nullable=False)
    answers_json = Column(Text, nullable=True)  # JSON-encoded array of questions and user choices
    created_at = Column(DateTime(timezone=True), default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "score": self.score,
            "total_questions": self.total_questions,
            "percentage": round(self.percentage, 1),
            "answers_json": self.answers_json,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
        }

class StudyNote(Base):
    __tablename__ = "study_notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), default="General")
    created_at = Column(DateTime(timezone=True), default=utc_now)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else "",
        }
