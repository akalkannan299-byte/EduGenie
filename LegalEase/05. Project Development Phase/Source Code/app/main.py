from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routes import router

BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure tables are created immediately
init_db()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title='EduGenie – Google Gemini Powered Learning Assistant',
    description='Intelligent AI Learning Assistant with Q&A, Concept Explanations, Interactive Quizzes, Summaries, and Personalized Roadmaps.',
    version='1.0.0',
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static', StaticFiles(directory=str(BASE_DIR / 'static')), name='static')
app.include_router(router)
