from contextvars import Token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from datetime import datetime, timedelta
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm import Session
from controllers.auth import authenticate_user, create_access_token
import database
from schemas.schemas import TokenResponse, EmailPasswordRequestForm

ACCESS_TOKEN_EXPIRE_MINUTES = 30
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)




@router.post("/login", response_model=TokenResponse)
async def login_for_access_token(form_data: EmailPasswordRequestForm, db: Session = Depends(database.get_db)):
    print(f'email: {form_data.email}, password: {form_data.password}')
    user = authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}