from pydantic import BaseModel

class TopicRequest(BaseModel):
    name:str

class TopicResponse(BaseModel):
    id:int
    name:str

    class Config:
        orm_mode = True