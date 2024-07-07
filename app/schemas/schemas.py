from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime

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

class MarcaVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

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

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    uuidvehiculo: UUID
    marca: MarcaVehiculoBasic
    modelo: ModeloVehiculoBasic

    class Config:
        orm_mode = True

class TallerMecanicoBase(BaseModel):
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horarioAtencion: str
    servicios: Optional[str] = None

class TallerMecanicoCreate(TallerMecanicoBase):
    pass

class TallerMecanico(TallerMecanicoBase):
    uuidTallermecanico: UUID

    class Config:
        orm_mode = True

class EstadoTurnoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EstadoTurnoCreate(EstadoTurnoBase):
    pass

class EstadoTurno(EstadoTurnoBase):
    uuidEstadoTurno: UUID

    class Config:
        orm_mode = True

class DetalleMantenimientoBase(BaseModel):
    tipo: str
    descripcion: str
    cantidad: int
    costo_unitario: float

class DetalleMantenimientoCreate(DetalleMantenimientoBase):
    pass

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

class DetalleMantenimiento(DetalleMantenimientoBase):
    uuidDetalle: UUID
    tarea_manual: Optional[TareaManual]
    repuesto: Optional[Repuesto]

    class Config:
        orm_mode = True

class EstadoMantenimientoBase(BaseModel):
    uuidEstadoMantenimiento: UUID
    nombre: str




class TurnoBase(BaseModel):
    fecha: datetime
    hora: datetime
    uuidTallerMecanico: UUID
    uuidEstadoTurno: UUID
    duracion: Optional[int] = 0
    kilometraje: Optional[int] = 0
    costo_total: Optional[float] = 0
    descripcion: Optional [str] = None
    estado: EstadoTurnoBase
    vehiculos: List[Vehiculo] = []
    cupo: Optional[int] = 1
    detalles: List[DetalleMantenimiento] = []

class TurnoCreate(TurnoBase):
    pass

class TurnoResponseReserva(TurnoBase):
    uuidTurno: UUID
    taller_mecanico: TallerMecanico
    estadoMantenimiento: EstadoMantenimientoBase
    class Config:
        orm_mode = True

class Turno(TurnoBase):
    uuidTurno: UUID
    detalles: List[DetalleMantenimiento] = []

    class Config:
        orm_mode = True

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
