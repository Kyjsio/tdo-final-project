import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.models import Base as ModelsBase

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    ModelsBase.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        ModelsBase.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def auth_header(client):
    client.post(
        "/auth/register",
        params={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"
        }
    )

    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200, f"Błąd w fixturze logowania: {response.text}"

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}