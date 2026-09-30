from .gemini_client import generate_text

def get_learning_recommendations(topic:str,level:str='beginner')->str:
    return generate_text(f'''Create a structured learning path for "{topic}". Learner level: {level}. Organize: prerequisites, beginner, intermediate, advanced, timeline, practice/projects, revision strategy, and trusted resource types. Explain why each stage matters. Do not invent URLs.''',1500,0.4)
