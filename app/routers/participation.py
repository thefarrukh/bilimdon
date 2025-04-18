from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import db_dep, current_user_dep, admin_user_dep
from app.schemas import ParticipationResponse, ParticipationCreate, ParticipationUpdate
from app.models import Participation

router = APIRouter(prefix="/participations", tags=["participation"])


@router.get("/", response_model=list[ParticipationResponse])
async def list_participations(db: db_dep):
    return db.query(Participation).all()


@router.get("/{id}/", response_model=ParticipationResponse)
async def get_participation(
        db: db_dep,
        id: int
):
    return db.query(Participation).filter(Participation.id == id).first()


@router.post("/create/", response_model=ParticipationResponse)
async def create_participation(
        db: db_dep,
        current_user: current_user_dep,
        participation: ParticipationCreate
):
    db_participation = Participation(
        **participation.model_dump(exclude_unset=True),
        user_id=current_user.id
    )

    db.add(db_participation)
    db.commit()
    db.refresh(db_participation)

    return db_participation


# Update
@router.patch("/{id}/update/", response_model=ParticipationResponse)
async def update_participation(
        db: db_dep,
        current_user: current_user_dep,
        participation: ParticipationUpdate
):
    participation_obj = db.query(Participation).filter(
        Participation.id == participation.id
    ).first()

    if not participation_obj:
        raise HTTPException(
            status_code=404,
            detail={
                "Participation with this id is not found."
            }
        )

    participation_obj.start_time = participation.start_time if participation.start_time else participation_obj.start_time
    participation_obj.end_time = participation.end_time if participation.end_time else participation_obj.end_time
    participation_obj.gained_score = participation.gained_score if participation.gained_score else participation_obj.gained_score

    db.commit()
    db.refresh(participation_obj)

    return participation_obj


@router.get("/{id}/submissions/")
async def participation_submissions(
        db: db_dep,
        current_user: current_user_dep,
        id: int
):
    pass