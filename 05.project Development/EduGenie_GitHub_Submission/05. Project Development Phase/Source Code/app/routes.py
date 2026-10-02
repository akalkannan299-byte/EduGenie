import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from .config import BASE_DIR, GEMINI_MODEL
from .database import get_db
from .gemini_client import is_api_configured
from . import crud
from .explanation_module import explain_concept
from .learning_path import get_learning_recommendations
from .qna import answer_question
from .quiz_module import generate_quiz
from .summary_module import summarize_text

router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# --- Pydantic Schemas ---
class TextRequest(BaseModel):
    text: str = Field(min_length=3, max_length=15000)
    level: Optional[str] = Field(default="beginner", max_length=50)

class LearningPathRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=300)
    level: str = Field(default="beginner", min_length=2, max_length=50)

class QuizAnswerItem(BaseModel):
    question: str
    selected_answer: str
    correct_answer: str
    explanation: Optional[str] = ""

class QuizSubmitRequest(BaseModel):
    topic: str = Field(default="General Quiz", max_length=255)
    answers: List[QuizAnswerItem]

class NoteCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=50000)
    category: Optional[str] = Field(default="General", max_length=100)

# --- Web UI Route ---
@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"ai_configured": is_api_configured(), "model_name": GEMINI_MODEL}
    )

# --- Health Check Route ---
@router.get("/health")
def health():
    return {
        "status": "ok",
        "service": "EduGenie",
        "version": "1.0.0",
        "model": GEMINI_MODEL,
        "ai_live": is_api_configured(),
        "database": "sqlite",
    }

# --- Core AI Operations (Backward compatible with project design) ---
@router.post("/qa")
def qa(p: TextRequest, db: Session = Depends(get_db)):
    try:
        ans = answer_question(p.text)
        item = crud.create_history(db, task_type="qa", input_text=p.text, output_result=ans)
        return {"result": ans, "history_id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
def explain(p: TextRequest, db: Session = Depends(get_db)):
    try:
        res = explain_concept(p.text, level=p.level or "beginner")
        item = crud.create_history(db, task_type="explain", input_text=p.text, output_result=res)
        return {"result": res, "history_id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/quiz")
def quiz(p: TextRequest, db: Session = Depends(get_db)):
    try:
        data = generate_quiz(p.text)
        item = crud.create_history(db, task_type="quiz", input_text=p.text, output_result=json.dumps(data))
        return {"quiz": data, "history_id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
def summarize(p: TextRequest, db: Session = Depends(get_db)):
    try:
        summary = summarize_text(p.text)
        item = crud.create_history(db, task_type="summarize", input_text=p.text, output_result=summary)
        return {"result": summary, "history_id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/learn/recommendations")
def learn(p: LearningPathRequest, db: Session = Depends(get_db)):
    try:
        path = get_learning_recommendations(p.topic, p.level)
        item = crud.create_history(db, task_type="learn", input_text=f"{p.topic} ({p.level})", output_result=path)
        return {"result": path, "history_id": item.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Database & History APIs ---
@router.get("/api/history")
def get_history(
    task_type: Optional[str] = Query(None),
    bookmarked_only: bool = Query(False),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    items = crud.get_history(db, task_type=task_type, bookmarked_only=bookmarked_only, search=search, limit=limit, offset=offset)
    return {"history": [x.to_dict() for x in items]}

@router.delete("/api/history/{item_id}")
def delete_history_item(item_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_history_item(db, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail="History item not found")
    return {"success": True, "message": f"Item {item_id} deleted"}

@router.delete("/api/history")
def clear_history(db: Session = Depends(get_db)):
    deleted = crud.clear_history(db)
    return {"success": True, "deleted_count": deleted}

@router.post("/api/history/{item_id}/bookmark")
def toggle_bookmark(item_id: int, db: Session = Depends(get_db)):
    item = crud.toggle_bookmark(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="History item not found")
    return {"success": True, "is_bookmarked": item.is_bookmarked}

@router.get("/api/bookmarks")
def get_bookmarks(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    items = crud.get_bookmarks(db, limit=limit)
    return {"bookmarks": [x.to_dict() for x in items]}

# --- Quiz Submission & Progress Tracking ---
@router.post("/api/quiz/submit")
def submit_quiz(submission: QuizSubmitRequest, db: Session = Depends(get_db)):
    total = len(submission.answers)
    if total == 0:
        raise HTTPException(status_code=400, detail="Cannot submit empty quiz")

    score = 0
    breakdown = []
    for item in submission.answers:
        is_correct = item.selected_answer.strip().lower() == item.correct_answer.strip().lower()
        if is_correct:
            score += 1
        breakdown.append({
            "question": item.question,
            "selected_answer": item.selected_answer,
            "correct_answer": item.correct_answer,
            "is_correct": is_correct,
            "explanation": item.explanation
        })

    pct = round((score / total) * 100.0, 1)
    attempt = crud.create_quiz_attempt(db, topic=submission.topic, score=score, total_questions=total, answers_detail=breakdown)

    return {
        "attempt_id": attempt.id,
        "topic": submission.topic,
        "score": score,
        "total_questions": total,
        "percentage": pct,
        "passed": pct >= 60.0,
        "breakdown": breakdown,
    }

@router.get("/api/quiz/history")
def get_quiz_history(limit: int = Query(20, ge=1, le=50), db: Session = Depends(get_db)):
    attempts = crud.get_quiz_attempts(db, limit=limit)
    return {"attempts": [a.to_dict() for a in attempts]}

# --- Study Notes APIs ---
@router.get("/api/notes")
def get_notes(limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)):
    notes = crud.get_notes(db, limit=limit)
    return {"notes": [n.to_dict() for n in notes]}

@router.post("/api/notes")
def create_note(payload: NoteCreateRequest, db: Session = Depends(get_db)):
    note = crud.create_note(db, title=payload.title, content=payload.content, category=payload.category or "General")
    return {"success": True, "note": note.to_dict()}

@router.delete("/api/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_note(db, note_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Study note not found")
    return {"success": True, "message": f"Note {note_id} deleted"}

# --- Analytics & Stats ---
@router.get("/api/stats")
def get_learning_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)

@router.get("/api/config")
def get_system_config():
    return {
        "model": GEMINI_MODEL,
        "ai_live": is_api_configured(),
        "database": "SQLite (edugenie.db)",
        "features": [
            "Question & Answer",
            "Concept Explanation with Learner Levels",
            "Interactive Quiz Generator & Scoring",
            "Text Summarizer for Quick Revision",
            "Personalized Learning Path Roadmaps",
            "Study Notes & Bookmarking",
            "Interactive Progress & Performance Analytics"
        ]
    }
