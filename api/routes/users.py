from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.database import get_db
from api.models.user import User

router = APIRouter()

@router.post("/register")
async def register_user(db: Session = Depends(get_db)):
    # TODO: Implementar registro de usuario
    pass

@router.post("/login")  
async def login_user(db: Session = Depends(get_db)):
    # TODO: Implementar login de usuario
    pass

@router.get("/profile")
async def get_user_profile(db: Session = Depends(get_db)):
    # TODO: Implementar obtener perfil de usuario
    pass

@router.put("/profile")
async def update_user_profile(db: Session = Depends(get_db)):
    # TODO: Implementar actualizar perfil de usuario
    pass