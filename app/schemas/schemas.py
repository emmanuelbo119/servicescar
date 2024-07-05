from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

## -------------------------------------- Usuarios --------------------------------
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    dni: str 
    email: EmailStr
    edad: int 
    telefono: str
    username: str 

    @validator('email')
    def validate_email(cls, v):
        return v

class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    fechaCreacion: datetime
    fechaModificacion: Optional[datetime]
    uuidUsuario: UUID

    class Config:
        orm_mode = True

## -------------------------------------- Vehiculos --------------------------------
class MarcaVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechaCreacion: Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None

class MarcaVehiculoCreate(MarcaVehiculoBase):
    pass

class MarcaVehiculo(MarcaVehiculoBase):
    uuidmarcavehiculo: UUID

    class Config:
        orm_mode = True

class MarcaVehiculoBasic(BaseModel):
    uuidmarcavehiculo: UUID
    nombre: str

    class Config:
        orm_mode = True

class ModeloVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechaCreacion: datetime
    fechaModificacion: Optional[datetime] = None
    marca: MarcaVehiculoBase

class ModeloVehiculoCreate(ModeloVehiculoBase):
    pass

class ModeloVehiculoBasic(BaseModel):
    uuidmodelovehiculo: UUID
    nombre: str

    class Config:
        orm_mode = True

class ModeloVehiculo(ModeloVehiculoBase):
    uuidmodelovehiculo: UUID

    class Config:
        orm_mode = True

class VehiculoBase(BaseModel):
    modelo_id: UUID
    usuario_id: UUID
    color: str
    patente: Optional[str] = None
    anio: str
    marca_id: UUID
    kilometraje: Optional[int] = 0
    fechaCreacion: Optional[datetime]
    fechaModificacion: Optional[datetime]

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    uuidvehiculo: UUID
    marca: MarcaVehiculoBasic
    modelo: ModeloVehiculoBasic

    class Config:
        orm_mode = True

## -------------------------------------- Taller Mecanico --------------------------------
class TallerMecanicoBase(BaseModel):
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horarioAtencion: str
    servicios: Optional[str] = None
    fechaCreacion: Optional[datetime]
    fechaModificacion: Optional[datetime]

class TallerMecanicoCreate(TallerMecanicoBase):
    pass

class TallerMecanico(TallerMecanicoBase):
    uuidTallermecanico: UUID

    class Config:
        orm_mode = True

## -------------------------------------- Tipo Servicio Mantenimiento --------------------------------
class TipoServicioMantenimientoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechaCreacion: datetime
    fechaModificacion: datetime

class TipoServicioMantenimientoCreate(TipoServicioMantenimientoBase):
    pass

class TipoServicioMantenimiento(TipoServicioMantenimientoBase):
    uuidtiposerviciomantenimiento: UUID

    class Config:
        orm_mode = True

## -------------------------------------- Estado Turno --------------------------------
class EstadoTurnoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EstadoTurnoCreate(EstadoTurnoBase):
    pass

class EstadoTurno(EstadoTurnoBase):
    uuidEstadoTurno: UUID

    class Config:
        orm_mode = True

## -------------------------------------- Turno --------------------------------
class TurnoBase(BaseModel):
    fecha: datetime
    hora: datetime
    uuidTallerMecanico: UUID
    uuidEstadoTurno: UUID
    duracion: Optional[int] = 0
    kilometraje_vehiculo: Optional[int] = 0
    costo_total: float
    descripcion: str
    uuidTipoServicioMantenimiento: UUID
    uuidVehiculo: UUID
    estado: EstadoTurnoBase
    vehiculos: List[VehiculoBase] = []
    cupo: Optional[int] = 1

class TurnoCreate(TurnoBase):
    pass

class TurnoResponseReserva(TurnoBase):
    uuidTurno: UUID
    taller_mecanico: TallerMecanico
    vehiculos: List[Vehiculo]

class Turno(TurnoBase):
    uuidTurno: UUID
    detalles: List['DetalleMantenimiento'] = []

    class Config:
        orm_mode = True

## -------------------------------------- Detalle Mantenimiento --------------------------------
class DetalleMantenimientoBase(BaseModel):
    tipo: str
    descripcion: str
    cantidad: int
    costo_unitario: float

class DetalleMantenimientoCreate(DetalleMantenimientoBase):
    pass

class DetalleMantenimiento(DetalleMantenimientoBase):
    uuidDetalle: UUID
    tarea_manual: Optional['TareaManual']
    repuesto: Optional['Repuesto']

    class Config:
        orm_mode = True

class TareaManualBase(BaseModel):
    descripcion_tarea: str
    tiempo_estimado: float

class TareaManualCreate(TareaManualBase):
    pass

class TareaManual(TareaManualBase):
    uuidTarea: UUID

    class Config:
        orm_mode = True

class RepuestoBase(BaseModel):
    nombre_repuesto: str
    marca_repuesto: str

class RepuestoCreate(RepuestoBase):
    pass

class Repuesto(RepuestoBase):
    uuidRepuesto: UUID

    class Config:
        orm_mode = True

## -------------------------------------- Chofer Grua --------------------------------
class ChoferGruaBase(UsuarioBase):
    tipoCarnet: Optional[str]
    numeroCarnet: Optional[str]

class ChoferGruaCreate(ChoferGruaBase):
    pass

class ChoferGrua(ChoferGruaBase):
    uuidChoferGrua: str

    class Config:
        orm_mode = True

## -------------------------------------- Asesor --------------------------------------
class AsesorBase(UsuarioBase):
    legajo: Optional[str]

class AsesorCreate(AsesorBase):
    pass

class Asesor(AsesorBase):
    uuidAsesor: str

    class Config:
        orm_mode = True

## -------------------------------------- Authenticated --------------------------------
class EmailPasswordRequestForm(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    uuidUsuario: UUID

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

DetalleMantenimiento.update_forward_refs()
