from pydantic import BaseModel

class GameQuestionRequest(BaseModel):
    game_id: int
    question_id: int
    score: int

class GameQuestionResponse(BaseModel):
    id: int
    game_id: int
    question_id: int
    score: int

    class Config:
        orm_mode = True

class GameQuestionUpdate(BaseModel):
    score: int