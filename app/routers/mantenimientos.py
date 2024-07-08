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
from app.schemas.schemas import DetalleMantenimientoCreate



router = APIRouter(
    prefix="/mantenimientos",
    tags=["mantenimientos"],
    responses={404: {"description": "Not found"}},
    
)


@router.delete("/turnos/{turno_id}/detalles/{detalle_id}", response_model=schemas.DetalleMantenimiento)
async def eliminar_detalle_mantenimiento(turno_id: uuid.UUID, detalle_id: uuid.UUID, db: Session = Depends(get_db)):
    detalle = mantenimientos_controller.eliminar_detalle_mantenimiento(turno_id, detalle_id, db)
    return detalle


@router.put("/turnos/{turno_id}/cambiar-estado-presupuesto", response_model=schemas.Turno)
async def finalizar_presupuesto(turno_id: uuid.UUID,estado:str, db: Session = Depends(get_db)):
    turno = mantenimientos_controller.finalizar_presupuesto(turno_id,estado, db)
    return turno



@router.get("/conceptos-detalles", response_model=List[schemas.ConceptoDetalleCreate])
async def read_repuestos(tipo: str,db: Session = Depends(get_db)):
    conceptos = mantenimientos_controller.read_conceptos_detalles(tipo,db)
    return conceptos



@router.post("/turnos/{turno_id}/detalles/{concepto_id}", response_model=schemas.DetalleMantenimientoBase)
def create_detalle(turno_id: uuid.UUID, concepto_id: uuid.UUID,cantidad:int, db: Session = Depends(get_db)):
    return mantenimientos_controller.agregar_detalle_mantenimiento(turno_id, concepto_id,cantidad,db)

@router.delete("/turnos/{turno_id}/detalles/{concepto_id}", response_model=schemas.DetalleMantenimientoBase)
def create_detalle(turno_id: uuid.UUID, concepto_id: uuid.UUID,cantidad:int, db: Session = Depends(get_db)):
    return mantenimientos_controller.eliminar_detalle_mantenimiento(turno_id, concepto_id,cantidad,db)