from app.database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]