from fastapi.testclient import TestClient
from ..main import app
from ..models.user import User

client = TestClient(app)

User("ahmed")

def test_retrieve_user():
    response = client.get("/user/1")
    assert response.status_code == 200


def test_retrieve_nonexistent_user():
    response = client.get("/user/0")
    assert response.status_code == 404


def test_deposit():
    response = client.post("/deposit", json={"user_id": 1, "amount": 5000})
    assert response.status_code == 200


def test_deposit_invalid_amount():
    response = client.post("/deposit", json={"user_id": 1, "amount": 0})
    assert response.status_code == 422


def test_withdraw():
    response = client.post("/withdraw", json={"user_id": 1, "amount": 550})
    assert response.status_code == 200


def test_invalid_withdraw():
    response = client.post("/withdraw", json={"user_id": 1, "amount": 0})
    assert response.status_code == 422
