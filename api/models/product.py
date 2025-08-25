from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from api.database import Base
import uuid

class Product(Base):
    __tablename__ = "products"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        return f"<Product(id='{self.id}', name='{self.name}', price='{self.price}')>"