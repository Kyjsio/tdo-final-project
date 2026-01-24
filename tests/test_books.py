def test_get_books_initial(client):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0, "Baza powinna zawierać domyślne książki"
    assert "title" in data[0]

def test_create_book_authorized(client, auth_header):
    response = client.post(
        "/books/",
        json={
            "title": "Moja Testowa Książka",
            "author": "Ja",
            "publication_year": 2024,
            "description": "Opis"
        },
        headers=auth_header
    )
    assert response.status_code in [200, 201], f"Błąd tworzenia: {response.text}"
    data = response.json()
    assert data["title"] == "Moja Testowa Książka"

def test_create_book_unauthorized(client):
    response = client.post(
        "/books/",
        json={"title": "Hacker Book", "author": "Hacker", "publication_year": 2000}
    )
    assert response.status_code == 401