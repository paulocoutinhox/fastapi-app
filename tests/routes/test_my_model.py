from unittest.mock import patch

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from models.my_model import MyModelRequest
from routes.my_model import setup


@pytest.mark.asyncio
async def test_my_model_create(async_client: AsyncClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    response = await async_client.post(
        "/api/my-model/create", json=request.model_dump()
    )

    assert response.status_code == 200

    data = response.json()
    assert "model" in data
    assert data["model"]["field1"] == "Test 1"
    assert data["model"]["field2"] == True
    assert data["message"] == "created"


@pytest.mark.asyncio
async def test_my_model_random(async_client: AsyncClient):
    # create a registry
    request = MyModelRequest(field1="Test 1", field2=True)
    response = await async_client.post(
        "/api/my-model/create", json=request.model_dump()
    )
    assert response.status_code == 200

    # get random
    response = await async_client.get("/api/my-model/random")
    assert response.status_code == 200
    data = response.json()
    assert "model" in data
    assert data["model"]["field1"] == "Test 1"
    assert data["model"]["field2"] == True
    assert data["message"] == "random"


@pytest.mark.asyncio
async def test_my_model_create_fail_create(async_client: AsyncClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=None):
        response = await async_client.post(
            "/api/my-model/create", json=request.model_dump()
        )
        assert response.status_code == 400
        assert response.json() == {"detail": "Failed to create MyModel"}


@pytest.mark.asyncio
async def test_my_model_create_fail_find_by_id(async_client: AsyncClient):
    request = MyModelRequest(field1="Test 1", field2=True)

    with patch("services.my_model.create", return_value=1), patch(
        "services.my_model.find_by_id", return_value=None
    ):
        response = await async_client.post(
            "/api/my-model/create", json=request.model_dump()
        )
        assert response.status_code == 404
        assert response.json() == {"detail": "MyModel not found after creation"}


@pytest.mark.asyncio
async def test_my_model_random_not_found(async_client: AsyncClient):
    with patch("services.my_model.get_random_row", return_value=None):
        response = await async_client.get("/api/my-model/random")
        assert response.status_code == 200
        data = response.json()
        assert data == {"message": "not-found"}


@pytest.mark.asyncio
async def test_setup_function():
    app = FastAPI()

    setup(app)

    assert len(app.routes) > 0

    my_model_routes = [
        route
        for route in app.routes
        if hasattr(route, "path") and "/api/my-model" in str(route.path)
    ]

    assert len(my_model_routes) > 0
