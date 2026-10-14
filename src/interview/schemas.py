from pydantic import BaseModel,Field
from typing import Literal

class InterviewSchema(BaseModel):
    project_name: Literal["WhatsApp", "Netflix", "Tinder"]
    duration: int = Field(default=0, gt=45)
    status: str = "in_progress"