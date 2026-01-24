import uuid


def test_register_user(client):
    unique_code = str(uuid.uuid4())[:8]

    response = client.post(
        "/auth/register",
        params={
            "username": f"user_{unique_code}",
            "email": f"test_{unique_code}@example.com",
            "password": "password123",
            "role": "user"
        }
    )
    assert response.status_code == 201, f"Rejestracja nieudana: {response.text}"

def test_login_user(client):
    client.post(
        "/auth/register",
        params={"username": "login_user", "email": "login@example.com", "password": "password123"}
    )
    response = client.post(
        "/auth/token",
        data={"username": "login_user", "password": "password123"}
    )
    assert response.status_code == 200, f"Logowanie nieudane: {response.text}"
    data = response.json()
    assert "access_token" in data