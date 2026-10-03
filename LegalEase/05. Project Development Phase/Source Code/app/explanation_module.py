from .config import LOCAL_EXPLANATION_MODEL, USE_LOCAL_EXPLANATION
from .gemini_client import generate_text

_local_pipeline = None

def _local_explain(topic: str) -> str:
    global _local_pipeline
    from transformers import pipeline
    if _local_pipeline is None:
        _local_pipeline = pipeline('text2text-generation', model=LOCAL_EXPLANATION_MODEL)
    result = _local_pipeline('Explain for a beginner with an analogy and example: ' + topic, max_new_tokens=350, do_sample=False)
    return result[0]['generated_text'].strip()

def explain_concept(topic: str, level: str = "beginner") -> str:
    if USE_LOCAL_EXPLANATION:
        try:
            return _local_explain(topic)
        except Exception:
            pass

    prompt = f'''Explain the concept of "{topic}" tailored for a {level} learner.
Use clear Markdown formatting with headers and bullet points:
### 📘 1. Simple Definition
### 🔍 2. Step-by-Step Breakdown
### 💡 3. Real-World Analogy
### 💻 4. Practical Code or Real-Life Example
### 🔑 5. Key Takeaways & Common Pitfalls

Use engaging, educational language suitable for a {level} student.'''

    return generate_text(prompt, max_output_tokens=1400, temperature=0.35)
