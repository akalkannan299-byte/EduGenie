# EduGenie – User Guide

## 1. Prerequisites
- **Python**: Version 3.10 or higher.
- **Web Browser**: Chrome, Edge, Firefox, or Safari.

## 2. Quick Setup

### Option A: From Repository Root
```bash
# Install dependencies
pip install -r "05. Project Development Phase/Source Code/requirements.txt"

# Run the app
python run.py
```

### Option B: From the Source Code Folder
```bash
cd "05. Project Development Phase/Source Code"

# Create a virtual environment
python -m venv venv

# Activate on Windows:
venv\Scripts\activate
# Activate on macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the application
python run.py
# Or: uvicorn app.main:app --reload
```

## 3. Configuring Google Gemini AI
Open `.env` in `05. Project Development Phase/Source Code/`:
```ini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=sqlite:///./edugenie.db
DEMO_MODE=auto
```
- Obtain a free Gemini API key at: [https://aistudio.google.com/](https://aistudio.google.com/)
- If `GOOGLE_API_KEY` is not provided, EduGenie automatically operates in **Demo Mode**, generating structured offline educational responses so all features remain testable!

## 4. Using the Web Interface
Navigate to `http://127.0.0.1:8000` in your web browser.

### 💡 Learning Hub
- Select a learning task: **Ask a Question**, **Explain Concept**, or **Summarize Text**.
- For concept explanations, choose the learner target level: **Beginner**, **Intermediate**, or **Advanced**.
- Click quick suggestion chips or use the **🎤 Microphone** button to dictate your question.
- Click **Generate with AI** to view formatted answers.
- Use **🔊 Listen** to hear the response read aloud, **📋 Copy** to copy it, **⭐ Bookmark** to save it, or **💾 Save to Notes** to store it in your database.

### 🎯 Quiz Arena
- Enter any topic (e.g. *Computer Networks*, *Python OOP*) or paste study text.
- Click **Generate Quiz** to create practice MCQs.
- Select your answers and click **Submit Quiz & See Score** to receive your percentage, pass/fail status, and explanation for every answer.
- Review your score trajectory in the **Quiz Performance History** table below.

### 🗺️ Learning Paths
- Enter a skill (e.g. *Full Stack Web Development*, *Machine Learning*) and select your current experience level.
- Click **Create Learning Path** to receive a structured roadmap with milestones and project assignments.
- Save the roadmap directly to your study notes with one click.

### 📚 Study Notes & Activity History
- **Activity History**: Browse, search, copy, or delete previous queries.
- **Bookmarks**: Quickly access all starred responses.
- **Study Notes**: Create, edit, and organize custom notes with category tags.

### 📊 Analytics Dashboard
- View total queries generated, completed quizzes, average quiz score, and task breakdown charts.

## 5. API Documentation
Access Swagger UI at `http://127.0.0.1:8000/docs` to test endpoints directly.

## 6. Running Tests
```bash
pytest
```
Verifies all 13 automated test cases covering endpoints, validation, database CRUD, and quiz grading.