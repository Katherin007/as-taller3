from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from routes import users, products, carts

# TODO: Crear la instancia de FastAPI
app = FastAPI(
    title="Tienda Virtual API", 
    version="1.0.0",
    description="API para la gestión de una tienda virtual")


# TODO: Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar según las necesidades de seguridad
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Incluir los routers
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(carts.router, prefix="/api/v1/carts", tags=["carts"])

@app.get("/")
async def root():
    # TODO: Endpoint de prueba
    return {"message": "Tienda Virtual API"}

@app.get("/health")
async def health_check():
    # TODO: Endpoint de verificación de salud
    return {"status": "ok"}
