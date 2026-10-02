from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_home():
    r = client.get("/")
    assert r.status_code == 200
    assert "EduGenie" in r.text
    assert "Learning Hub" in r.text

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "ok"
    assert data["service"] == "EduGenie"
    assert "database" in data

def test_docs():
    r = client.get("/docs")
    assert r.status_code == 200

def test_validation():
    # Less than 3 characters should be rejected with 422 Unprocessable Entity
    r = client.post("/qa", json={"text": "hi"})
    assert r.status_code == 422

def test_qa_endpoint():
    r = client.post("/qa", json={"text": "What is the difference between TCP and UDP?"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert len(data["result"]) > 10
    assert "history_id" in data

def test_explain_endpoint():
    r = client.post("/explain", json={"text": "TCP three-way handshake", "level": "beginner"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert len(data["result"]) > 10
    assert "history_id" in data

def test_quiz_endpoint():
    r = client.post("/quiz", json={"text": "Computer Networks and the OSI Model"})
    assert r.status_code == 200
    data = r.json()
    assert "quiz" in data
    quiz = data["quiz"]
    assert isinstance(quiz, list)
    assert len(quiz) >= 2
    for q in quiz:
        assert "question" in q
        assert "options" in q
        assert len(q["options"]) == 4
        assert "correct_answer" in q
        assert q["correct_answer"] in q["options"]

def test_summarize_endpoint():
    passage = "Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so."
    r = client.post("/summarize", json={"text": passage})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert len(data["result"]) > 10

def test_learning_path_endpoint():
    r = client.post("/learn/recommendations", json={"topic": "Python Programming", "level": "beginner"})
    assert r.status_code == 200
    data = r.json()
    assert "result" in data
    assert "Roadmap" in data["result"] or "Learning" in data["result"]

def test_history_and_bookmarks():
    # Fetch history
    r = client.get("/api/history")
    assert r.status_code == 200
    history = r.json()["history"]
    assert len(history) > 0
    item_id = history[0]["id"]

    # Toggle bookmark
    r_bm = client.post(f"/api/history/{item_id}/bookmark")
    assert r_bm.status_code == 200
    assert "is_bookmarked" in r_bm.json()

    # Get bookmarks
    r_bms = client.get("/api/bookmarks")
    assert r_bms.status_code == 200

    # Delete history item
    r_del = client.delete(f"/api/history/{item_id}")
    assert r_del.status_code == 200
    assert r_del.json()["success"] is True

def test_quiz_submission_and_scoring():
    payload = {
        "topic": "Computer Science Basics",
        "answers": [
            {
                "question": "What does CPU stand for?",
                "selected_answer": "Central Processing Unit",
                "correct_answer": "Central Processing Unit",
                "explanation": "CPU is the central processing unit of a computer."
            },
            {
                "question": "Which of these is a database?",
                "selected_answer": "HTML",
                "correct_answer": "PostgreSQL",
                "explanation": "PostgreSQL is a relational database management system."
            }
        ]
    }
    r = client.post("/api/quiz/submit", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["total_questions"] == 2
    assert data["score"] == 1
    assert data["percentage"] == 50.0
    assert len(data["breakdown"]) == 2

    # Verify quiz history reflects the attempt
    r_hist = client.get("/api/quiz/history")
    assert r_hist.status_code == 200
    assert len(r_hist.json()["attempts"]) > 0

def test_study_notes_crud():
    # Create note
    payload = {
        "title": "Algorithms Revision",
        "content": "Quicksort has average complexity O(n log n) and worst-case O(n^2).",
        "category": "Data Structures"
    }
    r_create = client.post("/api/notes", json=payload)
    assert r_create.status_code == 200
    note = r_create.json()["note"]
    note_id = note["id"]

    # Read notes
    r_get = client.get("/api/notes")
    assert r_get.status_code == 200
    notes = r_get.json()["notes"]
    assert any(n["id"] == note_id for n in notes)

    # Delete note
    r_del = client.delete(f"/api/notes/{note_id}")
    assert r_del.status_code == 200
    assert r_del.json()["success"] is True

def test_stats_and_config():
    r_stats = client.get("/api/stats")
    assert r_stats.status_code == 200
    stats = r_stats.json()
    assert "total_queries" in stats
    assert "total_quizzes_taken" in stats
    assert "task_breakdown" in stats

    r_cfg = client.get("/api/config")
    assert r_cfg.status_code == 200
    cfg = r_cfg.json()
    assert "features" in cfg
    assert "database" in cfg
