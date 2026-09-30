from .config import LOCAL_EXPLANATION_MODEL, USE_LOCAL_EXPLANATION
from .gemini_client import generate_text
_local_pipeline=None

def _local_explain(topic:str)->str:
    global _local_pipeline
    from transformers import pipeline
    if _local_pipeline is None:
        _local_pipeline=pipeline('text2text-generation',model=LOCAL_EXPLANATION_MODEL)
    result=_local_pipeline('Explain for a beginner with an analogy and example: '+topic,max_new_tokens=350,do_sample=False)
    return result[0]['generated_text'].strip()

def explain_concept(topic:str)->str:
    if USE_LOCAL_EXPLANATION:
        try: return _local_explain(topic)
        except Exception: pass
    return generate_text(f'''Explain this concept for a beginner: {topic}\nUse: 1. Simple definition 2. Step-by-step explanation 3. Real-world analogy 4. Small example 5. Key points. Use clear language.''',1200,0.35)
