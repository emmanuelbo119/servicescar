from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from app.models import models
from app.schemas import schemas
from app import database
from app.controllers import usuarios as user_controller

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
    
)

# Dependencia para obtener la sesión de la base de datos

@router.post("/", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    return user_controller.create_user(user, db)

@router.get("/{user_id}", response_model=schemas.Usuario)
async def read_user(user_id: uuid.UUID, db: Session = Depends(database.get_db)):
    return user_controller.get_user(user_id, db)

@router.get("/", response_model=List[schemas.Usuario])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return user_controller.get_users(skip, limit, db)

@router.delete("/{user_id}", response_model=schemas.Usuario)
def delete_user(user_id: uuid.UUID, db: Session = Depends(database.get_db)):
    return user_controller.delete_user(user_id, db)

@router.put("/{user_id}", response_model=schemas.Usuario)
def update_user(user_id: uuid.UUID, updated_user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    return user_controller.update_user(user_id, updated_user, db)


@router.post("/reset-password")
def reset_password(request: schemas.ResetPasswordRequest, db: Session = Depends(database.get_db)):
    return user_controller.reset_password(request.email, request.new_password, db)