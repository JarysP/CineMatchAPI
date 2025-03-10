from fastapi import FastAPI
from routes.routes import router as movie_router
from authenticate.auth import router as auth_router
from config.db import engine
from models.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(movie_router)
app.include_router(auth_router)