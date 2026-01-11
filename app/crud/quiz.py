from sqlalchemy.orm import Session
from app.models.quiz import Quiz
from app.models.question import Question

def get_quiz_by_url(db: Session, url: str):
    return db.query(Quiz).filter(Quiz.url == url).first()

def create_quiz(db: Session, quiz_data, questions):
    quiz = Quiz(**quiz_data)
    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    for q in questions:
        question = Question(quiz_id=quiz.id, **q)
        db.add(question)

    db.commit()
    return quiz
