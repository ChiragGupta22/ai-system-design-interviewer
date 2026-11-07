
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.models import Question
from src.answer.model import Answer
from src.interview.models import Interview

from src.evaluation.bi_encoder import (
    evaluate_answer as evaluate_bi_encoder
)


def create_answer(body, db: Session, user):
    try:
        # Check whether the question exists
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

        # Verify interview ownership
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

        # Prevent duplicate answers
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

        # Get expected answer from the Question model
        expected_answer = question.expected_answer

        if not expected_answer or not expected_answer.strip():
            raise HTTPException(
                status_code=422,
                detail="Expected answer is not available for this question"
            )

        candidate_answer = body.answer_text.strip()

        # Evaluate using BiEncoder
        bi_result = evaluate_bi_encoder(
            candidate_answer,
            expected_answer
        )

        final_marks = bi_result["marks"]

        # Save the candidate's answer
        answer = Answer(
            question_id=question.id,
            user_id=user.id,
            answer_text=candidate_answer,
            marks=final_marks
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        # Return answer and evaluation results
        return {
            "message": "Answer saved and evaluated successfully",
            "answer": {
                "id": answer.id,
                "question_id": answer.question_id,
                "user_id": answer.user_id,
                "answer_text": answer.answer_text
            },
            "evaluation": {
                "bi_encoder": bi_result,
                "final_marks": answer.marks
            }
        }

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to save and evaluate answer"
        )
