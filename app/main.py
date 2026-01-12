from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.quiz import router as quiz_router

app = FastAPI()

# 🔥 CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-mcq-generator-seven.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quiz_router, prefix="/api/quiz")
