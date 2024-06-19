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
