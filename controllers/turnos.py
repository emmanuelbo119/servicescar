from typing import List
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import date, datetime, time, timedelta
from models import EstadoTurno as EstadoTurnoModel
from models import Turno as TurnoModel 
from models import Vehiculo as VehiculoModel
from models import TallerMecanico as TallerMecanicoModelModel
from models import Usuario as UserModel
from models import MarcaVehiculo as MarcaModel
from models import ModeloVehiculo as ModeloVehiculoModel
from schemas import schemas
import uuid

def getTurnosDisponibles(tallermecanico_id: uuid.UUID, db: Session, start_date: date = None, end_date: date = None):
    ## Si no se proporciona la fecha de inicio y fin de la consulta se toma por defecto 1 semana desde la fecha actual 
    if not start_date:
        start_date = datetime.now()
    if not end_date:
        end_date = start_date + timedelta(weeks=1)
    # Filtrar los turnos disponibles usando JOIN
    print(start_date)
    print(end_date)
    turnos = db.query(TurnoModel).join(EstadoTurnoModel).filter(
        TurnoModel.uuidTallerMecanico == tallermecanico_id,
        TurnoModel.fecha >= start_date,
        TurnoModel.fecha <= end_date,
        EstadoTurnoModel.nombre=='Disponible'
        
    ).all()

    return turnos


def crear_turno(db: Session, turno:schemas.TurnoBase):
    db_turno = TurnoModel(
        fecha=turno.fecha,
        hora=turno.hora,
        estado=turno.estado,
        uuidTallerMecanico=turno.tallermecanicoId
    )
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno


def generate_turnos(tallermecanico_id, fechaInicio, fechaFin, horaInicio, horaFin, intervalo, cupo, db):
    estado_disponible = db.query(EstadoTurnoModel).filter(EstadoTurnoModel.nombre == 'Disponible').first()
    if not estado_disponible:
        raise HTTPException(status_code=404, detail="Estado 'Disponible' no encontrado")
    
    if not cupo:
        cupo = 1
    
    turnos = []
    current_date = fechaInicio
    
    while current_date <= fechaFin:
        current_time = datetime.combine(current_date, horaInicio)
        end_time = datetime.combine(current_date, horaFin)
        
        while current_time <= end_time:
            turno = TurnoModel(
                uuidTurno=uuid.uuid4(),
                fecha=current_date,
                hora=current_time,
                uuidEstadoTurno=estado_disponible.uuidEstadoTurno,
                uuidTallerMecanico=tallermecanico_id,
                uuidVehiculo=None,
                cupo=cupo  
            )
            db.add(turno)
            turnos.append(turno)
            current_time += timedelta(minutes=intervalo)
        current_date += timedelta(days=1)
    
    db.commit()
    return turnos



def reservarTurno(db: Session, turno_id: uuid.UUID, vehiculo_id: uuid.UUID):
    turno = db.query(TurnoModel)\
        .filter(TurnoModel.uuidTurno == turno_id)\
        .options(
            joinedload(TurnoModel.vehiculos).joinedload(VehiculoModel.modelo).joinedload(ModeloVehiculoModel.marca),
            joinedload(TurnoModel.taller_mecanico),
            joinedload(TurnoModel.estado)
        )\
        .first()
    
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    # Verificar si el turno está ocupado
    if turno.estado.nombre != 'Disponible':
        raise HTTPException(status_code=400, detail="Turno no disponible")
    
    # Verificar si hay cupos disponibles
    if turno.cupo <= 0:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles")
    
    # Disminuir el cupo en 1
    turno.cupo -= 1

    # Asignar el vehiculo al turno
    vehiculo = db.query(VehiculoModel).filter(VehiculoModel.uuidvehiculo == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail=f"Vehiculo {vehiculo_id} no encontrado")
    try:
        turno.vehiculos.append(vehiculo)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al asignar vehiculo al turno: " + str(e))
    

    # Verificar si el contador de cupo queda en 0 y marcar el turno como ocupado
    if turno.cupo == 0:
        estado_ocupado = db.query(EstadoTurnoModel).filter(EstadoTurnoModel.nombre == 'Ocupado').first()
        if not estado_ocupado:
            raise HTTPException(status_code=404, detail="Estado 'Ocupado' no encontrado")
        turno.estado = estado_ocupado
    
    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(turno)
    
    return turno



def get_turnos(db: Session, skip: int, limit: int):
    turnos = db.query(TurnoModel).join(EstadoTurnoModel).offset(skip).limit(limit).all()
    return turnos

def get_turnosById(db: Session,turno_id:uuid.UUID):
    turnos = db.query(TurnoModel).filter(TurnoModel.uuidTurno == turno_id)
    return turnos




def CancelarTurno(db: Session, turno_id: uuid.UUID):
    # Obtener el turno por su ID
    turno = db.query(TurnoModel)\
        .filter(TurnoModel.uuidTurno == turno_id)\
        .first()
    
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    # Verificar el estado actual del turno usando la relación estado
    if turno.estado.nombre != 'Ocupado':
        raise HTTPException(status_code=400, detail="Turno Disponble, no se puede cancelar")

    # Obtener el objeto del estado 'Ocupado'
    estado_ocupado = db.query(EstadoTurnoModel).filter(EstadoTurnoModel.nombre == 'Disponible').first()
    if not estado_ocupado:
        raise HTTPException(status_code=404, detail="Estado 'Disponible' no encontrado")
    
    # Actualizar el estado del turno usando la relación ORM
    turno.estado = estado_ocupado
    db.commit()
    db.refresh(turno)
    return turno



# def get_turno_by_user(db: Session, user_id: uuid.UUID):
#     turno = db.query(UserModel).filter(UserModel.uuidUsuario == user_id)

#         .join(EstadoTurnoModel)\
#         .filter(TurnoModel.uuidTurno == user_id)\
#         .first()
    
#     if not turno:
#         raise HTTPException(status_code=404, detail="Turno no encontrado")
#     return turno