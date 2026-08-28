from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, inventory, products, sales, users

app = FastAPI(title="Mi Tienda ERP API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(products.router, prefix="/api/v1")
app.include_router(inventory.router, prefix="/api/v1")
app.include_router(sales.router, prefix="/api/v1")
@app.get("/health")
def health(): return {"status": "ok"}

