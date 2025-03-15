import jwt
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from models.models import User
from config.dependence import get_db

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

router = APIRouter()

@router.post("/auth/register")
def register(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = bcrypt.hash(password)
    user = User(username=username, email=email, password_hash=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "Usuario registrado"}

@router.post("/auth/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(email == User.email).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = jwt.encode({"user_id": user.id}, SECRET_KEY, algorithm="HS256")
    return {"token": token}

