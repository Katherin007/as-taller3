from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from api.database import Base

class User(Base):
    __tablename__ = "users"
    
    # TODO: Definir los campos del modelo User
    # id = Column(...)
    # username = Column(...)
    # email = Column(...)
    # password_hash = Column(...)
    # is_active = Column(...)
    # created_at = Column(...)
    
    def __repr__(self):
        # TODO: Implementar representación del objeto
        pass