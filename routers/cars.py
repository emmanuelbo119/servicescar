from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models import models
from schemas import schemas
import database
import uuid
from controllers import cars



router = APIRouter(prefix="/Automoviles")




#CRUD

@router.post("/automoviles/", response_model=schemas.Vehiculo)
def create_car(car: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    return cars.create_car(car, db)

@router.get("/automoviles/", response_model=List[schemas.Vehiculo])
def read_cars(db: Session = Depends(database.get_db)):
    return cars.read_cars(db)


@router.delete("/automoviles/{automovil_id}",response_model=str)
def delete_car(automovil_id: uuid.UUID, db: Session = Depends(database.get_db)):
    return cars.delete_car(automovil_id, db)

@router.put("/automoviles/{automovil_id}", response_model=schemas.Vehiculo)
def update_car(automovil_id: uuid.UUID, updated_car: schemas.VehiculoCreate, db: Session = Depends(database.get_db)):
    return cars.update_car(automovil_id, updated_car, db)

##get by id 
@router.get("/automoviles/{automovil_id}", response_model=schemas.Vehiculo)
def get_car(automovil_id: uuid.UUID, db: Session = Depends(database.get_db)):
    return cars.get_car(automovil_id, db)