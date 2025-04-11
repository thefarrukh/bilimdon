from fastapi import APIRouter, HTTPException
from starlette import status
from app.database import *
from app.models import Option
from app.schemas.optionschema import *
from app.routers.questions import Question

router = APIRouter(tags=["Options"])


@router.get('/get_options', status_code=status.HTTP_200_OK)
async def get_options(db: db_dep):
    return db.query(Option).all()


@router.get('/get_options_by_id/{todo_id}', status_code=status.HTTP_200_OK)
async def get_options(id:int, db: db_dep):

    option_model = db.query(Option).filter(id == Option.question_id).all()

    if option_model is not None:
        return option_model
    raise HTTPException(status_code=404, detail='Todo not found')


@router.post('/create_options', status_code=status.HTTP_201_CREATED, response_model=OptionsResponse)
async def create_options(db: db_dep, request:OptionsRequest):

    options_model = db.query(Question).filter(Question.id == request.question_id).first()


    if options_model is None:
        raise HTTPException(status_code=404, detail='Question not found')

    new_model = Option(**request.model_dump())

    db.add(new_model)
    db.commit()
    db.refresh(new_model)

    return new_model


@router.put('/update_options/{option_id}', response_model=OptionsResponse)
async def update_options(option_id: int, db: db_dep, request: OptionsRequest):

    options_model = db.query(Option).filter(option_id == Option.id).first()

    if options_model is None:
        raise HTTPException(status_code=404, detail='Option not found')

    options_model.title = request.title
    options_model.is_correct = request.is_correct
    options_model.question_id = request.question_id

    db.add(options_model)
    db.commit()
    db.refresh(options_model)

    return options_model


@router.delete('/delete_options/{todo_id}')
async def delete_options(db : db_dep, question_id: int):
    options_model = db.query(Option).filter(question_id == Option.id).first()
    if options_model is None:
        raise HTTPException(status_code=404, detail='Option not found')
    db.query(Option).filter(question_id == Option.id).delete()

    db.commit()

    return options_model