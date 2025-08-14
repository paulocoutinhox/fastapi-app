import json

from fastapi import Response
from pydantic import BaseModel, Field, ValidationError

from models.web_response import WebResponse


class SamplePydanticModel(BaseModel):
    """Test model for WebResponse testing"""

    id: int
    name: str
    active: bool = True


class SampleORMModel:
    """Test ORM model with to_dict method"""

    def __init__(self, id: int, name: str, active: bool = True):
        self.id = id
        self.name = name
        self.active = active

    def to_dict(self):
        return {"id": self.id, "name": self.name, "active": self.active}


class SampleRegularObject:
    """Test regular object with __dict__"""

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


def test_web_response_success_response():
    response = WebResponse.s("test-success")
    assert response.response.success is True
    assert response.response.message == "test-success"
    assert response.response.data is None


def test_web_response_error_response():
    response = WebResponse.e("test-error")
    assert response.response.success is False
    assert response.response.message == "test-error"
    assert response.response.data is None


def test_web_response_with_data_dict():
    data = {"key": "value", "number": 123}
    response = WebResponse.s("test-with-data", data)
    assert response.response.success is True
    assert response.response.message == "test-with-data"
    assert response.response.data == data


def test_web_response_with_pydantic_model():
    model = SamplePydanticModel(id=1, name="Test User")
    response = WebResponse.s("test-with-model", model)
    assert response.response.success is True
    assert response.response.data["id"] == 1
    assert response.response.data["name"] == "Test User"


def test_web_response_with_orm_model():
    model = SampleORMModel(id=2, name="ORM User")
    response = WebResponse.s("test-with-orm", model)
    assert response.response.success is True
    assert response.response.data["id"] == 2
    assert response.response.data["name"] == "ORM User"


def test_web_response_with_regular_object():
    obj = SampleRegularObject(id=3, name="Regular User")
    response = WebResponse.s("test-with-object", obj)
    assert response.response.success is True
    assert response.response.data["id"] == 3
    assert response.response.data["name"] == "Regular User"


def test_web_response_with_single_value():
    response = WebResponse.s("test-with-value", "simple-string")
    assert response.response.success is True
    assert response.response.data["value"] == "simple-string"


def test_web_response_with_errors():
    errors = {"email": ["Invalid email format"], "name": ["Name is required"]}
    response = WebResponse.e("validation-failed", errors=errors)
    assert response.response.success is False
    assert response.response.message == "validation-failed"
    assert response.response.data["errors"] == errors


def test_web_response_status_codes():
    response = WebResponse.s("test")
    assert response.r200().status_code == 200
    assert response.r201().status_code == 201
    assert response.r400().status_code == 400
    assert response.r401().status_code == 401
    assert response.r403().status_code == 403
    assert response.r404().status_code == 404
    assert response.r409().status_code == 409
    assert response.r422().status_code == 422
    assert response.r500().status_code == 500
    assert response.r503().status_code == 503
    assert response.r(202).status_code == 202


def test_web_response_json_structure():
    data = {"user_id": 123, "username": "testuser"}
    response = WebResponse.s("user-created", data)
    http_response = response.r201()
    content = json.loads(http_response.body.decode())
    assert content["success"] is True
    assert content["message"] == "user-created"
    assert content["data"]["user_id"] == 123
    assert http_response.media_type == "application/json"


def test_web_response_error_json_structure():
    errors = {"field": ["Error message"]}
    response = WebResponse.e("validation-error", errors=errors)
    http_response = response.r422()
    content = json.loads(http_response.body.decode())
    assert content["success"] is False
    assert content["message"] == "validation-error"
    assert content["data"]["errors"]["field"] == ["Error message"]


def test_web_response_add_data_method():
    response = WebResponse.s("test")
    response.response.add_data("key1", "value1")
    response.response.add_data("key2", "value2")
    assert response.response.data["key1"] == "value1"
    assert response.response.data["key2"] == "value2"


def test_web_response_add_error_method():
    response = WebResponse.e("test")
    response.response.add_error("email", "Invalid email")
    response.response.add_error("email", "Email already exists")
    response.response.add_error("name", "Name is required")
    assert response.response.data["errors"]["email"] == [
        "Invalid email",
        "Email already exists",
    ]
    assert response.response.data["errors"]["name"] == ["Name is required"]


def test_web_response_create_method():
    response = WebResponse.create(True, "test-message", {"key": "value"})
    assert response.response.success is True
    assert response.response.message == "test-message"
    assert response.response.data["key"] == "value"


def test_web_response_create_with_errors():
    errors = {"field": ["Error"]}
    response = WebResponse.create(False, "test-error", errors=errors)
    assert response.response.success is False
    assert response.response.message == "test-error"
    assert response.response.data["errors"] == errors


def test_web_response_automatic_pydantic_error_processing():
    class UserModel(BaseModel):
        email: str = Field(pattern=r"^[^@]+@[^@]+\.[^@]+$")
        age: int = Field(ge=0, le=150)
        name: str = Field(min_length=2)

    try:
        UserModel(email="invalid-email", age=200, name="a")
    except ValidationError as e:
        response = WebResponse.e("validation-failed", verror=e)
        assert response.response.success is False
        assert response.response.message == "validation-failed"
        assert "errors" in response.response.data

        field_errors = response.response.data["errors"]
        assert "email" in field_errors
        assert "age" in field_errors
        assert "name" in field_errors


def test_web_response_automatic_pydantic_error_with_additional_data():
    class ProductModel(BaseModel):
        name: str = Field(min_length=3)
        price: float = Field(gt=0)

    try:
        ProductModel(name="ab", price=-5)
    except ValidationError as e:
        additional_data = {"request_id": "12345", "timestamp": "2024-01-01"}
        response = WebResponse.e(
            "product-validation-failed", data=additional_data, verror=e
        )
        assert response.response.success is False
        assert "errors" in response.response.data
        assert "request_id" in response.response.data
        assert "timestamp" in response.response.data

        field_errors = response.response.data["errors"]
        assert "name" in field_errors
        assert "price" in field_errors


def test_web_response_automatic_pydantic_error_with_manual_errors():
    class OrderModel(BaseModel):
        quantity: int = Field(gt=0)
        customer_id: int = Field(gt=0)

    try:
        OrderModel(quantity=0, customer_id=-1)
    except ValidationError as e:
        manual_errors = {"payment": ["Payment method not supported"]}
        response = WebResponse.e(
            "order-validation-failed", errors=manual_errors, verror=e
        )
        assert response.response.success is False
        assert "errors" in response.response.data

        field_errors = response.response.data["errors"]
        assert "quantity" in field_errors
        assert "customer_id" in field_errors
        assert "payment" in field_errors
        assert "Payment method not supported" in field_errors["payment"]
