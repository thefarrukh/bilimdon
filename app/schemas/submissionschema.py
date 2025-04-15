from datetime import datetime

from pydantic import BaseModel

class SubmissionRequest(BaseModel):
    user_id: int
    question_id: int
    option_id: int
    created_at: datetime
    is_correct: bool

class SubmissionResponse(BaseModel):
    id:int
    user_id: int
    question_id: int
    option_id: int
    created_at: datetime
    is_correct: bool
