from unittest.mock import patch

from fastapi.testclient import TestClient

from models.my_model import MyModelRequest


def test_my_model_create(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)
    response = client.post("/api/my-model/create", json=request.model_dump())
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "created"

    # check if the model data is in the response
    model_data = data.get("data", data)
    assert "field1" in model_data
    assert model_data["field1"] == "Test 1"
    assert model_data["field2"] is True


def test_my_model_random(client: TestClient):
    # create a registry
    request = MyModelRequest(field1="Test 1", field2=True)
    response = client.post("/api/my-model/create", json=request.model_dump())
    assert response.status_code == 201

    # get random
    response = client.get("/api/my-model/random")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "random"

    # check if the model data is in the response
    model_data = data.get("data", data)
    assert "field1" in model_data
    assert model_data["field1"] == "Test 1"
    assert model_data["field2"] is True


def test_my_model_create_fail_create(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=None):
        response = client.post("/api/my-model/create", json=request.model_dump())
        assert response.status_code == 400
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "create-failed"


def test_my_model_create_fail_find_by_id(client: TestClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=1), patch(
        "services.my_model.find_by_id", return_value=None
    ):
        response = client.post("/api/my-model/create", json=request.model_dump())
        assert response.status_code == 404

        # check if the response is a json
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "not-found"


def test_my_model_random_not_found(client: TestClient):
    with patch("services.my_model.get_random_row", return_value=None):
        response = client.get("/api/my-model/random")
        assert response.status_code == 404

        # check if the response is a json
        data = response.json()
        assert data["success"] is False
        assert data["message"] == "not-found"
