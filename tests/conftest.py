import pytest
from fastapi.testclient import TestClient
from app.main import app, reset_test_data

@pytest.fixture()
def client():
    # Isolate tests by resetting the in-memory store before each test.
    reset_test_data()
    with TestClient(app) as test_client:
        yield test_client
    reset_test_data()

@pytest.fixture()
def valid_user():
    return {"name": "Asha Rao", "email": "asha@example.com", "age": 30}
