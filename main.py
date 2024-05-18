from fastapi import FastAPI
from routers import users
from models import models
from schemas import schemas
from database import engine


models.Base.metadata.create_all(bind=engine,)

app = FastAPI() 

app.include_router(users.router, prefix="/api", tags=["users"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 