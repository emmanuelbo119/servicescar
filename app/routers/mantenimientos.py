from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List
import uuid
from app import models
from app import schemas
from app.database import get_db




router = APIRouter(
    prefix="/mantenimientos",
    tags=["mantenimientos"],
    responses={404: {"description": "Not found"}},
    
)



@router.post("/", response_model=schemas.Mantenimiento)
def create_mantenimiento(mantenimiento: schemas.MantenimientoCreate, db: Session = Depends(get_db)):
    db_mantenimiento = models.Mantenimiento(**mantenimiento.dict())
    db.add(db_mantenimiento)
    db.commit()
    db.refresh(db_mantenimiento)
    return db_mantenimiento

@router.put("/{mantenimiento_id}", response_model=schemas.Mantenimiento)
def update_mantenimiento(mantenimiento_id: uuid.UUID, updated_mantenimiento: schemas.MantenimientoUpdate, db: Session = Depends(get_db)):
    db_mantenimiento = db.query(models.Mantenimiento).filter(models.Mantenimiento.id == mantenimiento_id).first()
    if db_mantenimiento is None:
        raise HTTPException(status_code=404, detail="Mantenimiento not found")
    db_mantenimiento.descripcion = updated_mantenimiento.descripcion
    db_mantenimiento.fecha = updated_mantenimiento.fecha
    db.commit()
    db.refresh(db_mantenimiento)
    return db_mantenimiento
    