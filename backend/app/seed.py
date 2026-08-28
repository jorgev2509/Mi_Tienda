from sqlalchemy import select
from app.config import settings
from app.database import SessionLocal
from app.models import Permission, Role, User
from app.security import hash_password

PERMISSIONS = {
    "users.manage": "Administrar usuarios, roles y permisos",
    "products.view": "Consultar productos",
    "products.manage": "Crear y modificar productos",
    "inventory.view": "Consultar inventario y movimientos",
    "inventory.manage": "Registrar entradas y ajustes",
    "sales.view": "Consultar ventas",
    "sales.create": "Crear ventas desde el POS",
}
def run():
    with SessionLocal() as db:
        permissions = []
        for code, description in PERMISSIONS.items():
            item = db.scalar(select(Permission).where(Permission.code == code)) or Permission(code=code, description=description)
            db.add(item); permissions.append(item)
        db.flush()
        admin_role = db.scalar(select(Role).where(Role.name == "Administrador"))
        if not admin_role: admin_role = Role(name="Administrador", permissions=permissions); db.add(admin_role)
        else: admin_role.permissions = permissions
        db.flush()
        admin = db.scalar(select(User).where(User.email == settings.first_admin_email.lower()))
        if not admin:
            db.add(User(email=settings.first_admin_email.lower(), full_name="Administrador", hashed_password=hash_password(settings.first_admin_password), roles=[admin_role]))
        db.commit()
if __name__ == "__main__": run()

