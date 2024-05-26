from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Text, Double, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base
import uuid

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

class ModeloVehiculo(Base):
    __tablename__ = "modelo_vehiculos"
    uuidmodelovehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"), nullable=False)
    
    # Relaciones
    marca = relationship("MarcaVehiculo", back_populates="modelos")

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    __table_args__ = {'extend_existing': True} 
    uuidvehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelo_id = Column(UUID(as_uuid=True), ForeignKey("modelo_vehiculos.uuidmodelovehiculo"))
    color = Column(String)
    patente = Column(String, nullable=True)
    anio = Column(String)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidUsuario"))
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"))
    
    # Relaciones
    modelo = relationship("ModeloVehiculo")
    usuario = relationship("Usuario", back_populates="vehiculos")
    mantenimientos = relationship("Mantenimiento", back_populates="vehiculo", cascade="all, delete-orphan")

class EstadoMantenimiento(Base):
    __tablename__ = "estado_mantenimientos"
    __table_args__ = {'extend_existing': True} 
    uuidestadomantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"
    __table_args__ = {'extend_existing': True} 
    uuidmantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha = Column(DateTime, nullable=False)
    hora = Column(DateTime, nullable=False)
    duracion = Column(Integer, nullable=False)
    servicio = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    costo = Column(Float, nullable=False)
    observacionesadicionales = Column(Text)
    tallermecanico_id = Column(UUID(as_uuid=True), ForeignKey("taller_mecanicos.uuidTallermecanico"))
    estado = Column(UUID(as_uuid=True), ForeignKey("estado_mantenimientos.uuidestadomantenimiento"))
    vehiculo_id = Column(UUID(as_uuid=True), ForeignKey("vehiculos.uuidvehiculo"), nullable=False)
    
    # Relaciones
    taller_mecanico = relationship("TallerMecanico")
    estado_mantenimiento = relationship("EstadoMantenimiento")
    vehiculo = relationship("Vehiculo", back_populates="mantenimientos")

class ServicioMantenimiento(Base):
    __tablename__ = "servicio_mantenimientos"
    __table_args__ = {'extend_existing': True} 
    uuidserviciomantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=False)
    tiposervicio = Column(UUID(as_uuid=True), ForeignKey("tipo_servicio_mantenimientos.uuidtiposerviciomantenimiento"))
    uuidmantenimiento = Column(UUID(as_uuid=True), ForeignKey("mantenimientos.uuidmantenimiento"), nullable=False)
    uuidrepuesto = Column(UUID(as_uuid=True), ForeignKey("repuestos.uuidrepuesto"))
    tipo_servicio_mantenimiento = relationship("TipoServicioMantenimiento")
    mantenimiento = relationship("Mantenimiento")

class TallerMecanico(Base):
    __tablename__ = "taller_mecanicos"
    __table_args__ = {'extend_existing': True} 
    uuidTallermecanico = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=False)
    latitud = Column(Double, nullable=False)
    longitud = Column(Double, nullable=False)
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


## entidad nueva agregar al diagrama de clases 


class Turno(Base):
    __tablename__ = "turnos"
    uuidTurno = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha = Column(DateTime, nullable=False)
    hora = Column(DateTime, nullable=False)
    estado = Column(UUID (as_uuid=True),ForeignKey("turnosEstados.uuidEstadoTurno"))
    uuidTallerMecanico = Column(UUID(as_uuid=True), ForeignKey("taller_mecanicos.uuidTallermecanico"), nullable=False)
    
    # Relaciones
    taller_mecanico = relationship("TallerMecanico", back_populates="turnos")


class EstadoTurno(Base):
    __tablename__ = "turnosEstados"
    uuidEstadoTurno = Column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4())
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)

                             
