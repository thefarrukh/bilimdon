
from typing import List

from fastapi import APIRouter, HTTPException
from app.models import Topic
from app.dependencies import db_dep
from app.schemas.topicsschema import *

router = APIRouter(tags=["Topic"])

@router.get('/get_topics', response_model=List[TopicResponse])
async def get_topics(db: db_dep):
    return db.query(Topic).all()

@router.post('/create_topic', response_model=TopicResponse)
async def create_question(db: db_dep, request:TopicRequest):
    topic_model = Topic(**request.model_dump())

    db.add(topic_model)
    db.commit()
    db.refresh(topic_model)

    return topic_model


@router.delete('/delete_topic/{todo_id}')
async def delete_topic(db : db_dep, topic_id: int):
    topic_model = db.query(Topic).filter(topic_id == Topic.id).first()
    if topic_model is None:
        raise HTTPException(status_code=404, detail='Topic not found')
    db.query(Topic).filter(topic_id == Topic.id).delete()

    db.commit()

    return topic_model