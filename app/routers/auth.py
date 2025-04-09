from fastapi import APIRouter, HTTPException, status
from app.database import *
from app.schema import *
from app.models import User
from app.routers.utils import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post('/registration', response_model=AuthRegistrationResponse)
async def registration(db: db_dep, user: AuthRegistration):
    # Email tekshirish
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu email allaqachon ro'yxatdan o'tgan."
        )

    # Username tekshirish
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username allaqachon band."
        )

    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password),
        email=user.email,
        role='user'
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



@router.post('/login')
async def login(
        db: db_dep,
        user: AuthLogin
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    is_correct = verify_password(user.password, db_user.hashed_password)  # To'g'ri: hashed_password

    if not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid password or username."
        )

    access_token = create_access_token(user.model_dump())
    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
