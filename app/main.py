from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.questions import router as question_router
from app.routers.topic import router as topic_router
from app.routers.options import router as options_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(question_router)
app.include_router(options_router)
app.include_router(topic_router)
