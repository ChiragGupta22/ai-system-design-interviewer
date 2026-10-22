
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.User.settings import groq_client, GROQ_MODEL
from src.User.model import TaskModel
from src.interview.models import Interview
from src.question.models import Question, ExpectedConcept
from src.answer.model import Answer


def generate_question(
    interview_id: int,
    db: Session,
    user: TaskModel,
    total_questions: int = 10,
    show_expected_answer: bool = False
):
    try:
        # 1. Verify interview ownership
        interview = (
            db.query(Interview)
            .filter(
                Interview.id == interview_id,
                Interview.user_id == user.id
            )
            .first()
        )

        if not interview:
            raise HTTPException(
                status_code=404,
                detail="Interview not found"
            )

        # 2. Fetch previous questions
        previous_questions = (
            db.query(Question)
            .filter(
                Question.interview_id == interview.id
            )
            .order_by(Question.id)
            .all()
        )

        if len(previous_questions) >= total_questions:
            return {
                "completed": True,
                "message": "Interview completed",
                "total_questions": len(previous_questions)
            }

        # 3. Require an answer before generating next question
        if previous_questions:
            last_question = previous_questions[-1]

            existing_answer = (
                db.query(Answer)
                .filter(
                    Answer.question_id == last_question.id,
                    Answer.user_id == user.id
                )
                .first()
            )

            if not existing_answer:
                response_data = {
                    "completed": False,
                    "question_number": len(previous_questions),
                    "total_questions": total_questions,
                    "id": last_question.id,
                    "interview_id": last_question.interview_id,
                    "question_text": last_question.question_text,
                    "message": (
                        "Answer this question before requesting "
                        "the next one"
                    )
                }

                if show_expected_answer:
                    response_data["expected_answer"] = (
                        last_question.expected_answer
                    )

                    concepts = (
                        db.query(ExpectedConcept)
                        .filter(
                            ExpectedConcept.question_id
                            == last_question.id
                        )
                        .all()
                    )

                    response_data["expected_concepts"] = [
                        item.concept for item in concepts
                    ]

                return response_data

        # 4. Previous questions for context
        previous_texts = [
            question.question_text
            for question in previous_questions
        ]

        # 5. Generate question, expected answer and concepts
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an expert system design interviewer.

Generate exactly ONE system design interview question
for the specified project.

Return valid JSON:
{
  "question_text": "Interview question",
  "expected_answer": "Detailed technically correct reference answer",
  "expected_concepts": [
    "Concept 1",
    "Concept 2",
    "Concept 3",
    "Concept 4"
  ]
}

Rules:
- Explain architecture, key components and trade-offs.
- Generate 4 to 6 distinct expected concepts.
- Concepts must be technically relevant.
- Avoid repeating previous questions.
- Return valid JSON only.
"""
                },
                {
                    "role": "user",
                    "content": json.dumps({
                        "project_name": interview.project_name,
                        "previous_questions": previous_texts
                    })
                }
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Groq returned an empty response")

        result = json.loads(content)

        question_text = result.get("question_text")
        expected_answer = result.get("expected_answer")
        concepts = result.get("expected_concepts")

        if not isinstance(question_text, str) or not question_text.strip():
            raise ValueError("Invalid question text")

        if not isinstance(expected_answer, str) or not expected_answer.strip():
            raise ValueError("Invalid expected answer")

        if not isinstance(concepts, list):
            raise ValueError("Invalid expected concepts")

        concepts = list(dict.fromkeys(
            concept.strip()
            for concept in concepts
            if isinstance(concept, str) and concept.strip()
        ))

        if len(concepts) < 2:
            raise ValueError("Groq returned too few expected concepts")

        # 6. Save question and expected answer
        question = Question(
            interview_id=interview.id,
            question_text=question_text.strip(),
            expected_answer=expected_answer.strip()
        )

        db.add(question)
        db.flush()

        # 7. Save expected concepts
        for concept in concepts:
            db.add(
                ExpectedConcept(
                    question_id=question.id,
                    concept=concept
                )
            )

        db.commit()
        db.refresh(question)

        # 8. Default response: candidate sees only question
        response_data = {
            "completed": False,
            "question_number": len(previous_questions) + 1,
            "total_questions": total_questions,
            "id": question.id,
            "interview_id": question.interview_id,
            "question_text": question.question_text
        }

        # Include reference data only when explicitly requested
        if show_expected_answer:
            response_data["expected_answer"] = (
                question.expected_answer
            )
            response_data["expected_concepts"] = concepts

        return response_data

    except HTTPException:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Question generation or database save failed"
        )
