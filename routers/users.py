from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid
from models import models
from schemas import schemas
import database
from controllers import users as user_controller

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.Usuario)
def create_user(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return user_controller.create_user(user, db)

@router.get("/users/{user_id}", response_model=schemas.Usuario)
async def read_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return user_controller.get_user(user_id, db)

@router.get("/users/", response_model=List[schemas.Usuario])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_controller.get_users(skip, limit, db)

@router.delete("/users/{user_id}", response_model=schemas.Usuario)
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    return user_controller.delete_user(user_id, db)

@router.put("/users/{user_id}", response_model=schemas.Usuario)
def update_user(user_id: uuid.UUID, updated_user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return user_controller.update_user(user_id, updated_user, db)
