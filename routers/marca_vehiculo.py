from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas import schemas 
from controllers import marca_vehiculo
from typing import List
from database import SessionLocal, engine, get_db
from uuid import UUID


router = APIRouter(
    prefix="/marcas_vehiculos",
    tags=["marcas"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.MarcaVehiculo)
def create_marca(marca: schemas.MarcaVehiculoCreate, db: Session = Depends(get_db)):
    return marca_vehiculo.create_marca(db=db, marca=marca)

@router.get("/{marca_id}", response_model=schemas.MarcaVehiculo)
def read_marca(marca_id: UUID, db: Session = Depends(get_db)):  # Asegúrate de que marca_id sea de tipo UUID
    db_marca = marca_vehiculo.get_marca(db, marca_id=marca_id)
    if db_marca is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return db_marca

@router.get("/", response_model=List[schemas.MarcaVehiculo])
def read_marcas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    marcas = marca_vehiculo.get_marcas(db, skip=skip, limit=limit)
    return marcas

@router.delete("/{marca_id}")
def delete_marca(marca_id: UUID, db: Session = Depends(get_db)):  # Asegúrate de que marca_id sea de tipo UUID
    result = marca_vehiculo.delete_marca(db=db, marca_id=marca_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Marca not found")
    return {"message": "Marca deleted successfully"}