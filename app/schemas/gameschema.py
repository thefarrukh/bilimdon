from pydantic import BaseModel
from datetime import datetime

class GameRequest(BaseModel):
    title: str
    description: str
    score: int
    owner_id: int
    topic_id: int
    start_time: datetime
    end_time: datetime

class GameResponse(BaseModel):
    id: int
    title: str
    description: str
    score: int
    owner_id: int
    topic_id: int
    start_time: datetime
    end_time: datetime


class GameUpdateRequest(BaseModel):
    title: str
    description: str
    score: int
    start_time: datetime
    end_time: datetime