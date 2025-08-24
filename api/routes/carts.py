from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.cart import Cart, CartItem

router = APIRouter()

@router.get("/")
async def get_user_cart(db: Session = Depends(get_db)):
    # TODO: Implementar obtener carrito del usuario
    pass

@router.post("/items")
async def add_item_to_cart(db: Session = Depends(get_db)):
    # TODO: Implementar agregar item al carrito
    pass

@router.put("/items/{item_id}")
async def update_cart_item(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar actualizar cantidad de item
    pass

@router.delete("/items/{item_id}")
async def remove_item_from_cart(item_id: int, db: Session = Depends(get_db)):
    # TODO: Implementar remover item del carrito
    pass

@router.delete("/")
async def clear_cart(db: Session = Depends(get_db)):
    # TODO: Implementar limpiar carrito
    pass