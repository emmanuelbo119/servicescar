from datetime import date, datetime, time
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
import models
from schemas import schemas
from typing import List 
from database import SessionLocal, engine, get_db
from uuid import UUID
from controllers import turnos as turnos_controller



router = APIRouter(
    prefix="/turnos",
    tags=["turnos"],
    responses={404: {"description": "Not found"}},

)

@router.get("/",response_model=schemas.Turno)
async def read_turnos(skip: int=0,limit:int=10,db:Session=Depends(get_db)) :
    turnos = turnos_controller.getAllTurnos(db,skip,limit)




@router.post("/CrearTurnos", response_model=List[schemas.Turno])
def create_turnos(
    tallermecanico_id: UUID,
    fechaInicio: date,
    fechaFin: date,
    horaInicio: time,
    horaFin: time,
    intervalo: int,
    db: Session = Depends(get_db)
):
    return turnos_controller.generate_turnos(tallermecanico_id, fechaInicio, fechaFin, horaInicio, horaFin, intervalo, db)