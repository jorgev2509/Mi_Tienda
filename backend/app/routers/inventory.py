from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InventoryMovement, MovementType, Product, User
from app.schemas import MovementCreate, MovementOut
from app.security import require_permission

router = APIRouter(prefix="/inventory", tags=["inventario"])
def stock_for(db, product_id):
    return db.scalar(select(func.coalesce(func.sum(case((InventoryMovement.movement_type.in_([MovementType.SALE, MovementType.ADJUSTMENT_OUT]), -InventoryMovement.quantity), else_=InventoryMovement.quantity)), 0)).where(InventoryMovement.product_id == product_id))
@router.get("/movements", response_model=list[MovementOut])
def movements(db: Session = Depends(get_db), _=Depends(require_permission("inventory.view"))): return db.scalars(select(InventoryMovement).order_by(InventoryMovement.id.desc()).limit(500)).all()
@router.post("/movements", response_model=MovementOut, status_code=201)
def create_movement(data: MovementCreate, db: Session = Depends(get_db), user: User = Depends(require_permission("inventory.manage"))):
    if data.movement_type == MovementType.SALE: raise HTTPException(400, "Las salidas por venta se crean desde el POS")
    if not db.get(Product, data.product_id): raise HTTPException(404, "Producto no encontrado")
    if data.movement_type == MovementType.ADJUSTMENT_OUT and stock_for(db, data.product_id) < data.quantity: raise HTTPException(409, "Inventario insuficiente")
    movement = InventoryMovement(**data.model_dump(), created_by_id=user.id); db.add(movement); db.commit(); db.refresh(movement); return movement

