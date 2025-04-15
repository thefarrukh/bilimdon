from typing import List

from fastapi import APIRouter, HTTPException
from app.database import db_dep
from app.schemas.participationschame import ParticipationRequest, ParticipationResponse
from app.models import Participation, Game, User

router = APIRouter(tags=['Participation'])

@router.get('/get_participation', response_model=List[ParticipationResponse])
async def get_participation(db:db_dep):
    return db.query(Participation).all()


@router.get('/get_participation/{id}', response_model=ParticipationResponse)
async def get_participation(id:int, db:db_dep):
    participation = db.query(Participation).filter(Participation.id == id).first()
    if not participation:
        raise HTTPException(status_code=404, detail='Participation not found')
    return participation


@router.post('/create_participation', response_model=ParticipationResponse)
async def create_participation(db:db_dep, request:ParticipationRequest):
    if not db.query(Game).filter(Game.id == request.game_id).first():
        raise HTTPException(status_code=404, detail='Your game_id does not exist')

    if not db.query(User).filter(User.id == request.user_id).first():
        raise HTTPException(status_code=404, detail="Your user_id does not exist")

    participation_model = Participation(**request.model_dump())

    db.add(participation_model)
    db.commit()
    db.refresh(participation_model)

    return participation_model


@router.put('/update_participation', response_model=ParticipationResponse)
async def update_participation(id:int, db:db_dep, request:ParticipationRequest):
    participation_model = db.query(Participation).filter(Participation.id == id).first()

    if not participation_model:
        raise HTTPException(status_code=404, detail='Participation not found')

    if not db.query(Game).filter(Game.id != request.game_id).first():
        raise HTTPException(status_code=404, detail='Your game_id is not exist')

    if not db.query(User).filter(User.id != request.user_id).first():
        raise HTTPException(status_code=404, detail="Your user_id not exist")


    participation_model.user_id = request.user_id
    participation_model.game_id = request.game_id
    participation_model.start_time = request.start_time
    participation_model.end_time = request.end_time
    participation_model.gained_score = request.gained_score
    participation_model.registered_at = request.registered_at

    db.add(participation_model)
    db.commit()
    db.refresh(participation_model)

    return participation_model

@router.delete('/delete_participation')
async def delete_participation(id:int, db: db_dep):
    participation_model = db.query(Participation).filter(Participation.id == id).first()

    if not participation_model:
        raise HTTPException(status_code=404, detail='Participation not found')

    db.delete(participation_model)
    db.commit()
    return {participation_model}
