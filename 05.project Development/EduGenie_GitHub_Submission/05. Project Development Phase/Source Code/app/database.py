import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DATABASE_URL, BASE_DIR

# Normalize sqlite path so it is always relative to the project base directory
db_url = DATABASE_URL
if db_url.startswith("sqlite:///") and not db_url.startswith("sqlite:////"):
    rel_path = db_url.replace("sqlite:///", "")
    db_file = (BASE_DIR / rel_path).resolve()
    db_url = f"sqlite:///{db_file}"

engine = create_engine(
    db_url,
    connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
