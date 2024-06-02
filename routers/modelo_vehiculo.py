from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List
import uuid
from models import models
from schemas import schemas
from database import get_db
#from controllers import users as user_controller

router = APIRouter(
    prefix="/modelos",
    tags=["modelos"],
    responses={404: {"description": "Not found"}},
    
)

@router.get("/", response_model=List[schemas.ModeloVehiculo])
def get_modelos(db: Session = Depends(get_db)):
    modelos = db.query(models.ModeloVehiculo).all()
    return modelos



