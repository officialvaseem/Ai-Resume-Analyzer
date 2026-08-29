from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from database import SessionLocal, AnalysisHistory
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import io
import re

app = FastAPI()

@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).all()
    db.close()
    return [
        {
            "id": r.id,
            "filename": r.filename,
            "match_score_percent": r.match_score,
            "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills,
            "created_at": r.created_at.isoformat()
        }
        for r in records
    ]
@app.delete("/history")
def clear_history():
    db = SessionLocal()
    db.query(AnalysisHistory).delete()
    db.commit()
    db.close()
    return {"message": "History cleared successfully"}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# A curated list of common tech skills/tools to check for.
# Add more as you like!
SKILLS_DB = [
    "python", "java", "javascript", "typescript", "c++", "c#", "sql", "nosql",
    "mysql", "postgresql", "mongodb", "redis", "html", "css", "react", "angular",
    "vue", "node.js", "node", "express", "django", "flask", "fastapi", "spring",
    "springboot", "mybatis", "springcloud", "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp", "linux", "rest", "api", "apis", "graphql", "machine learning",
    "deep learning", "nlp", "llm", "llms", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "data structures", "algorithms", "oop", "agile", "scrum",
    "ci/cd", "jenkins", "terraform", "microservices", "unit testing", "debugging"

    # HR / Talent Acquisition
    "recruitment", "sourcing", "onboarding", "ats", "talent acquisition",
    "employee relations", "hrms", "payroll", "performance management",
    "workforce planning", "interviewing", "screening", "hr policies",

    # Marketing / Sales
    "seo", "sem", "content marketing", "social media", "google analytics",
    "crm", "salesforce", "lead generation", "email marketing", "branding",
    "market research", "negotiation", "cold calling", "b2b", "b2c",

    # Finance / Accounting
    "excel", "financial modeling", "budgeting", "forecasting", "accounting",
    "auditing", "taxation", "gst", "bookkeeping", "quickbooks", "sap",

    # General/soft skills
    "communication", "leadership", "teamwork", "project management",
    "problem solving", "time management", "presentation", "stakeholder management"
]

@app.get("/")
def read_root():
    return {"message": "Resume Analyzer API is running!"}

def extract_skills(text: str):
    """Find which known skills from SKILLS_DB appear in the text."""
    text_lower = text.lower()
    found = set()
    for skill in SKILLS_DB:
        # Use word boundaries so "java" doesn't match inside "javascript"
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill)
    return found

def extract_general_keywords(text: str):
    """Fallback: extract meaningful generic keywords when few known skills are found."""
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    keywords = [w for w in words if w not in ENGLISH_STOP_WORDS]
    return set(keywords)

@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    pdf_bytes = await resume.read()
    pdf_file = io.BytesIO(pdf_bytes)
    reader = PdfReader(pdf_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_description])
    match_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    score_percent = round(match_score * 100, 2)

    jd_skills = extract_skills(job_description)
    resume_skills = extract_skills(resume_text)
    if len(jd_skills)<3:
        jd_skills=extract_general_keywords(job_description)
        resume_skills= extract_skills(resume_text)
    missing_skills = list(jd_skills - resume_skills)
    matched_skills = list(jd_skills & resume_skills)

    # Save analysis result to database
    db = SessionLocal()
    record = AnalysisHistory(
        filename=resume.filename,
        match_score=score_percent,
        matched_skills=", ".join(matched_skills),
        missing_skills=", ".join(missing_skills)
    )
    db.add(record)
    db.commit()
    db.close()

    return {
        "filename": resume.filename,
        "match_score_percent": score_percent,
        "matched_skills": matched_skills[:20],
        "missing_skills": missing_skills[:20],
        "resume_text_length": len(resume_text)
    }