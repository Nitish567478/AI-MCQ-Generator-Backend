from pydantic import BaseModel
from typing import List, Dict
from app.schemas.question import QuestionBase

class QuizCreate(BaseModel):
    url: str

class QuizResponse(BaseModel):
    id: int
    url: str
    title: str
    summary: str
    sections: List[str]
    key_entities: Dict
    related_topics: List[str]
    quiz: List[QuestionBase]

    class Config:
        orm_mode = True
