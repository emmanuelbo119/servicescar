from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import uuid
from models import models
from schemas import schemas

def create_marca(db: Session, marca: schemas.MarcaVehiculoCreate):
    db_marca = models.MarcaVehiculo(
        nombre=marca.nombre,
        descripcion=marca.descripcion,
        fechacreacion=marca.fechacreacion,
        fechamodificacion=marca.fechamodificacion
    )
    db.add(db_marca)
    db.commit()
    db.refresh(db_marca)
    return db_marca

def get_marca(db: Session, marca_id: uuid.UUID):  # Asegúrate de que marca_id sea de tipo UUID
    return db.query(models.MarcaVehiculo).filter(models.MarcaVehiculo.uuidmarcavehiculo == marca_id).first()

def get_marcas(db: Session, skip: int = 0, limit: int = 10) -> List[models.MarcaVehiculo]:
    return db.query(models.MarcaVehiculo).offset(skip).limit(limit).all()

def delete_marca(db: Session, marca_id: uuid.UUID):  # Asegúrate de que marca_id sea de tipo UUID
    db_marca = db.query(models.MarcaVehiculo).filter(models.MarcaVehiculo.uuidmarcavehiculo == marca_id).first()
    if db_marca:
        db.delete(db_marca)
        db.commit()
        return {"message": "Marca deleted successfully"}
    return None