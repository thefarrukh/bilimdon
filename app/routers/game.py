from typing import List

from fastapi import APIRouter, HTTPException
from app.schemas.gameschema import *
from app.models import Game, User, Topic
from app.dependencies import db_dep

router = APIRouter(
    tags=['Game']
)

@router.get('/get_games', response_model=List[GameResponse])
async def get_info(db: db_dep):
    return db.query(Game).all()


@router.post('/create_game', response_model=GameResponse)
async def create_game(db: db_dep, request: GameRequest):
    game_model = Game(**request.model_dump())

    if not db.query(User).filter(User.id == request.owner_id).first():
        raise HTTPException(status_code=404, detail="Owner not found")

    if not db.query(Topic).filter(Topic.id == request.topic_id).first():
        raise HTTPException(status_code=404, detail="Topic not found")

    db.add(game_model)
    db.commit()
    db.refresh(game_model)

    return game_model


@router.put('/update_game/{game_id}', response_model=GameResponse)
async def update_question(game_id: int, db: db_dep, request: GameUpdateRequest):

    game_model = db.query(Game).filter(game_id == Game.id).first()

    if game_model is None:
        raise HTTPException(status_code=404, detail='Game not found')

    game_model.title = request.title
    game_model.description = request.description
    # game_model.score = request.score
    # game_model.owner_id = game_model.owner_id
    # game_model.topic_id = game_model.topic_id
    game_model.start_time = request.start_time
    game_model.end_time = request.end_time

    db.add(game_model)
    db.commit()
    db.refresh(game_model)

    return game_model


@router.delete('/delete_game/{game_id}')
async def delete_question(db : db_dep, game_id: int):
    game_model = db.query(Game).filter(game_id == Game.id).first()
    if game_model is None:
        raise HTTPException(status_code=404, detail='Game not found')
    db.query(Game).filter(game_id == Game.id).delete()

    db.commit()

    return game_model
