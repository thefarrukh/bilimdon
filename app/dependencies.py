from fastapi import Depends

from typing import Annotated

from sqlalchemy.orm import Session


def get_db():
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[Session, Depends(get_db)]