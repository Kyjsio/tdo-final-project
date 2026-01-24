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


# 2. Fixture bazy danych: Tworzy tabele przed testem, usuwa po teście
@pytest.fixture(scope="function")
def db_session():
    # Tworzymy tabele
    ModelsBase.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Usuwamy tabele (czysty start dla kolejnego testu)
        ModelsBase.metadata.drop_all(bind=engine)


# 3. Fixture klienta: Nadpisuje zależność get_db w aplikacji
@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass  # Session closing is handled by db_session fixture

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Czyścimy override po testach
    app.dependency_overrides.clear()


# 4. Fixture pomocniczy: Tworzy użytkownika i zwraca token (dla testów wymagających logowania)
@pytest.fixture
def auth_header(client):
    # 1. Rejestracja
    # Zmieniamy json={...} na params={...}, bo błąd mówił "loc: query"
    # Dodajemy też 'email', 'role', itp. na wszelki wypadek
    client.post(
        "/auth/register",
        params={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "user"  # Czasami wymagane
        }
    )

    # 2. Logowanie (To jest standard OAuth2 - form data)
    response = client.post(
        "/auth/token",
        data={"username": "testuser", "password": "password123"}
    )

    # Jeśli tu nadal będzie błąd, dowiemy się dlaczego
    assert response.status_code == 200, f"Błąd w fixturze logowania: {response.text}"

    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}