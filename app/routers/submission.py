from typing import List

from fastapi import APIRouter, HTTPException
from app.dependencies import db_dep
from app.schemas.submissionschema import SubmissionResponse, SubmissionRequest
from app.models import Submission, Question, Option, User

router = APIRouter(tags=['Submission'])

@router.get('/get_submission', response_model=List[SubmissionResponse])
async def get_submission(db:db_dep):
    return db.query(Submission).all()


@router.get('/get_submission/{id}', response_model=SubmissionResponse)
async def get_submission(id:int, db:db_dep):
    submission = db.query(Submission).filter(Submission.id == id).first()
    if not submission:
        raise HTTPException(status_code=404, detail='Submission not found')
    return submission


@router.post('/create_submission', response_model=SubmissionResponse)
async def create_submission(db:db_dep, request:SubmissionRequest):
    if not db.query(Question).filter(Question.id == request.question_id).first():
        raise HTTPException(status_code=404, detail='Your question_id does not exist')

    if not db.query(User).filter(User.id == request.user_id).first():
        raise HTTPException(status_code=404, detail="Your user_id does not exist")

    if not db.query(Option).filter(Option.id == request.option_id).first():
        raise HTTPException(status_code=404, detail="Your option_id does not exist")

    submission_model = Submission(**request.model_dump())

    db.add(submission_model)
    db.commit()
    db.refresh(submission_model)

    return submission_model


@router.put('/update_submission', response_model=SubmissionResponse)
async def update_participation(id:int, db:db_dep, request:SubmissionRequest):
    submission_model = db.query(Submission).filter(Submission.id == id).first()

    if not submission_model:
        raise HTTPException(status_code=404, detail='Submission not found')

    if not db.query(Question).filter(Question.id != request.question_id).first():
        raise HTTPException(status_code=404, detail='Your question_id is not exist')

    if not db.query(User).filter(User.id != request.user_id).first():
        raise HTTPException(status_code=404, detail="Your user_id not exist")

    if not db.query(Option).filter(Option.id == request.option_id).first():
        raise HTTPException(status_code=404, detail="Your option_id does not exist")


    submission_model.user_id = request.user_id
    submission_model.question_id = request.question_id
    submission_model.option_id = request.option_id
    submission_model.created_at = request.created_at
    submission_model.is_correct = request.is_correct

    db.add(submission_model)
    db.commit()
    db.refresh(submission_model)

    return submission_model

@router.delete('/delete_submission')
async def delete_participation(id:int, db: db_dep):
    submission_model = db.query(Submission).filter(Submission.id == id).first()

    if not submission_model:
        raise HTTPException(status_code=404, detail='Submission not found')

    db.delete(submission_model)
    db.commit()
    return {submission_model}
