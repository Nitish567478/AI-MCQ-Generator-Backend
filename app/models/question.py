from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    question = Column(String)
    answer = Column(String)
