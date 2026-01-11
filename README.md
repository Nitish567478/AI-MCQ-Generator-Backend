
---

# 📄 BACKEND README.md

**File:** `backend/README.md`

```md
# Backend – AI Wiki Quiz Generator

This backend uses FastAPI to fetch Wikipedia content and generate MCQ quizzes.

## Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn requests

## Run
uvicorn app.main:app --reload
