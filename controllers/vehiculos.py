from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from typing import List
from uuid import UUID
from models import Vehiculo
from schemas import schemas
from datetime import datetime


def crearVehiculo(car: schemas.VehiculoBase, db: Session):
    db_car = Vehiculo(
        marca_id=car.marca_id,
        modelo_id=car.modelo_id,
        anio=car.anio,
        color=car.color,
        patente=car.patente,
        usuario_id=car.usuario_id,
        fechaCreacion= datetime.now(),
        fechaModificacion= datetime.now()
    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car

def getVehiculos(db: Session) -> List[Vehiculo]:
    return db.query(Vehiculo).all()

def borrarVehiculo(automovil_id: UUID, db: Session):   
    db_car = db.query(Vehiculo).filter(Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
    return db_car

def getVehiculoById(db:Session, automovil_id:UUID):
    db_car = db.query(Vehiculo).filter(Vehiculo.uuidautomovil == automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    return db_car


def get_mantenimientos(db: Session, automovil_id:UUID):
    db_car = db.query(Vehiculo).filter(Vehiculo.uuidautomovil == automovil_id).first()

def actualizarVehiculo(db: Session, automovil_id: UUID,automovil_updated: schemas.VehiculoCreate):
    db_car = db.query(Vehiculo).get(automovil_id).first()
    if db_car is None:
        raise HTTPException(status_code=404, detail="Car not found")
    db_car.update(automovil_updated=automovil_updated)

    db.commit()
    return db_car



def get_vehiculos_by_user(user_id: UUID, db: Session) -> List[Vehiculo]:
    db_vehiculos = (
        db.query(Vehiculo)
        .filter(Vehiculo.usuario_id == user_id)
        .options(
            joinedload(Vehiculo.marca),
            joinedload(Vehiculo.modelo)
        )
        .all()
    )
    if not db_vehiculos:
        raise HTTPException(status_code=404, detail="User not found")
    
    return db_vehiculos