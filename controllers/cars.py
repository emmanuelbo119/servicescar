from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
import uuid
from models import models
from schemas import schemas



def create_car(car: schemas.VehiculoCreate, db: Session):
    db_car = models.Vehiculo(
        marca=car.marca,
        modelo=car.modelo,
        anio=car.anio,
        color=car.color,
        precio=car.precio,
        descripcion=car.descripcion
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def read_cars(db: Session) -> List[models.Vehiculo]:
    return db.query(models.Vehiculo).all()

def delete_car(automovil_id: uuid.UUID, db: Session):   

    db_car = db.query(models.Vehiculo).filter(models.Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return db_car

def get_car(db:Session, automovil_id:uuid.UUID):
    db_car = db.query(models.Vehiculo).filter(models.Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car