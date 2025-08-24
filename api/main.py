from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from api.database import get_db
from api.routes import users, products, carts

# TODO: Crear la instancia de FastAPI
app = FastAPI(title="Tienda Virtual API", version="1.0.0")

# TODO: Configurar CORS
app.add_middleware(
    CORSMiddleware,
    # TODO: Configurar orígenes permitidos, métodos, etc.
)

# TODO: Incluir los routers
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
# app.include_router(carts.router, prefix="/api/v1/carts", tags=["carts"])

@app.get("/")
async def root():
    # TODO: Endpoint de prueba
    return {"message": "Tienda Virtual API"}

@app.get("/health")
async def health_check():
    # TODO: Endpoint de verificación de salud
    pass
