from .gemini_client import generate_text

def summarize_text(text:str)->str:
    return generate_text(f'''Summarize this educational passage for quick revision. Keep important facts, remove repetition, use simple language and short bullets. Do not add unsupported facts.\nPASSAGE:\n{text}''',1000,0.3)
