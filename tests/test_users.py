import pytest

def test_create_user_returns_created_user(client, valid_user):
    response = client.post("/users", json=valid_user)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["name"] == valid_user["name"]
    assert body["email"] == valid_user["email"]
    assert body["age"] == valid_user["age"]

def test_list_users_returns_created_users(client, valid_user):
    client.post("/users", json=valid_user)

    response = client.get("/users")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == valid_user["email"]

def test_get_existing_user(client, valid_user):
    created = client.post("/users", json=valid_user).json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created

def test_get_missing_user_returns_404(client):
    response = client.get("/users/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_delete_user_returns_no_content(client, valid_user):
    created = client.post("/users", json=valid_user).json()

    response = client.delete(f"/users/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/users/{created['id']}").status_code == 404

def test_duplicate_email_returns_409(client, valid_user):
    client.post("/users", json=valid_user)
    duplicate = {**valid_user, "name": "Different Name"}

    response = client.post("/users", json=duplicate)

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.parametrize(
    "payload",
    [
        {"name": "A"},  # Name too short
        {"name": "Asha Rao", "email": "asha@example.com"},  # Missing age
        {"name": "Asha Rao", "email": "x", "age": 30},  # Invalid email length
        {"name": "Asha Rao", "email": "asha@example.com", "age": 17},  # Age below minimum
        {"name": "Asha Rao", "email": "asha@example.com", "age": 121},  # Age above maximum
    ],
)
def test_invalid_user_payload_returns_422(client, payload):
    response = client.post("/users", json=payload)

    assert response.status_code == 422, (
        f"Expected 422 but got {response.status_code}: {response.text}"
    )
