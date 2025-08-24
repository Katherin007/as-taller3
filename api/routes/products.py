from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.product import Product

router = APIRouter()

@router.get("/")
async def get_products(db: Session = Depends(get_db)):
    # TODO: Implementar obtener lista de productos
    pass

@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar obtener producto por ID
    pass

@router.post("/")
async def create_product(db: Session = Depends(get_db)):
    # TODO: Implementar crear producto (admin)
    pass

@router.put("/{product_id}")
async def update_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar producto
    pass

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar eliminar producto
    pass