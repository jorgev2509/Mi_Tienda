from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import Token, UserOut
from app.security import create_token, current_user, verify_password

router = APIRouter(prefix="/auth", tags=["autenticación"])
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == form.username.lower()))
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")
    return Token(access_token=create_token(user.id), user=user)
@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)): return user

