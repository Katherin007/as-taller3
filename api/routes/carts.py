from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from api.database import get_db
from api.models.cart import Cart, CartItem
from api.models.product import Product
from api.models.user import User
from pydantic import BaseModel, Field
from typing import List

router = APIRouter()
def get_current_user_placeholder(db: Session = Depends(get_db)):
    """Simula la obtención del usuario actual a partir de un token."""
    user = db.query(User).filter(User.username == "juanperez").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
class CartItemAdd(BaseModel):
    product_id: str
    quantity: int = Field(ge=1)

class CartItemUpdate(BaseModel):
    quantity: int = Field(ge=1)

class CartItemResponse(BaseModel):
    id: str
    product_id: str
    quantity: int
    added_at: str

    class Config:
        orm_mode = True

class CartResponse(BaseModel):
    id: str
    user_id: str
    items: List[CartItemResponse]
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

@router.get("/", response_model=CartResponse)
async def get_user_cart(current_user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar obtener carrito del usuario
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    
    if not cart:
        # Crea un nuevo carrito si no existe
        new_cart = Cart(user_id=current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        cart = new_cart
    
    return cart
    pass

@router.post("/items", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_item_to_cart(item_data: CartItemAdd, current_user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar agregar item al carrito
    product = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    

    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        new_cart = Cart(user_id=current_user.id)
        db.add(new_cart)
        db.commit()
        db.refresh(new_cart)
        cart = new_cart
    
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item_data.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_data.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=item_data.product_id,
            quantity=item_data.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item
   

@router.put("/items/{item_id}", response_model=CartItemResponse)
async def update_cart_item(item_id: str, item_data: CartItemUpdate, current_user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar actualizar cantidad de item
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado en el carrito")
    
    cart_item.quantity = item_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_item_from_cart(item_id: str, current_user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar remover item del carrito
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

    cart_item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item no encontrado en el carrito")
    
    db.delete(cart_item)
    db.commit()
    return None
   

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(current_user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar limpiar carrito
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carrito no encontrado")

  
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return None
