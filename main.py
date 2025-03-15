from fastapi import FastAPI
from routes.routes import router as movie_router
from authenticate.auth import router as auth_router
from config.db import engine
from models.models import Base
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(movie_router)
app.include_router(auth_router)

# Redireccion a docs
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las conexiones (ajústalo en producción)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)