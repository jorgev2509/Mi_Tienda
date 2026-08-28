from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User

password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
def hash_password(password: str): return password_hash.hash(password)
def verify_password(password: str, hashed: str): return password_hash.verify(password, hashed)
def create_token(user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_minutes)
    return jwt.encode({"sub": str(user_id), "exp": expires}, settings.secret_key, algorithm="HS256")
def current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    try: user_id = int(jwt.decode(token, settings.secret_key, algorithms=["HS256"])["sub"])
    except (InvalidTokenError, KeyError, ValueError): raise error
    user = db.scalar(select(User).where(User.id == user_id))
    if not user or not user.is_active: raise error
    return user
def require_permission(code: str):
    def dependency(user: User = Depends(current_user)):
        if code not in {p.code for role in user.roles for p in role.permissions}:
            raise HTTPException(status_code=403, detail=f"Permiso requerido: {code}")
        return user
    return dependency

