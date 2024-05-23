from fastapi import FastAPI
from routers import auth, users,cars
from models import models
from schemas import schemas
from database import engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine,)

app = FastAPI() 

app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(cars.router, prefix='/cars', tags=['cars'] )

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 