
from src.question.models import Question

def create_question(body, db, user):
    question = Question(
        interview_id=body.interview_id,
        question_text=body.question_text,
        expected_answer=body.expected_answer
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question