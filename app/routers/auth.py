from fastapi import APIRouter, HTTPException, Response

from app.database import *
from app.schemas.authschema import *
from app.models import User
from app.utils.auth import *
from app.dependencies import *

router = APIRouter(tags=["Auth"])


@router.post('/registration', response_model=AuthRegistrationResponse)
async def registration(
        db: db_dep,
        user: AuthRegistrationRequest
):
    is_first_user = db.query(User).count() == 0

    is_user_exists = db.query(User).filter(User.email == user.email).first()

    if is_user_exists:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists."
        )

    db_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        username=user.email.split("@")[0],
        is_active=True,
        is_staff=is_first_user,
        is_superuser=is_first_user
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
    db_user = db.query(User).filter(User.email == user.email).first()
    is_correct = verify_password(user.password, db_user.hashed_password) if db_user else False

    if not db_user or not is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid password or username."
        )

    token_data = {
        "username": db_user.username,
        "email": db_user.email,
        "role": "admin" if db_user.is_superuser else "user"
    }

    access_token = create_access_token(token_data)
    refresh_token = create_access_token(token_data, REFRESH_TOKEN_EXPIRE_MINUTES)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer"
    }