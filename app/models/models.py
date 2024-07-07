import enum
from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
import uuid



Base = declarative_base()

##Tablas de valores
class MarcaVehiculo(Base):
    __tablename__ = "marca_vehiculos"
    __table_args__ = {'extend_existing': True} 
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
    __table_args__ = {'extend_existing': True} 
    uuidmodelovehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"), nullable=False)
    
    # Relaciones
    marca = relationship("MarcaVehiculo", back_populates="modelos")

class TallerMecanico(Base):
    __tablename__ = "taller_mecanicos"
    __table_args__ = {'extend_existing': True}
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



class EstadoTurno(Base):
    __tablename__ = "turnosEstados"
    __table_args__ = {'extend_existing': True}
    uuidEstadoTurno = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    turnos = relationship("Turno", back_populates="estado")


class EstadoMantenimiento(Base):
    __tablename__ = "estado_mantenimiento"
    __table_args__ = {'extend_existing': True}
    uuidEstadoMantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(String(255), nullable=True)
    turno = relationship("Turno", back_populates="estadoMantenimiento", uselist=False)


class TipoDetalle(enum.Enum):
    TAREA_MANUAL = "TAREA_MANUAL"
    REPUESTO = "REPUESTO"


class TareaManual(Base):
    __tablename__ = "tarea_manual"
    uuidTarea = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    descripcion_tarea = Column(Text, nullable=False)
    tiempo_estimado = Column(Float, nullable=False)
    costo = Column(Float, nullable=False)
    detalle_id = Column(UUID(as_uuid=True), ForeignKey("detalle_mantenimientos.uuidDetalle"))
    
    detalle = relationship("DetalleMantenimiento", back_populates="tarea_manual")

class Repuesto(Base):
    __tablename__ = "repuesto"
    uuidRepuesto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre_repuesto = Column(String, nullable=False)
    marca_repuesto = Column(String, nullable=False)
    costo = Column(Float, nullable=False)
    detalle_id = Column(UUID(as_uuid=True), ForeignKey("detalle_mantenimientos.uuidDetalle"))
    
    detalle = relationship("DetalleMantenimiento", back_populates="repuesto")



## Tablas complejas 


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



class Vehiculo(Base):
    __tablename__ = "vehiculos"
    uuidvehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelo_id = Column(UUID(as_uuid=True), ForeignKey("modelo_vehiculos.uuidmodelovehiculo"))
    color = Column(String)
    patente = Column(String, nullable=True)
    anio = Column(String)
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    kilometraje = Column(Integer, nullable=True, default=0)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidUsuario"))
    marca_id = Column(UUID(as_uuid=True), ForeignKey("marca_vehiculos.uuidmarcavehiculo"))    
    # Relaciones
    modelo = relationship("ModeloVehiculo")
    usuario = relationship("Usuario", back_populates="vehiculos")
    marca = relationship("MarcaVehiculo", back_populates="vehiculos")
    turnos_relacionados = relationship("TurnoVehiculos", back_populates="vehiculo")

class Turno(Base):
    __tablename__ = "turnos"
    __table_args__ = {'extend_existing': True}
    uuidTurno = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fecha = Column(DateTime, nullable=False)
    hora = Column(DateTime, nullable=False)
    cupo = Column(Integer, nullable=False,default=1)
    duracion = Column(Integer, nullable=True, default=30)
    kilometraje_vehiculo = Column(Integer, nullable=True, default=0)
    costo_total = Column(Float, nullable=True,default=0)
    descripcion = Column(Text, nullable=True,default="")
    fechaCreacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fechaModificacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    uuidEstadoTurno = Column(UUID(as_uuid=True), ForeignKey("turnosEstados.uuidEstadoTurno"), nullable=False)
    uuidTallerMecanico = Column(UUID(as_uuid=True), ForeignKey("taller_mecanicos.uuidTallermecanico"), nullable=False)
    uuidEstadoMantenimiento = Column(UUID(as_uuid=True), ForeignKey("estado_mantenimiento.uuidEstadoMantenimiento"), nullable=False)    
    # Relaciones
    taller_mecanico = relationship("TallerMecanico", back_populates="turnos")
    estado = relationship("EstadoTurno", back_populates="turnos")
    detalles = relationship("DetalleMantenimiento", back_populates="turno")
    vehiculos_relacionados = relationship("TurnoVehiculos", back_populates="turno")
    estadoMantenimiento = relationship("EstadoMantenimiento", back_populates="turno")

class DetalleMantenimiento(Base):
    __tablename__ = "detalle_mantenimientos"
    uuidDetalle = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuidTurno = Column(UUID(as_uuid=True), ForeignKey("turnos.uuidTurno"), nullable=False)
    tipo = Column(Enum(TipoDetalle), nullable=False)
    descripcion = Column(Text, nullable=False)
    cantidad = Column(Integer, nullable=False)
    costo_unitario = Column(Float, nullable=False)
    
    tarea_manual = relationship("TareaManual", back_populates="detalle")
    repuesto = relationship("Repuesto", back_populates="detalle")
    turno = relationship("Turno", back_populates="detalles")

class TurnoVehiculos(Base):
    __tablename__ = "turno_vehiculos"
    __table_args__ = {'extend_existing': True}
    uuidTurnoVehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuidTurno = Column(UUID(as_uuid=True), ForeignKey("turnos.uuidTurno"))
    uuidVehiculo = Column(UUID(as_uuid=True), ForeignKey("vehiculos.uuidvehiculo"))

    # Relaciones
    turno = relationship("Turno", back_populates="vehiculos_relacionados")
    vehiculo = relationship("Vehiculo", back_populates="turnos_relacionados")
