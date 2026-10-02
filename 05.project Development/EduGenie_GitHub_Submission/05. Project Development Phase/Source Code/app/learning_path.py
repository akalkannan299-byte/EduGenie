from .gemini_client import generate_text

def get_learning_recommendations(topic: str, level: str = "beginner") -> str:
    prompt = f'''Create a comprehensive, step-by-step personalized learning roadmap for:
Topic: "{topic}"
Current Learner Level: {level}

Format your response in rich GitHub Markdown:
# 🗺️ Master Learning Roadmap: {topic}

### 🎯 Essential Prerequisites
- Key fundamentals students should know before diving in.

### 🟢 Stage 1: Foundations (Week 1–2)
- **Core Topics**: Core concepts, terminology, syntax.
- **Hands-on Milestone**: A starter project or practical exercise.

### 🟡 Stage 2: Intermediate Application (Week 3–5)
- **Core Topics**: Deeper patterns, integration, libraries, problem-solving.
- **Hands-on Milestone**: A realistic mini-project.

### 🔴 Stage 3: Advanced Mastery (Week 6–8)
- **Core Topics**: Architecture, optimization, best practices, edge cases.
- **Hands-on Milestone**: A portfolio-ready capstone project.

### ⏱️ Recommended Study Routine & Spaced Repetition
- Daily schedule recommendation and active recall strategies.

### 📚 Trusted Resource Categories
- Suggested documentation types, official specs, and practice platforms (no fictitious links).'''

    return generate_text(prompt, max_output_tokens=1800, temperature=0.4)
