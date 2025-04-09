from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

from app.database import db_dep
from app.models import User

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "void@pointer"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES = 30  # daqiqa

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === UTILS ===

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: int = None):
    expire = datetime.now(timezone.utc) + timedelta(minutes=expires_delta or ACCESS_TOKEN_EXPIRES)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(request: Request, db: Session = Depends(db_dep)):  # `db` uchun `Depends` ishlatiladi
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="You are not authenticated.")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token.")
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token.")

def require_superuser(user: User = Depends(get_current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Only superusers allowed.")
    return user

# === ROUTERS ===

@router.post("/register")
def register(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_dep)):  # `db` uchun `Depends` ishlatiladi
    existing = db.query(User).filter(User.username == form.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists.")

    new_user = User(
        username=form.username,
        email=form.username + "@mail.com",  # may be changed
        hashed_password=hash_password(form.password),
        first_name="",
        last_name="",
        is_active=True,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_dep)):  # `db` uchun `Depends` ishlatiladi
    user = db.query(User).filter(User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me")
def me(user: User = Depends(get_current_user)):  # `Depends` ishlatiladi
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_superuser": user.is_superuser,
        "joined_at": user.joined_at,
    }

@router.get("/super", dependencies=[Depends(require_superuser)])
def only_for_superusers():
    return {"message": "Welcome, Superuser!"}
