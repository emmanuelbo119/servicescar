from typing import List
from sqlalchemy.orm import Session,joinedload
from fastapi import HTTPException
from datetime import date, datetime, time, timedelta
from app.models import EstadoTurno as EstadoTurnoModel
from app.models import Turno as TurnoModel 
from app.models import Vehiculo as VehiculoModel
from app.models import TallerMecanico as TallerMecanicoModelModel
from app.models import Usuario as UserModel
from app.models import MarcaVehiculo as MarcaModel
from app.models import ModeloVehiculo as ModeloVehiculoModel
from app.models import EstadoMantenimiento as EstadoMantenimientoModel
from app.models.models import TurnoVehiculos
from app.schemas import schemas
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
    
    estado_mantenimiento_solicitado= db.query(EstadoMantenimientoModel).filter(EstadoMantenimientoModel.nombre == 'Solicitado').first()
    if not estado_mantenimiento_solicitado:
        raise HTTPException(status_code=404, detail="Estado 'Solicitado' no encontrado")
    
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
                cupo=cupo,
                costo_total=0 ,
                descripcion="",
                uuidEstadoMantenimiento=estado_mantenimiento_solicitado.uuidEstadoMantenimiento

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
            joinedload(TurnoModel.vehiculos_relacionados).joinedload(TurnoVehiculos.vehiculo).joinedload(VehiculoModel.modelo).joinedload(ModeloVehiculoModel.marca),
            joinedload(TurnoModel.taller_mecanico),
            joinedload(TurnoModel.estado)
        )\
        .first()
    
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    if turno.estado.nombre != 'Disponible':
        raise HTTPException(status_code=400, detail="Turno no disponible")
    
    if turno.cupo <= 0:
        raise HTTPException(status_code=400, detail="No hay cupos disponibles")
    
    turno.cupo -= 1

    vehiculo = db.query(VehiculoModel).filter(VehiculoModel.uuidvehiculo == vehiculo_id).first()
    if not vehiculo:
        raise HTTPException(status_code=404, detail=f"Vehiculo {vehiculo_id} no encontrado")
    
    turno_vehiculo = TurnoVehiculos(uuidTurno=turno_id, uuidVehiculo=vehiculo_id)
    try:
        db.add(turno_vehiculo)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error al asignar vehiculo al turno: " + str(e))

    if turno.cupo == 0:
        estado_ocupado = db.query(EstadoTurnoModel).filter(EstadoTurnoModel.nombre == 'Ocupado').first()
        if not estado_ocupado:
            raise HTTPException(status_code=404, detail="Estado 'Ocupado' no encontrado")
        turno.estado = estado_ocupado
        estado_mantenimiento_solicitado= db.query(EstadoMantenimientoModel).filter(EstadoMantenimientoModel.nombre == 'Solicitado').first()
        if not estado_mantenimiento_solicitado:
            raise HTTPException(status_code=404, detail="Estado 'Solicitado' no encontrado")
        turno.estadoMantenimiento = estado_mantenimiento_solicitado
    db.commit()
    db.refresh(turno)

    vehiculos = db.query(VehiculoModel).join(TurnoVehiculos).filter(TurnoVehiculos.uuidTurno == turno.uuidTurno).all()
    
    estado_turno_dict = {
        "uuidEstadoTurno": turno.estado.uuidEstadoTurno,
        "nombre": turno.estado.nombre,
        "descripcion": turno.estado.descripcion
    }

    taller_mecanico_dict = {
        "uuidTallermecanico": turno.taller_mecanico.uuidTallermecanico,
        "nombre": turno.taller_mecanico.nombre,
        "direccion": turno.taller_mecanico.direccion,
        "latitud": turno.taller_mecanico.latitud,
        "longitud": turno.taller_mecanico.longitud,
        "horarioAtencion": turno.taller_mecanico.horarioAtencion,
        "servicios": turno.taller_mecanico.servicios
    }

    vehiculos_dict = [
        {
            "uuidvehiculo": vehiculo.uuidvehiculo,
            "modelo_id": vehiculo.modelo_id,
            "usuario_id": vehiculo.usuario_id,
            "color": vehiculo.color,
            "patente": vehiculo.patente,
            "anio": vehiculo.anio,
            "marca_id": vehiculo.marca_id,
            "kilometraje": vehiculo.kilometraje,
            "marca": {
                "uuidmarcavehiculo": vehiculo.marca.uuidmarcavehiculo,
                "nombre": vehiculo.marca.nombre,
                "descripcion": vehiculo.marca.descripcion
            },
            "modelo": {
                "uuidmodelovehiculo": vehiculo.modelo.uuidmodelovehiculo,
                "nombre": vehiculo.modelo.nombre,
                "descripcion": vehiculo.modelo.descripcion
            }
        }
        for vehiculo in vehiculos
    ]

    detalles_dict = [
        {
            "uuidDetalle": detalle.uuidDetalle,
            "tipo": detalle.tipo,
            "descripcion": detalle.descripcion,
            "cantidad": detalle.cantidad,
            "costo_unitario": detalle.costo_unitario
        }
        for detalle in turno.detalles
    ]

    turno_response = schemas.TurnoResponseReserva(
        uuidTurno=turno.uuidTurno,
        taller_mecanico=taller_mecanico_dict,
        vehiculos=vehiculos_dict,
        fecha=turno.fecha,
        hora=turno.hora,
        uuidTallerMecanico=turno.uuidTallerMecanico,
        uuidEstadoTurno=turno.uuidEstadoTurno,
        duracion=turno.duracion,
        kilometraje_vehiculo=turno.kilometraje_vehiculo,
        costo_total=turno.costo_total,
        descripcion=turno.descripcion,
        estado=estado_turno_dict,
        cupo=turno.cupo,
        detalles=detalles_dict
    )
    
    return turno_response


def get_turnos(db: Session, skip: int, limit: int):
    turnos = db.query(TurnoModel).join(EstadoTurnoModel).offset(skip).limit(limit).all()
    return turnos

def get_turnosById(db: Session,turno_id:uuid.UUID):
    turnos = db.query(TurnoModel).filter(TurnoModel.uuidTurno == turno_id)
    return turnos




def CancelarTurno(db: Session, turno_id: uuid.UUID):

    turno = db.query(TurnoModel)\
        .filter(TurnoModel.uuidTurno == turno_id)\
        .first()
    
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    if turno.estado.nombre != 'Ocupado':
        raise HTTPException(status_code=400, detail="Turno Disponble, no se puede cancelar")

    estado_ocupado = db.query(EstadoTurnoModel).filter(EstadoTurnoModel.nombre == 'Disponible').first()
    if not estado_ocupado:
        raise HTTPException(status_code=404, detail="Estado 'Disponible' no encontrado")
    turno.estado = estado_ocupado
    db.commit()
    db.refresh(turno)
    return turno


def get_turnos_by_usuario(db: Session, usuario_id: uuid.UUID):
    turnos = db.query(TurnoModel)\
        .join(TurnoVehiculos, TurnoModel.uuidTurno == TurnoVehiculos.uuidTurno)\
        .join(VehiculoModel, TurnoVehiculos.uuidVehiculo == VehiculoModel.uuidvehiculo)\
        .join(EstadoMantenimientoModel, EstadoMantenimientoModel.uuidEstadoMantenimiento == TurnoModel.uuidEstadoMantenimiento)\
        .filter(VehiculoModel.usuario_id == usuario_id)\
        .options(
            joinedload(TurnoModel.estado),
            joinedload(TurnoModel.taller_mecanico)
        ).all()
    if not turnos:
        raise HTTPException(status_code=404, detail="No se encontraron turnos para este usuario")
    
    return turnos
