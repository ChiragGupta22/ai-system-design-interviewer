
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.models import Question, ExpectedConcept
from src.answer.model import Answer
from src.interview.models import Interview

from src.evaluation.bi_encoder import (
    evaluate_answer as evaluate_groq
)


def create_answer(body, db: Session, user):
    try:
        question = (
            db.query(Question)
            .filter(Question.id == body.question_id)
            .first()
        )

        if not question:
            raise HTTPException(
                status_code=404,
                detail="Question not found"
            )

        interview = (
            db.query(Interview)
            .filter(
                Interview.id == question.interview_id,
                Interview.user_id == user.id
            )
            .first()
        )

        if not interview:
            raise HTTPException(
                status_code=403,
                detail="You cannot answer this question"
            )

        existing_answer = (
            db.query(Answer)
            .filter(
                Answer.question_id == question.id,
                Answer.user_id == user.id
            )
            .first()
        )

        if existing_answer:
            raise HTTPException(
                status_code=409,
                detail="You have already answered this question"
            )

        expected_answer = question.expected_answer

        if not expected_answer or not expected_answer.strip():
            raise HTTPException(
                status_code=422,
                detail="Expected answer is not available"
            )

        candidate_answer = body.answer_text.strip()

        if not candidate_answer:
            raise HTTPException(
                status_code=422,
                detail="Answer cannot be empty"
            )

        concepts = (
            db.query(ExpectedConcept)
            .filter(
                ExpectedConcept.question_id == question.id
            )
            .all()
        )

        expected_concepts = [
            item.concept for item in concepts
        ]

        # Evaluate using Groq
        groq_result = evaluate_groq(
            candidate_answer=candidate_answer,
            expected_answer=expected_answer,
            expected_concepts=expected_concepts,
            max_marks=10
        )

        final_marks = groq_result["marks"]

        answer = Answer(
            question_id=question.id,
            user_id=user.id,
            answer_text=candidate_answer,
            marks=final_marks
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        return {
            "message": "Answer saved and evaluated successfully",
            "answer": {
                "id": answer.id,
                "question_id": answer.question_id,
                "user_id": answer.user_id,
                "answer_text": answer.answer_text
            },
            "evaluation": {
                "groq": groq_result,
                "final_marks": answer.marks
            }
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("Answer evaluation error:", repr(e))

        raise HTTPException(
            status_code=500,
            detail="Failed to save and evaluate answer"
        )
