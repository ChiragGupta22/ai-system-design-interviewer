
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.models import Question
from src.answer.model import Answer
from src.interview.models import Interview

from src.evaluation.bi_encoder import (
    evaluate_answer as evaluate_bi_encoder
)

from src.evaluation.cross_encoder import (
    evaluate_answer as evaluate_cross_encoder
)


def create_answer(body, db: Session, user):
    try:
        # 1. Check whether the question exists
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

        # 2. Verify interview ownership
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

        # 3. Prevent duplicate answers
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

        # 4. Get expected answer from the Question model
        expected_answer = question.expected_answer

        if not expected_answer or not expected_answer.strip():
            raise HTTPException(
                status_code=422,
                detail="Expected answer is not available for this question"
            )

        candidate_answer = body.answer_text.strip()

        # 5. Evaluate using both encoders
        bi_result = evaluate_bi_encoder(
            candidate_answer,
            expected_answer
        )

        cross_result = evaluate_cross_encoder(
            candidate_answer,
            expected_answer
        )

        # 6. Save the candidate's answer
        answer = Answer(
            question_id=question.id,
            user_id=user.id,
            answer_text=candidate_answer
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        # 7. Return answer and evaluation results
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
                "cross_encoder": cross_result
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
