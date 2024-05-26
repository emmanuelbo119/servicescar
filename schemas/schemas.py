from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import re

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
    uuidusuario: UUID

    class Config:
        orm_mode = True


##  --------------------------- Vehiculo --------------------------------

class VehiculoBase(BaseModel):
    modelo_id: UUID
    automovilista_id: UUID
    color: str
    patente: Optional[str] = None
    anio: str
    marca_id:UUID
    fechaCreacion: datetime
    fechaModificacion: datetime

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    uuidvehiculo: UUID

    class Config:
        orm_mode = True




class MarcaVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechaCreacion: Optional[datetime] = None
    fechaModificacion: Optional[datetime] = None

class MarcaVehiculoCreate(MarcaVehiculoBase):
    pass

class MarcaVehiculo(MarcaVehiculoBase):
    uuidmarcavehiculo: UUID

class MarcaVehiculoBasic(BaseModel):
    nombre: str
    descripcion:  str

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

class ModeloVehiculo(ModeloVehiculoBase):
    uuidmodelovehiculo: UUID

    class Config:
        orm_mode = True


 
## ------------------------------------------Mantenimiento  ----------------------------------------------------------------


class EstadoMantenimientoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class EstadoMantenimientoCreate(EstadoMantenimientoBase):
    pass

class EstadoMantenimiento(EstadoMantenimientoBase):
    uuidestadomantenimiento: UUID

    class Config:
        orm_mode = True


class MantenimientoBase(BaseModel):
    fecha: datetime
    hora: datetime
    duracion: int
    servicio: str
    descripcion: str
    costo: float
    observacionesadicionales: Optional[str] = None
    tallermecanico_id: Optional[UUID] = None
    estado: Optional[UUID] = None

class MantenimientoCreate(MantenimientoBase):
    pass

class Mantenimiento(MantenimientoBase):
    uuidmantenimiento: UUID

    class Config:
        orm_mode = True


class TallerMecanicoBase(BaseModel):
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horarioatencion: str
    servicios: Optional[str] = None
    fechaCreacion: datetime
    fechaModificacion: datetime

class TallerMecanicoCreate(TallerMecanicoBase):
    pass

class TallerMecanico(TallerMecanicoBase):
    uuidtallermecanico: UUID

    class Config:
        orm_mode = True



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


## ----------------------------- Authenticated --------------------------------

class EmailPasswordRequestForm(BaseModel):
    email: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
