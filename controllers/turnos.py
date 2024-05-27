from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import date, datetime, time, timedelta
from models import models  
from schemas import schemas
import uuid

def getTurnosDisponibles(tallermecanico_id: uuid.UUID, db: Session, start_date: date = None, end_date: date = None):
    ## Si no se proporciona la fecha de inicio y fin de la consulta se toma por defecto 1 semana desde la fecha actual 
    if not start_date:
        start_date = datetime.now()
    if not end_date:
        end_date = start_date + timedelta(weeks=1)
    # Filtrar los turnos disponibles usando JOIN
    turnos = db.query(models.Turno).join(models.EstadoTurno).filter(
        models.Turno.uuidTallerMecanico == tallermecanico_id,
        models.Turno.fecha >= start_date,
        models.Turno.fecha <= end_date,
        models.EstadoTurno.nombre=='Disponible'
        
    ).all()

    return turnos


def crear_turno(db: Session, turno:schemas.TurnoBase):
    db_turno = models.Turno(
        fecha=turno.fecha,
        hora=turno.hora,
        estado=turno.estado,
        uuidTallerMecanico=turno.tallermecanicoId
    )
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno


def getAllTurnos(db_turno:Session,skip,limit):
    turnos=db_turno.query(models.Turno).offset(skip).limit(limit).all()
    return turnos

def generate_turnos(tallermecanico_id: uuid.UUID, fechaInicio: date, fechaFin: date, horaInicio: time, horaFin: time, intervalo: int, db: Session):
    ## genera una lista de turnos entre fecha inicio y fecha fin
    ## el intervalod de tiempo debe ser en minutos 
      # Obtener el UUID del estado "disponible"
    estado_disponible = db.query(models.Turno.EstadoTurno).filter(models.Turno.EstadoTurno.nombre == 'Disponible').first()
    if not estado_disponible:
        raise HTTPException(status_code=404, detail="Estado 'disponible' no encontrado")
    turnos = []
    current_date = fechaInicio
    
    while current_date <= fechaFin:
        current_time = datetime.combine(current_date, horaInicio)
        end_time = datetime.combine(current_date, horaFin)
        
        while current_time <= end_time:
            turno = models.Turno(
                uuidTurno=uuid.uuid4(),
                fecha=current_date,
                hora=current_time,
                estado=estado_disponible.uuidEstadoTurno,
                uuidTallerMecanico=tallermecanico_id
            )
            db.add(turno)
            turnos.append(turno)
            current_time += timedelta(minutes=intervalo)
        current_date += timedelta(days=1)
    db.commit()
    return turnos