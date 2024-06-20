from unittest.mock import patch

from fastapi.testclient import TestClient

from models.my_model import MyModelRequest


def test_my_model_create(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)
    response = client.post("/api/my-model/create", json=request.model_dump())
    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert data["model"]["field1"] == "Test 1"
    assert data["model"]["field2"] == True


def test_my_model_random(client: TestClient):
    # create a registry
    request = MyModelRequest(field1="Test 1", field2=True)
    response = client.post("/api/my-model/create", json=request.model_dump())
    assert response.status_code == 200

    # get random
    response = client.post("/api/my-model/random")
    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert data["model"]["field1"] == "Test 1"
    assert data["model"]["field2"] == True


def test_my_model_create_fail_create(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=None):
        response = client.post("/api/my-model/create", json=request.model_dump())
        assert response.status_code == 400
        assert response.json() == {"detail": "Failed to create MyModel"}


def test_my_model_create_fail_find_by_id(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=1), patch(
        "services.my_model.find_by_id", return_value=None
    ):
        response = client.post("/api/my-model/create", json=request.model_dump())
        assert response.status_code == 404
        assert response.json() == {"detail": "MyModel not found after creation"}
