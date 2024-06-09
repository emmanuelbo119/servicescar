from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
from database import get_db
from uuid import UUID
from controllers import vehiculos



router = APIRouter(
    prefix="/vehiculos",
    tags=["Vehiculos"],
    responses={404: {"description": "Not found"}},)


#CRUD

@router.post("/", response_model=schemas.VehiculoCreate)
def create_car(car: schemas.VehiculoBase, db: Session = Depends(get_db)):
    return vehiculos.crearVehiculo(car, db)

@router.get("/", response_model=List[schemas.Vehiculo])
def read_cars(db: Session = Depends(get_db)):
    return vehiculos.getVehiculos(db)


@router.delete("/{automovil_id}",response_model=str)
def delete_car(automovil_id: UUID, db: Session = Depends(get_db)):
    return vehiculos.borrarVehiculo(automovil_id, db)

@router.put("/{automovil_id}", response_model=schemas.Vehiculo)
def update_car(automovil_id: UUID, updated_car: schemas.VehiculoCreate, db: Session = Depends(get_db)):
    return vehiculos.actualizarVehiculo(automovil_id, updated_car, db)

##get by id 
@router.get("/{automovil_id}", response_model=schemas.Vehiculo)
def get_car(automovil_id: UUID, db: Session = Depends(get_db)):
    return vehiculos.getVehiculoById(automovil_id, db)




@router.get("/{user_id}/vehiculos", response_model=List[schemas.Vehiculo])
def get_vehiculos(user_id: UUID, db: Session = Depends(get_db)):
    return vehiculos.get_vehiculos_by_user(user_id, db) 