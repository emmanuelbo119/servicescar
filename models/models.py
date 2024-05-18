from sqlalchemy import Column, ForeignKey, Integer, String, Text, Double, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


from database import Base
import uuid

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = {'extend_existing': True} 
    uuidusuario = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    dni = Column(String(20), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    edad = Column(Integer, nullable=False)
    telefono = Column(String(20), nullable=False)
    asesor_consultas = relationship("AsesorConsulta", back_populates="usuario")
    automovilistas = relationship("Automovilista", back_populates="usuario")
    chofer_gruas = relationship("ChoferGrua", back_populates="usuario")



class AsesorConsulta(Base):
    __tablename__ = "asesor_consultas"
    __table_args__ = {'extend_existing': True} 
    uuidusuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidusuario"), primary_key=True)
    usuario = relationship("Usuario", back_populates="asesor_consultas")


class Automovilista(Base):
    __tablename__ = "automovilistas"
    __table_args__ = {'extend_existing': True} 
    uuidusuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidusuario"), primary_key=True)
    usuario = relationship("Usuario", back_populates="automovilistas")
    vehiculos = relationship("Vehiculo", back_populates="automovilista")


class ChoferGrua(Base):
    __tablename__ = "chofer_gruas"
    __table_args__ = {'extend_existing': True} 
    uuidusuario = Column(UUID(as_uuid=True), ForeignKey("usuarios.uuidusuario"), primary_key=True)
    tipocarnet = Column(String(50), nullable=False)
    usuario = relationship("Usuario", back_populates="chofer_gruas")


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
    costo = Column(Double, nullable=False)
    observacionesadicionales = Column(Text)
    tallermecanico_id = Column(UUID(as_uuid=True), ForeignKey("taller_mecanicos.uuidtallermecanico"))
    estado = Column(UUID(as_uuid=True), ForeignKey("estado_mantenimientos.uuidestadomantenimiento"))
    taller_mecanico = relationship("TallerMecanico")
    estado_mantenimiento = relationship("EstadoMantenimiento")

## CREO QUE NO ES NECESARIO REVISAR 
class MantenimientoXVehiculo(Base):
    __tablename__ = "mantenimientos_x_vehiculos"
    __table_args__ = {'extend_existing': True} 
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    uuidvehiculo = Column(UUID(as_uuid=True), ForeignKey("vehiculos.uuidvehiculo"), nullable=False)
    uuidmantenimiento = Column(UUID(as_uuid=True), ForeignKey("mantenimientos.uuidmantenimiento"), nullable=False)



class MarcaRepuesto(Base):
    __tablename__ = "marca_repuestos"
    __table_args__ = {'extend_existing': True} 
    uuidmarcarepuesto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    observaciones = Column(Text)


class MarcaVehiculo(Base):
    __tablename__ = "marca_vehiculos"
    __table_args__ = {'extend_existing': True} 
    uuidmarcavehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fechacreacion = Column(DateTime, nullable=False)
    fechamodificacion = Column(DateTime)


class ModeloVehiculo(Base):
    __tablename__ = "modelo_vehiculos"
    __table_args__ = {'extend_existing': True} 
    uuidmodelovehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)
    fechacreacion = Column(DateTime, nullable=False)
    fechamodificacion = Column(DateTime)


class Repuesto(Base):
    __tablename__ = "repuestos"
    __table_args__ = {'extend_existing': True} 
    uuidrepuesto = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    fabricante = Column(String(255), nullable=False)
    marca = Column(UUID(as_uuid=True), ForeignKey("marca_repuestos.uuidmarcarepuesto"))
    costo = Column(Double, nullable=False)
    marca_repuesto = relationship("MarcaRepuesto")



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
    repuesto = relationship("Repuesto")


class TallerMecanico(Base):
    __tablename__ = "taller_mecanicos"
    __table_args__ = {'extend_existing': True} 
    uuidtallermecanico = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=False)
    latitud = Column(Double, nullable=False)
    longitud = Column(Double, nullable=False)
    horarioatencion = Column(String(255), nullable=False)
    servicios = Column(Text)



class TipoServicioMantenimiento(Base):
    __tablename__ = "tipo_servicio_mantenimientos"
    __table_args__ = {'extend_existing': True} 
    uuidtiposerviciomantenimiento = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    descripcion = Column(Text)


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    __table_args__ = {'extend_existing': True} 
    uuidvehiculo = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    modelo = Column(UUID(as_uuid=True), ForeignKey("modelo_vehiculos.uuidmodelovehiculo"))
    automovilista_id = Column(UUID(as_uuid=True), ForeignKey("automovilistas.uuidusuario"))
    modelo_vehiculo = relationship("ModeloVehiculo")
    automovilista = relationship("Automovilista", back_populates="vehiculos")
