from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import Turno, DetalleMantenimiento,EstadoMantenimiento,EstadoTurno
from app.schemas import DetalleMantenimientoCreate
from app.models import ConceptoDetalle
from uuid import UUID



def agregar_detalle_mantenimiento(turno_id, concepto_id,cantidad, db):
    turno = db.query(Turno).filter(Turno.uuidTurno == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    concepto = db.query(ConceptoDetalle).filter(ConceptoDetalle.uuidConcepto == concepto_id).first()
    if not concepto:
        raise HTTPException(status_code=404, detail="Concepto de detalle no encontrado")

    nuevo_detalle = DetalleMantenimiento(
        uuidTurno=turno_id,
        descripcion=concepto.descripcion,
        cantidad=cantidad,
        costo_unitario=concepto.costo,
        uuidConcepto=concepto.uuidConcepto,
        costo_total=concepto.costo * cantidad
    )
    print(nuevo_detalle)
    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)
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


def finalizar_presupuesto(turno_id, estado, db):
    turno = db.query(Turno).filter(Turno.uuidTurno == turno_id).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    total = 0.0
    for detalle in turno.detalles:
        total += detalle.cantidad * detalle.costo_unitario
    turno.costo_total = total
    
    estado_presupuestado = db.query(EstadoMantenimiento).filter(EstadoMantenimiento.nombre == estado).first()
    estado_turno = db.query(EstadoTurno).filter(EstadoTurno.nombre == 'En Progreso').first()
    if not estado_presupuestado:    
        raise HTTPException(status_code=500, detail="Estado no encontrado")
    
    turno.uuidEstadoMantenimiento = estado_presupuestado.uuidEstadoMantenimiento
    if estado =='Completado':
        turno.uuidEstadoTurno= estado_turno.uuidEstadoTurno
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
    return turno


def read_conceptos_detalles(tipo,db):
    return db.query(ConceptoDetalle).filter(ConceptoDetalle.tipo_concepto==tipo).all()


