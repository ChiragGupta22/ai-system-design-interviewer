
from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.question.embending_models import ExpectedAnswerEmbedding
from src.question.models import Question
from src.answer.model import Answer
from src.interview.models import Interview


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

        # Get expected answer
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
                detail="Candidate answer cannot be empty"
            )

        # Generate candidate embedding
        from src.evaluation.hf_client import generate_embedding

        candidate_embedding = generate_embedding(candidate_answer)

        # Check expected embedding exists
        expected_embedding = (
            db.query(ExpectedAnswerEmbedding)
            .filter(
                ExpectedAnswerEmbedding.question_id == question.id
            )
            .first()
        )

        if not expected_embedding:
            raise HTTPException(
                status_code=404,
                detail="Expected answer embedding not found"
            )

        # Calculate cosine similarity using pgvector
        distance = (
            db.query(
                ExpectedAnswerEmbedding.embedding.cosine_distance(
                    candidate_embedding
                )
            )
            .filter(
                ExpectedAnswerEmbedding.question_id == question.id
            )
            .scalar()
        )

        if distance is None:
            raise HTTPException(
                status_code=404,
                detail="Expected answer embedding not found"
            )

        similarity = 1 - float(distance)
        similarity = max(0.0, min(1.0, similarity))

        # Bi-Encoder evaluation
        bi_result = {
            "similarity_score": round(similarity, 4),
            "marks": round(similarity * 10, 2),
            "max_marks": 10
        }

        # Selective Cross-Encoder evaluation
        if similarity >= 0.85:
            cross_result = None
            final_marks = bi_result["marks"]

        else:
            from src.evaluation.hf_client import evaluate_with_cross_encoder

            cross_result = evaluate_with_cross_encoder(
                candidate_answer,
                expected_answer
            )

            final_marks = round(
                (bi_result["marks"] + cross_result["marks"]) / 2,
                2
            )

        # Save candidate answer
        answer = Answer(
            question_id=question.id,
            user_id=user.id,
            answer_text=candidate_answer,
            marks=final_marks
        )

        db.add(answer)
        db.commit()
        db.refresh(answer)

        
        response = {
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

        if cross_result is not None:
            response["evaluation"]["cross_encoder"] = cross_result

        return response
        

    except HTTPException:
        db.rollback()
        raise

    except Exception as e:
        db.rollback()
        print("ANSWER ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
