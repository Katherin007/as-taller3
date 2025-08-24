from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from api.database import Base

class Product(Base):
    __tablename__ = "products"
    
    # TODO: Definir los campos del modelo Product
    # id = Column(...)
    # name = Column(...)
    # description = Column(...)
    # price = Column(...)
    # stock = Column(...)
    # image_url = Column(...)
    # created_at = Column(...)
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        pass