from pydantic import BaseModel
from typing import Literal

class InterviewSchema(BaseModel):
    project_name: Literal["WhatsApp", "Netflix", "Tinder"]
    
    status: str = "in_progress"