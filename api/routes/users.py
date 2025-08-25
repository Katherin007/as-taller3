from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.user import User
from pydantic import BaseModel, Field
from passlib.context import CryptContext


def get_current_user_placeholder(db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == "juanperez").first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: str = Field(pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: str
    password: str

class UserUpdate(BaseModel):
    email: str | None = None
    is_active: bool | None = None
    
    
@router.post("/register", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario o el email ya están en uso"
        )
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
   

@router.post("/login", status_code=status.HTTP_200_OK) 
async def login_user(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # TODO: Implementar login de usuario
   user = db.query(User).filter(User.email == user_credentials.email).first()
   if not user or not pwd_context.verify(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )
   return {"message": "Login exitoso"}
    
    

@router.get("/profile", status_code=status.HTTP_200_OK)
async def get_user_profile(user: User = Depends(get_current_user_placeholder)):
    # TODO: Implementar obtener perfil de usuario
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }
    return user_data
    

@router.put("/profile", status_code=status.HTTP_200_OK)
async def update_user_profile(updated_data: UserUpdate, user: User = Depends(get_current_user_placeholder), db: Session = Depends(get_db)):
    # TODO: Implementar actualizar perfil de usuario
    if updated_data.email:
        user.email = updated_data.email
    if updated_data.is_active is not None:
        user.is_active = updated_data.is_active
        
    db.commit()
    db.refresh(user)
    
    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "created_at": user.created_at
    }
    return user_data