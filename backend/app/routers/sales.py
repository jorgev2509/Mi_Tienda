from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import case, func, select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import InventoryMovement, MovementType, Product, Sale, SaleLine, User
from app.schemas import SaleCreate, SaleOut
from app.security import require_permission

router = APIRouter(prefix="/sales", tags=["ventas POS"])
money = lambda value: value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
def stock_for(db, product_id):
    return db.scalar(select(func.coalesce(func.sum(case((InventoryMovement.movement_type.in_([MovementType.SALE, MovementType.ADJUSTMENT_OUT]), -InventoryMovement.quantity), else_=InventoryMovement.quantity)), 0)).where(InventoryMovement.product_id == product_id))
@router.get("", response_model=list[SaleOut])
def list_sales(db: Session = Depends(get_db), _=Depends(require_permission("sales.view"))): return db.scalars(select(Sale).order_by(Sale.id.desc()).limit(200)).all()
@router.post("", response_model=SaleOut, status_code=201)
def create_sale(data: SaleCreate, db: Session = Depends(get_db), user: User = Depends(require_permission("sales.create"))):
    ids = [line.product_id for line in data.lines]
    if len(ids) != len(set(ids)): raise HTTPException(400, "No repita productos en una venta")
    products = {p.id: p for p in db.scalars(select(Product).where(Product.id.in_(ids)).with_for_update())}
    if len(products) != len(ids): raise HTTPException(404, "Uno o más productos no existen")
    for line in data.lines:
        if stock_for(db, line.product_id) < line.quantity: raise HTTPException(409, f"Inventario insuficiente para {products[line.product_id].name}")
    number = f"V-{datetime.now():%Y%m%d}-{(db.scalar(select(func.count(Sale.id))) or 0) + 1:06d}"
    sale = Sale(number=number, subtotal=0, tax=0, total=0, created_by_id=user.id); db.add(sale); db.flush()
    subtotal = tax = Decimal("0")
    for item in data.lines:
        product = products[item.product_id]; price = item.unit_price if item.unit_price is not None else product.sale_price
        base = money(price * item.quantity); line_tax = money(base * product.tax_rate / 100)
        sale.lines.append(SaleLine(product_id=product.id, quantity=item.quantity, unit_price=price, tax_rate=product.tax_rate, line_total=base + line_tax))
        db.add(InventoryMovement(product_id=product.id, movement_type=MovementType.SALE, quantity=item.quantity, reference=number, note="Venta POS", created_by_id=user.id))
        subtotal += base; tax += line_tax
    sale.subtotal=money(subtotal); sale.tax=money(tax); sale.total=sale.subtotal+sale.tax
    db.commit(); db.refresh(sale); return sale

