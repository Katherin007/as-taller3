from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from api.database import Base

class Cart(Base):
    __tablename__ = "carts"
    
    # TODO: Definir los campos del modelo Cart
    # id = Column(...)
    # user_id = Column(..., ForeignKey(...))
    # created_at = Column(...)
    # updated_at = Column(...)
    
    # TODO: Definir relaciones
    # user = relationship(...)
    # items = relationship(...)

class CartItem(Base):
    __tablename__ = "cart_items"
    
    # TODO: Definir los campos del modelo CartItem
    # id = Column(...)
    # cart_id = Column(..., ForeignKey(...))
    # product_id = Column(..., ForeignKey(...))
    # quantity = Column(...)
    # added_at = Column(...)
    
    # TODO: Definir relaciones
    # cart = relationship(...)
    # product = relationship(...)