from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# SQLite database file — will be created automatically in the backend folder
DATABASE_URL = "sqlite:///./resume_analyzer.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    match_score = Column(Float)
    matched_skills = Column(String)   # stored as comma-separated text
    missing_skills = Column(String)   # stored as comma-separated text
    created_at = Column(DateTime, default=datetime.utcnow)

# Create the table if it doesn't exist yet
Base.metadata.create_all(bind=engine)