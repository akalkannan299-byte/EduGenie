from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router
BASE_DIR=Path(__file__).resolve().parent.parent
app=FastAPI(title='EduGenie – Google Gemini Powered Learning Assistant',version='1.0.0')
app.mount('/static',StaticFiles(directory=BASE_DIR/'static'),name='static')
app.include_router(router)
