from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import uuid
from models import MarcaVehiculo
from schemas import MarcaVehiculoCreate

def create_marca(db: Session, marca: MarcaVehiculoCreate):
    db_marca = MarcaVehiculo(
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
    return db.query(MarcaVehiculo).filter(MarcaVehiculo.uuidmarcavehiculo == marca_id).first()

def get_marcas(db: Session, skip: int = 0, limit: int = 10) -> List[MarcaVehiculo]:
    return db.query(MarcaVehiculo).offset(skip).limit(limit).all()

def delete_marca(db: Session, marca_id: uuid.UUID):  # Asegúrate de que marca_id sea de tipo UUID
    db_marca = db.query(MarcaVehiculo).filter(MarcaVehiculo.uuidmarcavehiculo == marca_id).first()
    if db_marca:
        db.delete(db_marca)
        db.commit()
        return {"message": "Marca deleted successfully"}
    return None