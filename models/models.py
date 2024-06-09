from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Table, Text, Double, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
import uuid


class TurnoVehiculos(Base):
    __tablename__ = "turno_vehiculos"
    __table_args__ = {'extend_existing': True}
    uuidTurnoVehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    turno_id = Column(UUID(as_uuid=True), ForeignKey("turnos.uuidTurno"))
    vehiculo_id = Column(UUID(as_uuid=True), ForeignKey("vehiculos.uuidvehiculo"))

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True} 
    uuidUsuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    telefono = Column(String(20), nullable=False)
    username = Column(String(255), nullable=False)
    fechaCreacion = Column(DateTime(timezone=True), server_default=func.now())
    fechaModificacion = Column(DateTime(timezone=True), onupdate=func.now())
    ## relaciones
    vehiculos = relationship("Vehiculo", back_populates="usuario")

class MarcaVehiculo(Base):
    __tablename__ = "marca_vehiculos"
    uuidmarcavehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fechacreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechamodificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    modelos = relationship("ModeloVehiculo", back_populates="marca", cascade="all, delete-orphan")
    vehiculos = relationship("Vehiculo", back_populates="marca")

class ModeloVehiculo(Base):
    __tablename__ = "modelo_vehiculos"
    uuidmodelovehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text,nullable=True)
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"), nullable=False)
    
    # Relaciones
    marca = relationship("MarcaVehiculo", back_populates="modelos")


class TallerMecanico(Base):
    __tablename__ = "taller_mecanicos"
    uuidTallermecanico = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    horarioAtencion = Column(String(255), nullable=False)
    servicios = Column(Text)
    fechaCreacion = Column(DateTime(timezone=True), server_default=func.now())
    fechaModificacion = Column(DateTime(timezone=True), onupdate=func.now())
    turnos = relationship("Turno", back_populates="taller_mecanico", cascade="all, delete-orphan")
    
class TipoServicioMantenimiento(Base):
    __tablename__ = "tipo_servicio_mantenimientos"
    __table_args__ = {'extend_existing': True} 
    uuidtiposerviciomantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)

class Turno(Base):
    __tablename__ = "turnos"
    uuidTurno = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha = Column(DateTime, nullable=False)
    hora = Column(DateTime, nullable=False)
    uuidEstadoTurno = Column(UUID(as_uuid=True), ForeignKey("turnosEstados.uuidEstadoTurno"), nullable=False)
    uuidTallerMecanico = Column(UUID(as_uuid=True), ForeignKey("taller_mecanicos.uuidTallermecanico"), nullable=False)
    cupo=Column(Integer, nullable=False)

    taller_mecanico = relationship("TallerMecanico", back_populates="turnos")
    estado = relationship("EstadoTurno", back_populates="turnos")
    vehiculos = relationship("Vehiculo", secondary="turno_vehiculos", back_populates="turnos")

class EstadoTurno(Base):
    __tablename__ = "turnosEstados"
    __table_args__ = {'extend_existing': True}
    uuidEstadoTurno = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    turnos = relationship("Turno", back_populates="estado")



class Vehiculo(Base):
    __tablename__ = "vehiculos"
    uuidvehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelo_id = Column(UUID(as_uuid=True), ForeignKey("modelo_vehiculos.uuidmodelovehiculo"))
    color = Column(String)
    patente = Column(String, nullable=True)
    anio = Column(String)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidUsuario"))
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"))
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    modelo = relationship("ModeloVehiculo")
    usuario = relationship("Usuario", back_populates="vehiculos")
    marca = relationship("MarcaVehiculo", back_populates="vehiculos")
    turnos = relationship("Turno", secondary="turno_vehiculos", back_populates="vehiculos")