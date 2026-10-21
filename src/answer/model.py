
from pydantic import BaseModel, Field, ConfigDict


class AnswerCreate(BaseModel):
    question_id: int
    answer_text: str = Field(min_length=1)


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    user_id: int
    answer_text: str

    model_config = ConfigDict(from_attributes=True)
