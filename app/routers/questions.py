from fastapi import APIRouter, HTTPException
from starlette import status
from app.database import *
from app.models import Question
from app.schemas.questionschema import *

router = APIRouter(tags=["Questions"])


@router.get('/get_questions', status_code=status.HTTP_200_OK)
async def get_questions(db: db_dep):
    return db.query(Question).all()


@router.post('/create_question', status_code=status.HTTP_201_CREATED, response_model=QuestionResponse)
async def create_question(db: db_dep, request:QuestionRequest):
    question_model = Question(**request.model_dump())

    db.add(question_model)
    db.commit()
    db.refresh(question_model)

    return question_model


@router.put('/update_question/{todo_id}', response_model=QuestionResponse)
async def update_question(todo_id: int, db: db_dep, request: QuestionRequest):

    question_model = db.query(Question).filter(todo_id == Question.id).first()

    if question_model is None:
        raise HTTPException(status_code=404, detail='Question not found')

    question_model.title = request.title
    question_model.description = request.description
    question_model.topic_id = request.topic_id
    question_model.owner_id = request.owner_id

    db.add(question_model)
    db.commit()
    db.refresh(question_model)

    return question_model


@router.delete('/delete_question/{todo_id}')
async def delete_question(db : db_dep, question_id: int):
    question_model = db.query(Question).filter(question_id == Question.id).first()
    if question_model is None:
        raise HTTPException(status_code=404, detail='Question not found')
    db.query(Question).filter(question_id == Question.id).delete()

    db.commit()

    return question_model