from fastapi import APIRouter,HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel,Field
from .explanation_module import explain_concept
from .learning_path import get_learning_recommendations
from .qna import answer_question
from .quiz_module import generate_quiz
from .summary_module import summarize_text
router=APIRouter(); templates=Jinja2Templates(directory='templates')
class TextRequest(BaseModel): text:str=Field(min_length=3,max_length=15000)
class LearningPathRequest(BaseModel): topic:str=Field(min_length=2,max_length=300); level:str=Field(default='beginner',min_length=2,max_length=50)
@router.get('/',response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse(request=request,name='index.html')
@router.get('/health')
def health(): return {'status':'ok','service':'EduGenie'}
def _run(fn,payload):
    try: return fn(payload)
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))
@router.post('/qa')
def qa(p:TextRequest): return {'result':_run(answer_question,p.text)}
@router.post('/explain')
def explain(p:TextRequest): return {'result':_run(explain_concept,p.text)}
@router.post('/quiz')
def quiz(p:TextRequest): return {'quiz':_run(generate_quiz,p.text)}
@router.post('/summarize')
def summarize(p:TextRequest): return {'result':_run(summarize_text,p.text)}
@router.post('/learn/recommendations')
def learn(p:LearningPathRequest):
    try: return {'result':get_learning_recommendations(p.topic,p.level)}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))
