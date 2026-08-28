from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models import MovementType, SaleStatus

class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
class PermissionOut(ORMModel):
    id: int; code: str; description: str
class RoleOut(ORMModel):
    id: int; name: str; permissions: list[PermissionOut] = []
class RoleCreate(BaseModel):
    name: str; permission_ids: list[int] = []
class UserOut(ORMModel):
    id: int; email: EmailStr; full_name: str; is_active: bool; roles: list[RoleOut] = []
class UserCreate(BaseModel):
    email: EmailStr; full_name: str; password: str = Field(min_length=8); role_ids: list[int] = []
class Token(BaseModel):
    access_token: str; token_type: str = "bearer"; user: UserOut
class ProductCreate(BaseModel):
    sku: str; name: str; sale_price: Decimal = Field(ge=0); cost: Decimal = Field(default=0, ge=0); tax_rate: Decimal = Field(default=0, ge=0, le=100)
class ProductOut(ProductCreate, ORMModel):
    id: int; is_active: bool; stock: Decimal = 0
class MovementCreate(BaseModel):
    product_id: int; movement_type: MovementType; quantity: Decimal = Field(gt=0); note: str | None = None; reference: str | None = None
class MovementOut(MovementCreate, ORMModel):
    id: int; created_by_id: int; created_at: datetime
class SaleLineCreate(BaseModel):
    product_id: int; quantity: Decimal = Field(gt=0); unit_price: Decimal | None = Field(default=None, ge=0)
class SaleCreate(BaseModel):
    lines: list[SaleLineCreate] = Field(min_length=1)
class SaleLineOut(ORMModel):
    product_id: int; quantity: Decimal; unit_price: Decimal; tax_rate: Decimal; line_total: Decimal
class SaleOut(ORMModel):
    id: int; number: str; status: SaleStatus; subtotal: Decimal; tax: Decimal; total: Decimal; created_at: datetime; lines: list[SaleLineOut]

