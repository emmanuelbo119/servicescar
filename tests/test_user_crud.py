import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..models import models
from ..database import Base, get_db
from ..main import app
import uuid

# Crear una base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base de datos y las tablas
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos de prueba
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def test_client():
    # Esta función se ejecutará una vez por cada módulo
    yield client

# Test data
test_user_data = {
    "nombre": "John",
    "apellido": "Doe",
    "dni": "12345678",
    "email": "john.doe@example.com",
    "contraseña": "password",
    "edad": 30,
    "telefono": "1234567890"
}

# Test 1: Crear un usuario
def test_create_user(test_client):
    response = test_client.post("/users/", json=test_user_data)
    assert response.status_code == 200
    