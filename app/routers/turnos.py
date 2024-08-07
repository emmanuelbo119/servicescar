from datetime import date, datetime, time
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session 
from app.schemas import TurnoResponseReserva,Turno,TurnoREsponseDetail
from typing import List 
from app.database import SessionLocal, engine, get_db
from uuid import UUID
from app.controllers import turnos as turnos_controller,zoho_billing
from app.schemas import TurnoBase



router = APIRouter(
    prefix="/turnos",
    tags=["turnos"],
    responses={404: {"description": "Not found"}},

)

@router.get("/", response_model=List[Turno])
def get_turnos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    marcas = turnos_controller.get_turnos(db, skip=skip, limit=limit)
    return marcas


@router.post("/CrearTurnos", response_model=List[Turno])
def create_turnos(
    tallermecanico_id: UUID,
    fechaInicio: date,
    fechaFin: date,
    horaInicio: time,
    horaFin: time,
    intervalo: int,
    cupo: int,
    db: Session = Depends(get_db)
):
    return turnos_controller.generate_turnos(tallermecanico_id, fechaInicio, fechaFin, horaInicio, horaFin, intervalo,cupo, db)



@router.get("/{turno_id}", response_model=List[TurnoREsponseDetail])
async def getTurnoByID(turno_id: UUID, db: Session = Depends(get_db)):
    return turnos_controller.get_turnosById(db, turno_id)


@router.post("/{turno_id}/reservar", response_model=TurnoResponseReserva)
async def reservar_turno(turno_id: UUID,vehiculo_id: UUID, db: Session = Depends(get_db)):
    return turnos_controller.reservarTurno(db, turno_id,vehiculo_id)


@router.get("/{usuario_id}/turnos", response_model=List[TurnoResponseReserva])
async def get_turnos_by_usuario(usuario_id: UUID, db: Session = Depends(get_db)):
    return turnos_controller.get_turnos_by_usuario(db, usuario_id)



@router.post("/{turno_id}/", response_model=TurnoResponseReserva)
async def pagar_turnos_(turno_id: UUID, db: Session = Depends(get_db)):
    return turnos_controller.pagar_turno(db, turno_id)


@router.post("/{turno_id}/crear_factura")
async def crear_factura_turno(turno_id: UUID, db: Session = Depends(get_db)):
    return zoho_billing.crear_factura_from_turno(db,turno_id,5364125000000089552,5375979000000088100,'2024-08-03')