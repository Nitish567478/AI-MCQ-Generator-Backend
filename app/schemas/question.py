from pydantic import BaseModel
from typing import List

class QuestionBase(BaseModel):
    question: str
    options: List[str]
    answer: str
    difficulty: str
    explanation: str

    class Config:
        orm_mode = True
