from pydantic import BaseModel


class TopicResponse(BaseModel):
    id: int
    name: str


class TopicCreate(BaseModel):
    name: str