from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Turno, DetalleMantenimiento, TareaManual, Repuesto,EstadoMantenimiento
from app.schemas import DetalleMantenimientoCreate
from app.database import get_db
from uuid import UUID


def agregar_detalle_mantenimiento(turno_id, detalle,db):
    turno = db.query(Turno).filter(Turno.uuidTurno == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    nuevo_detalle = DetalleMantenimiento(
        uuidTurno=turno_id,
        tipo=detalle.tipo,
        descripcion=detalle.descripcion,
        cantidad=detalle.cantidad,
        costo_unitario=detalle.costo_unitario
    )
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
    if detalle.tipo == "TAREA_MANUAL":
        nueva_tarea = TareaManual(
            descripcion_tarea=detalle.descripcion,
            costo=detalle.costo_unitario,
            detalle_id=nuevo_detalle.uuidDetalle
        )
        db.add(nueva_tarea)
        db.commit()
    elif detalle.tipo == "REPUESTO":
        nuevo_repuesto = Repuesto(
            nombre_repuesto=detalle.descripcion,  
            costo=detalle.costo_unitario,  
            detalle_id=nuevo_detalle.uuidDetalle
        )
        db.add(nuevo_repuesto)
        db.commit()
    estado_presupuestado = db.query(EstadoMantenimiento).filter(EstadoMantenimiento.nombre == "Presupuestado").first()
    if not estado_presupuestado:
        raise HTTPException(status_code=500, detail="Estado 'Presupuestado' no encontrado")
    turno.estadoMantenimiento = estado_presupuestado
    db.commit()
    db.refresh(turno)
    return nuevo_detalle



def eliminar_detalle_mantenimiento(turno_id, detalle_id, db: Session):
    detalle = db.query(DetalleMantenimiento).filter(
        DetalleMantenimiento.uuidDetalle == detalle_id,
        DetalleMantenimiento.uuidTurno == turno_id
    ).first()
    if not detalle:
        raise HTTPException(status_code=404, detail="Detalle de mantenimiento no encontrado")
    db.delete(detalle)
    db.commit()
    return detalle


def finalizar_presupuesto(turno_id, db):
    turno = db.query(Turno).filter(Turno.uuidTurno == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    total = 0.0
    for detalle in turno.detalles:
        total += detalle.cantidad * detalle.costo_unitario
    turno.costo_total = total
    estado_presupuestado = db.query(EstadoMantenimiento).filter(EstadoMantenimiento.nombre == "Presupuestado").first()
    if not estado_presupuestado:
        raise HTTPException(status_code=500, detail="Estado 'Presupuestado' no encontrado")
    turno.estadoMantenimiento = estado_presupuestado
    db.commit()
    db.refresh(turno)
    return turno


def cambiar_estado_mantenimiento(turno_id, nuevo_estado, db):
    turno = db.query(Turno).filter(Turno.uuidTurno == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    nuevo_estado_obj = db.query(EstadoMantenimiento).filter(EstadoMantenimiento.nombre == nuevo_estado).first()
    if not nuevo_estado_obj:
        raise HTTPException(status_code=404, detail="Estado de mantenimiento no encontrado")
    turno.estadoMantenimiento = nuevo_estado_obj
    db.commit()
    db.refresh(turno)
    return turnos