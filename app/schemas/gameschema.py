from pydantic import BaseModel

from datetime import datetime


class GameOwnerResponse(BaseModel):
    id: int
    username: str
    first_name: str | None = None
    last_name: str | None = None

class TopicResponse(BaseModel):
    id: int
    name: str


class GameResponse(BaseModel):
    id: int
    owner: GameOwnerResponse
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    topic: TopicResponse


class GameCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    end_time: datetime
    topic_id: int | None = None


class GameUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None
    topic_id: int | None = None


class GameSelectQuestion(BaseModel):
    question_id: int
    game_id: int