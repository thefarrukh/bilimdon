from fastapi import APIRouter, HTTPException
from app.models import *
from app.database import db_dep
from app.schemas.gamequestion import GameQuestionRequest, GameQuestionResponse, GameQuestionUpdate

router = APIRouter(
    tags=['GameQuestion']
)

@router.get('/get_game_question', response_model=List[GameQuestionResponse])
async def get_game_question(db: db_dep):
    game_questions = db.query(GameQuestion).all()
    return game_questions


@router.get('/get_game_question/{id}', response_model=GameQuestionResponse)
async def get_game_question_by_id(id: int, db: db_dep):
    game_question = db.query(GameQuestion).filter(GameQuestion.id == id).first()

    if not game_question:
        raise HTTPException(status_code=404, detail="GameQuestion not found")

    return game_question



@router.post('/create_game_question', response_model=GameQuestionResponse)
async def create_game_question(db: db_dep, request: GameQuestionRequest):
    game_question = db.query(GameQuestion).filter(
        GameQuestion.game_id == request.game_id,
        GameQuestion.question_id == request.question_id
    ).first()

    if game_question:
        raise HTTPException(status_code=400, detail='Game already exist')

    new_game_question = GameQuestion(**request.dict())

    db.add(new_game_question)
    db.commit()
    db.refresh(new_game_question)

    return new_game_question


@router.put('/update_game_question/{id}', response_model=GameQuestionResponse)
async def update_game_question_by_id(id:int, db:db_dep, request:GameQuestionUpdate):

    game_question = db.query(GameQuestion).filter(GameQuestion.id==id).first()
    if not game_question:
        raise HTTPException(status_code=404, detail="GameQuestion not found")

    game_question.score = request.score

    db.add(game_question)
    db.commit()
    db.refresh(game_question)

    return game_question


@router.delete('/delete_game_question/{id}', response_model=GameQuestionResponse)
async def delete_options(db : db_dep, id: int):
    game_question = db.query(GameQuestion).filter(id == GameQuestion.id).first()
    if game_question is None:
        raise HTTPException(status_code=404, detail='GameQuestion not found')
    db.query(GameQuestion).filter(id == GameQuestion.id).delete()

    db.commit()

    return game_question