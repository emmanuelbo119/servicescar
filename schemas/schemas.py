from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import re

dni_pattern = r"^\d{7,8}$"
telefono_pattern = r"^\d{10,11}$"

class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    dni: str = Field(..., pattern=dni_pattern)
    email: EmailStr
    edad: int =Field(..., gt=18, lt=150, description="Edad debe ser mayor a 18 y menor a 150")
    telefono: str = Field(..., pattern=telefono_pattern)

    @validator('email')
    def validate_email(cls, v):
        return v

    @validator('dni')
    def validate_dni(cls, v):
        if not re.match(dni_pattern, v):
            raise ValueError('Invalid DNI format')
        return v

    @validator('telefono')
    def validate_telefono(cls, v):
        if not re.match(telefono_pattern, v):
            raise ValueError('Invalid phone number format')
        return v

class UsuarioCreate(UsuarioBase):
    contraseña: str

class Usuario(UsuarioBase):
    uuidusuario: UUID

    class Config:
        orm_mode = True


class AsesorConsultaBase(BaseModel):
    uuidusuario: UUID

class AsesorConsultaCreate(AsesorConsultaBase):
    pass

class AsesorConsulta(AsesorConsultaBase):
    class Config:
        orm_mode = True


class AutomovilistaBase(BaseModel):
    uuidusuario: UUID

class AutomovilistaCreate(AutomovilistaBase):
    pass

class Automovilista(AutomovilistaBase):
    class Config:
        orm_mode = True


class ChoferGruaBase(BaseModel):
    uuidusuario: UUID
    tipocarnet: str

class ChoferGruaCreate(ChoferGruaBase):
    pass

class ChoferGrua(ChoferGruaBase):
    class Config:
        orm_mode = True


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


class MantenimientoXVehiculoBase(BaseModel):
    uuidvehiculo: UUID
    uuidmantenimiento: UUID

class MantenimientoXVehiculoCreate(MantenimientoXVehiculoBase):
    pass

class MantenimientoXVehiculo(MantenimientoXVehiculoBase):
    id: UUID

    class Config:
        orm_mode = True


class MarcaRepuestoBase(BaseModel):
    nombre: str
    observaciones: Optional[str] = None

class MarcaRepuestoCreate(MarcaRepuestoBase):
    pass

class MarcaRepuesto(MarcaRepuestoBase):
    uuidmarcarepuesto: UUID

    class Config:
        orm_mode = True


class MarcaVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechacreacion: datetime
    fechamodificacion: Optional[datetime] = None

class MarcaVehiculoCreate(MarcaVehiculoBase):
    pass

class MarcaVehiculo(MarcaVehiculoBase):
    uuidmarcavehiculo: UUID

    class Config:
        orm_mode = True


class ModeloVehiculoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    fechacreacion: datetime
    fechamodificacion: Optional[datetime] = None

class ModeloVehiculoCreate(ModeloVehiculoBase):
    pass

class ModeloVehiculo(ModeloVehiculoBase):
    uuidmodelovehiculo: UUID

    class Config:
        orm_mode = True


class RepuestoBase(BaseModel):
    nombre: str
    fabricante: str
    marca: Optional[UUID] = None
    costo: float

class RepuestoCreate(RepuestoBase):
    pass

class Repuesto(RepuestoBase):
    uuidrepuesto: UUID

    class Config:
        orm_mode = True


class ServicioMantenimientoBase(BaseModel):
    nombre: str
    descripcion: str
    tiposervicio: Optional[UUID] = None
    uuidmantenimiento: UUID
    uuidrepuesto: Optional[UUID] = None

class ServicioMantenimientoCreate(ServicioMantenimientoBase):
    pass

class ServicioMantenimiento(ServicioMantenimientoBase):
    uuidserviciomantenimiento: UUID

    class Config:
        orm_mode = True


class TallerMecanicoBase(BaseModel):
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    horarioatencion: str
    servicios: Optional[str] = None

class TallerMecanicoCreate(TallerMecanicoBase):
    pass

class TallerMecanico(TallerMecanicoBase):
    uuidtallermecanico: UUID

    class Config:
        orm_mode = True

class TipoServicioMantenimientoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class TipoServicioMantenimientoCreate(TipoServicioMantenimientoBase):
    pass

class TipoServicioMantenimiento(TipoServicioMantenimientoBase):
    uuidtiposerviciomantenimiento: UUID

    class Config:
        orm_mode = True



class VehiculoBase(BaseModel):
    modelo: Optional[UUID] = None
    automovilista_id: Optional[UUID] = None

class VehiculoCreate(VehiculoBase):
    pass

class Vehiculo(VehiculoBase):
    uuidvehiculo: UUID

    class Config:
        orm_mode = True
