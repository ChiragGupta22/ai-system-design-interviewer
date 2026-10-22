
from pydantic import BaseModel, Field


class GenerateQuestionSchema(BaseModel):
    interview_id: int
    total_questions: int = Field(default=10, ge=1, le=50)
    show_expected_answer: bool = False


class QuestionCreateSchema(BaseModel):
    question_text: str
    expected_answer: str
    interview_id: int
