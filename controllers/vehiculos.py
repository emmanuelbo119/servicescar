from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from uuid import UUID
from models import models
from schemas import schemas
from datetime import datetime


def crearVehiculo(car: schemas.VehiculoCreate, db: Session):
    db_car = models.Vehiculo(
        marca_id=car.marca_id,
        modelo_id=car.modelo_id,
        anio=car.anio,
        color=car.color,
        patente=car.patente,
        automovilista_id=car.automovilista_id,
        fechaCreacion= datetime.now(),
        fechaModificacion= datetime.now()
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def getVehiculos(db: Session) -> List[models.Vehiculo]:
    return db.query(models.Vehiculo).all()

def borrarVehiculo(automovil_id: UUID, db: Session):   
    db_car = db.query(models.Vehiculo).filter(models.Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return db_car

def getVehiculoById(db:Session, automovil_id:UUID):
    db_car = db.query(models.Vehiculo).filter(models.Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


def get_mantenimientos(db: Session, automovil_id:UUID):
    db_car = db.query(models.Vehiculo).filter(models.Vehiculo.uuidautomovil == automovil_id).first()

def actualizarVehiculo(db: Session, automovil_id: UUID,automovil_updated: schemas.VehiculoCreate):
    db_car = db.query(models.Vehiculo).get(automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_car.update(automovil_updated=automovil_updated)

    db.commit()
    return db_car
