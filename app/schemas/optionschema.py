from pydantic import BaseModel

class OptionsRequest(BaseModel):
    question_id: int
    title: str
    is_correct: bool

class OptionsResponse(BaseModel):
    id: int
    question_id: int
    title: str
    is_correct: bool

    class Config:
        orm_mode = True
