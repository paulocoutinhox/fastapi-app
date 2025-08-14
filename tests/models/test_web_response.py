from fastapi import Response
from pydantic import BaseModel

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
    assert response.response.message == "test-with-model"
    assert response.response.data["id"] == 1
    assert response.response.data["name"] == "Test User"
    assert response.response.data["active"] is True


def test_web_response_with_orm_model():
    model = SampleORMModel(id=2, name="ORM User")
    response = WebResponse.s("test-with-orm", model)

    assert response.response.success is True
    assert response.response.message == "test-with-orm"
    assert response.response.data["id"] == 2
    assert response.response.data["name"] == "ORM User"
    assert response.response.data["active"] is True


def test_web_response_with_regular_object():
    obj = SampleRegularObject(id=3, name="Regular User")
    response = WebResponse.s("test-with-object", obj)

    assert response.response.success is True
    assert response.response.message == "test-with-object"
    assert response.response.data["id"] == 3
    assert response.response.data["name"] == "Regular User"


def test_web_response_with_single_value():
    response = WebResponse.s("test-with-value", "simple-string")

    assert response.response.success is True
    assert response.response.message == "test-with-value"
    assert response.response.data["value"] == "simple-string"


def test_web_response_with_errors():
    errors = {"email": ["Invalid email format"], "name": ["Name is required"]}
    response = WebResponse.e("validation-failed", errors=errors)

    assert response.response.success is False
    assert response.response.message == "validation-failed"
    assert response.response.data["errors"] == errors


def test_web_response_status_codes():
    response = WebResponse.s("test")

    # Test specific status codes
    assert isinstance(response.r200(), Response)
    assert isinstance(response.r201(), Response)
    assert isinstance(response.r400(), Response)
    assert isinstance(response.r401(), Response)
    assert isinstance(response.r403(), Response)
    assert isinstance(response.r404(), Response)
    assert isinstance(response.r409(), Response)
    assert isinstance(response.r422(), Response)
    assert isinstance(response.r500(), Response)
    assert isinstance(response.r503(), Response)

    # Test generic method
    assert isinstance(response.r(202), Response)
    assert isinstance(response.r(429), Response)


def test_web_response_status_code_values():
    response = WebResponse.s("test")

    # Test specific status codes
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

    # Test generic method
    assert response.r(202).status_code == 202
    assert response.r(429).status_code == 429


def test_web_response_json_structure():
    data = {"user_id": 123, "username": "testuser"}
    response = WebResponse.s("user-created", data)

    # Get the response object
    http_response = response.r201()

    # Parse JSON content
    import json

    content = json.loads(http_response.body.decode())

    assert content["success"] is True
    assert content["message"] == "user-created"
    assert content["data"]["user_id"] == 123
    assert content["data"]["username"] == "testuser"


def test_web_response_error_json_structure():
    errors = {"field": ["Error message"]}
    response = WebResponse.e("validation-error", errors=errors)

    # Get the response object
    http_response = response.r422()

    # Parse JSON content
    import json

    content = json.loads(http_response.body.decode())

    assert content["success"] is False
    assert content["message"] == "validation-error"
    assert content["data"]["errors"]["field"] == ["Error message"]


def test_web_response_media_type():
    response = WebResponse.s("test")
    http_response = response.r200()

    assert http_response.media_type == "application/json"


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


def test_web_response_empty_data():
    response = WebResponse.s("test")

    assert response.response.success is True
    assert response.response.message == "test"
    assert response.response.data is None


def test_web_response_complex_data():
    complex_data = {
        "users": [{"id": 1, "name": "User 1"}, {"id": 2, "name": "User 2"}],
        "total": 2,
        "metadata": {"page": 1, "per_page": 10},
    }

    response = WebResponse.s("users-retrieved", complex_data)

    assert response.response.success is True
    assert response.response.message == "users-retrieved"
    assert response.response.data["users"][0]["id"] == 1
    assert response.response.data["total"] == 2
    assert response.response.data["metadata"]["page"] == 1
