from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InventoryMovement, MovementType, Product
from app.schemas import ProductCreate, ProductOut
from app.security import require_permission

router = APIRouter(prefix="/products", tags=["productos"])
stock_expr = func.coalesce(func.sum(case((InventoryMovement.movement_type.in_([MovementType.SALE, MovementType.ADJUSTMENT_OUT]), -InventoryMovement.quantity), else_=InventoryMovement.quantity)), 0)
@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db), _=Depends(require_permission("products.view"))):
    rows = db.execute(select(Product, stock_expr.label("stock")).outerjoin(InventoryMovement).group_by(Product.id).order_by(Product.name)).all()
    return [ProductOut.model_validate(p).model_copy(update={"stock": stock}) for p, stock in rows]
@router.post("", response_model=ProductOut, status_code=201)
def create_product(data: ProductCreate, db: Session = Depends(get_db), _=Depends(require_permission("products.manage"))):
    if db.scalar(select(Product).where(Product.sku == data.sku)): raise HTTPException(409, "El SKU ya existe")
    product = Product(**data.model_dump()); db.add(product); db.commit(); db.refresh(product)
    return ProductOut.model_validate(product)

