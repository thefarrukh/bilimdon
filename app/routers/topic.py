from fastapi import APIRouter, HTTPException

from app.dependencies import db_dep, current_user_dep, admin_user_dep, staff_user_dep
from app.models import Topic
from app.schemas import TopicCreate, TopicResponse


router = APIRouter(prefix="/topics", tags=["topics"])



@router.get("/", response_model=list[TopicResponse])
async def get_topics(db: db_dep):
    return db.query(Topic).all()


@router.post("/create/", response_model=TopicResponse)
async def create_topic(
    topic: TopicCreate,
    db: db_dep,
    admin_user: admin_user_dep
):
    if db.query(Topic).filter(Topic.name == topic.name).first():
        raise HTTPException(
            status_code=400,
            detail="Topic with this name already exists."
        )
    db_topic = Topic(
        name=topic.name
    )

    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)

    return db_topic


@router.delete("/delete/{id}")
async def delete_topic(id: int, db: db_dep, admin_user: admin_user_dep):
    db_topic = db.query(Topic).filter(Topic.id == id).first()

    if not db_topic:
        raise HTTPException(
            status_code=404,
            detail="Topic not found."
        )

    db.delete(db_topic)
    db.commit()

    return {
        "topic_id": id,
        "message": "Topic deleted."
    }