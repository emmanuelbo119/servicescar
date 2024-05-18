from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import uuid
from models import models
from schemas import schemas

def create_user(user: schemas.UsuarioCreate, db: Session):
    db_user = db.query(models.Usuario).filter(models.Usuario.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    fake_hashed_password = user.contraseña + "notreallyhashed"
    db_user = models.Usuario(
        nombre=user.nombre,
        apellido=user.apellido,
        dni=user.dni,
        email=user.email,
        contraseña=fake_hashed_password,
        edad=user.edad,
        telefono=user.telefono
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: uuid.UUID, db: Session):
    db_user = db.query(models.Usuario).filter(models.Usuario.uuidusuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

def get_users(skip: int, limit: int, db: Session) -> List[models.Usuario]:
    return db.query(models.Usuario).offset(skip).limit(limit).all()

def delete_user(user_id: uuid.UUID, db: Session):
    db_user = db.query(models.Usuario).filter(models.Usuario.uuidusuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

def update_user(user_id: uuid.UUID, updated_user: schemas.UsuarioCreate, db: Session):
    db_user = db.query(models.Usuario).filter(models.Usuario.uuidusuario == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.nombre = updated_user.nombre
    db_user.apellido = updated_user.apellido
    db_user.dni = updated_user.dni
    db_user.email = updated_user.email
    db_user.contraseña = updated_user.contraseña + "notreallyhashed"
    db_user.edad = updated_user.edad
    db_user.telefono = updated_user.telefono

    db.commit()
    db.refresh(db_user)
    return db_user
