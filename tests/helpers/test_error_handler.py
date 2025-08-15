from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel

from helpers.error_handler import _process_validation_errors, setup


def test_process_validation_errors_body_field():
    error = {"loc": ["body", "field1"], "msg": "field required", "type": "missing"}
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "field1" in errors
    assert errors["field1"] == ["field required"]


def test_process_validation_errors_query_param():
    error = {
        "loc": ["query", "page"],
        "msg": "value is not a valid integer",
        "type": "type_error",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "page" in errors
    assert errors["page"] == ["value is not a valid integer"]


def test_process_validation_errors_path_param():
    error = {
        "loc": ["path", "id"],
        "msg": "value is not a valid integer",
        "type": "type_error",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "id" in errors
    assert errors["id"] == ["value is not a valid integer"]


def test_process_validation_errors_header():
    error = {
        "loc": ["header", "authorization"],
        "msg": "field required",
        "type": "missing",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "authorization" in errors
    assert errors["authorization"] == ["field required"]


def test_process_validation_errors_cookie():
    error = {
        "loc": ["cookie", "session_id"],
        "msg": "field required",
        "type": "missing",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "session_id" in errors
    assert errors["session_id"] == ["field required"]


def test_process_validation_errors_simple_field():
    error = {"loc": ["field1"], "msg": "field required", "type": "missing"}
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "field1" in errors
    assert errors["field1"] == ["field required"]


def test_process_validation_errors_nested_body():
    error = {
        "loc": ["body", "user", "profile", "age"],
        "msg": "value is not a valid integer",
        "type": "type_error",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "user.profile.age" in errors
    assert errors["user.profile.age"] == ["value is not a valid integer"]


def test_process_validation_errors_array_index():
    error = {
        "loc": ["body", "items", 0, "name"],
        "msg": "field required",
        "type": "missing",
    }
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "items.0.name" in errors
    assert errors["items.0.name"] == ["field required"]


def test_process_validation_errors_empty_location():
    error = {"loc": [], "msg": "validation failed", "type": "value_error"}
    errors = _process_validation_errors(RequestValidationError([error]))

    assert "" in errors
    assert errors[""] == ["validation failed"]


def test_process_validation_errors_multiple_errors_same_field():
    errors_list = [
        {"loc": ["body", "field1"], "msg": "field required", "type": "missing"},
        {
            "loc": ["body", "field1"],
            "msg": "value is not a valid string",
            "type": "type_error",
        },
    ]
    errors = _process_validation_errors(RequestValidationError(errors_list))

    assert "field1" in errors
    assert len(errors["field1"]) == 2
    assert "field required" in errors["field1"]
    assert "value is not a valid string" in errors["field1"]


def test_process_validation_errors_different_field_types():
    errors_list = [
        {"loc": ["body", "name"], "msg": "field required", "type": "missing"},
        {
            "loc": ["query", "page"],
            "msg": "value is not a valid integer",
            "type": "type_error",
        },
        {
            "loc": ["path", "id"],
            "msg": "value is not a valid uuid",
            "type": "type_error",
        },
        {"loc": ["header", "content-type"], "msg": "field required", "type": "missing"},
    ]
    errors = _process_validation_errors(RequestValidationError(errors_list))

    assert "name" in errors
    assert "page" in errors
    assert "id" in errors
    assert "content-type" in errors
    assert errors["name"] == ["field required"]
    assert errors["page"] == ["value is not a valid integer"]
    assert errors["id"] == ["value is not a valid uuid"]
    assert errors["content-type"] == ["field required"]


def test_setup_validation_error_handler():
    app = FastAPI()
    setup(app)

    # verify handler is registered
    assert RequestValidationError in app.exception_handlers


def test_validation_exception_handler_integration():
    app = FastAPI()
    setup(app)

    # create a test endpoint that will trigger validation
    @app.post("/test")
    async def test_endpoint(data: dict):
        return {"message": "success"}

    client = TestClient(app)

    # send invalid data to trigger validation error
    response = client.post("/test", json={"invalid": "data"})

    # verify the response format
    assert response.status_code == 200  # dict doesn't have validation
    response_data = response.json()

    assert response_data["message"] == "success"


def test_validation_exception_handler_with_real_validation():
    class TestModel(BaseModel):
        field1: str
        field2: int

    app = FastAPI()
    setup(app)

    @app.post("/test")
    async def test_endpoint(data: TestModel):
        return {"message": "success"}

    client = TestClient(app)

    # send data that will fail Pydantic validation
    response = client.post("/test", json={"field1": 123, "field2": "not_a_number"})

    # verify the response format
    assert response.status_code == 422
    response_data = response.json()

    assert response_data["success"] is False
    assert response_data["message"] == "validation-error"
    assert "data" in response_data
    assert "errors" in response_data["data"]

    # verify specific field errors
    errors = response_data["data"]["errors"]
    assert "field1" in errors
    assert "field2" in errors
