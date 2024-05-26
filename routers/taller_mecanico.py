from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional
from uuid import UUID
from models import models
from schemas import schemas 
from database import get_db
from controllers import turnos as turnos_cotroller


router = APIRouter(
    prefix="/tallerMecanico",
    tags=["tallerMecanico"],
    responses={404: {"description": "Not found"}},
)

@router.get('/',response_model=List[schemas.TallerMecanico])
async def get_tallerMecanico(db: Session = Depends(get_db)):
    talleresMecanicos = db.query(models.TallerMecanico).all()
    return talleresMecanicos



@router.get("/{tallerMecanico_id}", response_model=schemas.TallerMecanico)
async def get_tallerMecanico(tallerMecanico_id: UUID, db: Session = Depends(get_db)):
    try:
        tallerMecanico = db.query(models.TallerMecanico).get(tallerMecanico_id).first()
        if not tallerMecanico:
            raise HTTPException(status_code=404, detail="TallerMecanico not found")
        return tallerMecanico
    except NoResultFound:
        raise HTTPException(status_code=404, detail="TallerMecanico not found")
    


@router.get("/{tallerMecanico_id}/turnosDisponibles", response_model=List[schemas.Turno])
async def read_available_turnos( tallerMecanico_id: UUID,start_date: Optional[datetime] = None,end_date: Optional[datetime] = None,db: Session = Depends(get_db)):
    turnos_disponnibles = turnos_cotroller.getTurnosDisponibles(tallerMecanico_id, db, start_date, end_date)
    return turnos_disponnibles