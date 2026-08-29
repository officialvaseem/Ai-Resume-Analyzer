# 📄 AI Resume Analyzer & ATS Optimizer

A full-stack web application that analyzes resumes against job descriptions, providing a match score and highlighting matched/missing skills — helping candidates optimize their resumes for both tech and non-tech roles.

## Features

- 📤 Upload a resume (PDF) and paste any job description
- 🎯 Get an instant match score using TF-IDF and cosine similarity
- ✅ See matched skills and ❌ missing skills, tailored to tech, HR, marketing, and finance roles
- 📊 View analysis history stored in a local database
- 🎨 Clean, modern, responsive UI

## Tech Stack

- **Backend:** Python, FastAPI, scikit-learn, pypdf, SQLAlchemy
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript (no frameworks)

## How It Works

1. The backend extracts raw text from the uploaded PDF resume
2. TF-IDF vectorization converts both the resume and job description into numerical vectors
3. Cosine similarity measures how closely they match, producing a percentage score
4. A curated skills database (covering tech, HR, marketing, and finance) is checked against both texts to find matched and missing skills
5. Every analysis is saved to a SQLite database for future reference

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate      # Windows
pip install fastapi uvicorn pypdf scikit-learn sqlalchemy python-multipart
uvicorn main:app --reload
```
