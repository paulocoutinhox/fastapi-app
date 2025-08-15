from datetime import datetime

from models.my_model import MyModel, MyModelRequest, MyModelResponse


def test_my_model_creation():
    obj = MyModel(field1="Test 1", field2=True)

    assert obj.field1 == "Test 1"
    assert obj.field2 == True
    assert obj.id is None


def test_my_model_response_serialize_model_with_none():
    response = MyModelResponse(message="Test message", model=None)

    serialized_data = response.model_dump()

    assert serialized_data["message"] == "Test message"
    assert serialized_data["model"] is None


def test_my_model_response_serialize_model_with_valid_model():
    mock_model = MyModel(field1="Test Field 1", field2=False)

    mock_model.id = 1
    mock_model.created_at = datetime(2023, 1, 1, 12, 0, 0)
    mock_model.updated_at = datetime(2023, 1, 1, 12, 0, 0)

    response = MyModelResponse(message="Test message", model=mock_model)

    serialized_data = response.model_dump()

    assert serialized_data["message"] == "Test message"
    assert serialized_data["model"] is not None
    assert serialized_data["model"]["id"] == 1
    assert serialized_data["model"]["field1"] == "Test Field 1"
    assert serialized_data["model"]["field2"] == False
    assert serialized_data["model"]["created_at"] == datetime(2023, 1, 1, 12, 0, 0)
    assert serialized_data["model"]["updated_at"] == datetime(2023, 1, 1, 12, 0, 0)


def test_my_model_request_validation():
    request = MyModelRequest(field1="Test Field", field2=True)

    assert request.field1 == "Test Field"
    assert request.field2 == True

    data = request.model_dump()
    assert data["field1"] == "Test Field"
    assert data["field2"] == True
