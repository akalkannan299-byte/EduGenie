import json
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import HistoryItem, QuizAttempt, StudyNote

def create_history(db: Session, task_type: str, input_text: str, output_result: str) -> HistoryItem:
    item = HistoryItem(
        task_type=task_type,
        input_text=input_text,
        output_result=output_result,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_history(
    db: Session,
    task_type: Optional[str] = None,
    bookmarked_only: bool = False,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
) -> List[HistoryItem]:
    q = db.query(HistoryItem)
    if task_type and task_type != "all":
        q = q.filter(HistoryItem.task_type == task_type)
    if bookmarked_only:
        q = q.filter(HistoryItem.is_bookmarked.is_(True))
    if search:
        search_filter = f"%{search}%"
        q = q.filter(
            HistoryItem.input_text.ilike(search_filter) |
            HistoryItem.output_result.ilike(search_filter)
        )
    return q.order_by(HistoryItem.id.desc()).offset(offset).limit(limit).all()

def delete_history_item(db: Session, item_id: int) -> bool:
    item = db.query(HistoryItem).filter(HistoryItem.id == item_id).first()
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True

def clear_history(db: Session) -> int:
    deleted = db.query(HistoryItem).delete()
    db.commit()
    return deleted

def toggle_bookmark(db: Session, item_id: int) -> Optional[HistoryItem]:
    item = db.query(HistoryItem).filter(HistoryItem.id == item_id).first()
    if not item:
        return None
    item.is_bookmarked = not item.is_bookmarked
    db.commit()
    db.refresh(item)
    return item

def get_bookmarks(db: Session, limit: int = 50) -> List[HistoryItem]:
    return db.query(HistoryItem).filter(HistoryItem.is_bookmarked.is_(True)).order_by(HistoryItem.id.desc()).limit(limit).all()

def create_quiz_attempt(db: Session, topic: str, score: int, total_questions: int, answers_detail: list) -> QuizAttempt:
    pct = (score / total_questions * 100.0) if total_questions > 0 else 0.0
    attempt = QuizAttempt(
        topic=topic,
        score=score,
        total_questions=total_questions,
        percentage=pct,
        answers_json=json.dumps(answers_detail),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt

def get_quiz_attempts(db: Session, limit: int = 20) -> List[QuizAttempt]:
    return db.query(QuizAttempt).order_by(QuizAttempt.id.desc()).limit(limit).all()

def create_note(db: Session, title: str, content: str, category: str = "General") -> StudyNote:
    note = StudyNote(
        title=title,
        content=content,
        category=category,
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

def get_notes(db: Session, limit: int = 50) -> List[StudyNote]:
    return db.query(StudyNote).order_by(StudyNote.id.desc()).limit(limit).all()

def delete_note(db: Session, note_id: int) -> bool:
    note = db.query(StudyNote).filter(StudyNote.id == note_id).first()
    if not note:
        return False
    db.delete(note)
    db.commit()
    return True

def get_stats(db: Session) -> dict:
    total_history = db.query(func.count(HistoryItem.id)).scalar() or 0
    total_bookmarks = db.query(func.count(HistoryItem.id)).filter(HistoryItem.is_bookmarked.is_(True)).scalar() or 0
    total_notes = db.query(func.count(StudyNote.id)).scalar() or 0
    total_quizzes = db.query(func.count(QuizAttempt.id)).scalar() or 0
    avg_quiz_score = db.query(func.avg(QuizAttempt.percentage)).scalar() or 0.0

    task_breakdown = {}
    for task, count in db.query(HistoryItem.task_type, func.count(HistoryItem.id)).group_by(HistoryItem.task_type).all():
        task_breakdown[task] = count

    return {
        "total_queries": total_history,
        "total_bookmarks": total_bookmarks,
        "total_notes": total_notes,
        "total_quizzes_taken": total_quizzes,
        "average_quiz_score": round(float(avg_quiz_score), 1),
        "task_breakdown": task_breakdown,
    }
