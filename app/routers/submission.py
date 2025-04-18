from fastapi import APIRouter, HTTPException, Depends

from datetime import datetime

from app.models import Submission
from app.schemas import SubmissionCreate, SubmissionResponse
from app.dependencies import db_dep, current_user_dep, admin_user_dep

router = APIRouter(prefix="/submissions", tags=["submissions"])


@router.get("/", response_model=list[SubmissionResponse])
async def get_all_submissions(
        db: db_dep,
        current_user: current_user_dep
):
    return db.query(Submission).all()


@router.get("/{id}/", response_model=SubmissionResponse)
async def get_submission(
        db: db_dep,
        current_user: current_user_dep,
        id: int
):
    db_submission = db.query(Submission).filter(Submission.id == id).first()

    if not db_submission:
        raise HTTPException(
            status_code=404,
            detail={"Submission not found."}
        )

    return db_submission


@router.post("/create", response_model=SubmissionResponse)
async def create_submission(
        db: db_dep,
        current_user: current_user_dep,
        submission: SubmissionCreate
):
    db_submission = Submission(
        **submission.model_dump(exclude_unset=True),
        user_id=current_user.id
    )

    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)

    return db_submission