from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List
import uuid
from app import models
from app import schemas
from app.database import get_db
from app.models.models import DetalleMantenimiento, Turno
from app.controllers import mantenimientos  as  mantenimientos_controller



router = APIRouter(
    prefix="/mantenimientos",
    tags=["mantenimientos"],
    responses={404: {"description": "Not found"}},
    
)

@router.post("/turnos/{turno_id}/detalles", response_model=schemas.DetalleMantenimiento)
async def agregar_detalle_mantenimiento(turno_id: uuid.UUID, detalle: schemas.DetalleMantenimientoCreate, db: Session = Depends(get_db)):
    detalle = mantenimientos_controller.agregar_detalle_mantenimiento(turno_id, detalle, Session)
    return detalle


@router.delete("/turnos/{turno_id}/detalles/{detalle_id}", response_model=schemas.DetalleMantenimiento)
async def eliminar_detalle_mantenimiento(turno_id: uuid.UUID, detalle_id: uuid.UUID, db: Session = Depends(get_db)):
    detalle = mantenimientos_controller.eliminar_detalle_mantenimiento(turno_id, detalle_id, db)
    return detalle


@router.put("/turnos/{turno_id}/finalizar-presupuesto", response_model=schemas.Turno)
async def finalizar_presupuesto(turno_id: uuid.UUID, db: Session = Depends(get_db)):
    turno = mantenimientos_controller.finalizar_presupuesto(turno_id, db)
    return turno