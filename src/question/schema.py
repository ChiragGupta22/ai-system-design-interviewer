from pydantic import BaseModel


class questionSchema(BaseModel):
    question_text: str
    expected_answer: str
    interview_id: int