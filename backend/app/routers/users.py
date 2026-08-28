from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Permission, Role, User
from app.schemas import PermissionOut, RoleCreate, RoleOut, UserCreate, UserOut
from app.security import hash_password, require_permission

router = APIRouter(tags=["usuarios y permisos"])
@router.get("/permissions", response_model=list[PermissionOut])
def permissions(db: Session = Depends(get_db), _=Depends(require_permission("users.manage"))): return db.scalars(select(Permission).order_by(Permission.code)).all()
@router.get("/roles", response_model=list[RoleOut])
def roles(db: Session = Depends(get_db), _=Depends(require_permission("users.manage"))): return db.scalars(select(Role).order_by(Role.name)).all()
@router.post("/roles", response_model=RoleOut, status_code=201)
def create_role(data: RoleCreate, db: Session = Depends(get_db), _=Depends(require_permission("users.manage"))):
    if db.scalar(select(Role).where(Role.name == data.name)): raise HTTPException(409, "El rol ya existe")
    role = Role(name=data.name, permissions=list(db.scalars(select(Permission).where(Permission.id.in_(data.permission_ids)))))
    db.add(role); db.commit(); db.refresh(role); return role
@router.get("/users", response_model=list[UserOut])
def users(db: Session = Depends(get_db), _=Depends(require_permission("users.manage"))): return db.scalars(select(User).order_by(User.full_name)).all()
@router.post("/users", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db), _=Depends(require_permission("users.manage"))):
    if db.scalar(select(User).where(User.email == data.email.lower())): raise HTTPException(409, "El usuario ya existe")
    user = User(email=data.email.lower(), full_name=data.full_name, hashed_password=hash_password(data.password), roles=list(db.scalars(select(Role).where(Role.id.in_(data.role_ids)))))
    db.add(user); db.commit(); db.refresh(user); return user

