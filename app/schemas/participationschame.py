from pydantic import BaseModel
from datetime import datetime

class ParticipationRequest(BaseModel):
    user_id: int
    game_id: int
    start_time: datetime
    end_time: datetime
    gained_score: int
    registered_at: datetime


class ParticipationResponse(BaseModel):
    id: int
    user_id: int
    game_id: int
    start_time: datetime
    end_time: datetime
    gained_score: int
    registered_at: datetime
