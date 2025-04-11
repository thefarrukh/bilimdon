from pydantic import BaseModel

class QuestionRequest(BaseModel):
    title: str
    description: str
    topic_id: int
    owner_id: int


class QuestionResponse(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    topic_id: int