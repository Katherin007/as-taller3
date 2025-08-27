from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database import get_db
from models.product import Product
from pydantic import BaseModel, Field
from typing import List, Optional

router = APIRouter()
def get_current_user_is_admin(user_id: str | None = None):

    if user_id != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador."
        )
    return True


class ProductCreate(BaseModel):
    name: str = Field(min_length=3, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    image_url: str | None = None

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    image_url: Optional[str] = None

class ProductResponse(BaseModel):
    id: str # revisar
    name: str
    description: str | None
    price: float
    stock: int
    image_url: str | None
    created_at: str #revisar

    class Config:
        orm_mode = True

@router.get("/", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db)):
    # TODO: Implementar obtener lista de productos
    products = db.query(Product).all()
    return products
  

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    # TODO: Implementar obtener producto por ID}
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return product
    
   

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, db: Session = Depends(get_db), is_admin: bool = Depends(get_current_user_is_admin)):
    # TODO: Implementar crear producto (admin)
    new_product = Product(**product_data.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product
   

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product_data: ProductUpdate, db: Session = Depends(get_db), is_admin: bool = Depends(get_current_user_is_admin)):
    # TODO: Implementar actualizar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product
   

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, db: Session = Depends(get_db), is_admin: bool = Depends(get_current_user_is_admin)):
    # TODO: Implementar eliminar producto
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    db.delete(product)
    db.commit()
    return None
   