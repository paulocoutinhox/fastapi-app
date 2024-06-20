from unittest.mock import patch

from sqlalchemy.orm import Session

from models.my_model import MyModel
from services import my_model as service_my_model


def test_create_success(db: Session):
    obj = MyModel(field1="Test 1", field2=True)

    result = service_my_model.create(obj, db)

    assert result is not None
    obj_from_db = db.query(MyModel).filter_by(id=result).first()
    assert obj_from_db is not None
    assert obj_from_db.field1 == "Test 1"
    assert obj_from_db.field2 == True


def test_create_failure(db: Session):
    obj = MyModel(field1="Test 1", field2=True)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = service_my_model.create(obj, db)

    assert result is None
    obj_from_db = db.query(MyModel).filter_by(field1="Test 1").first()
    assert obj_from_db is None


def test_get_random_row_success(db: Session):
    obj1 = MyModel(field1="Test 1", field2=True)
    obj2 = MyModel(field1="Test 2", field2=False)
    service_my_model.create(obj1, db)
    service_my_model.create(obj2, db)

    result = service_my_model.get_random_row(db)

    assert result is not None
    assert result.field1 in ["Test 1", "Test 2"]


def test_get_random_row_failure(db: Session):
    with patch.object(db, "query", side_effect=Exception("DB Error")):
        result = service_my_model.get_random_row(db)

    assert result is None


def test_update_success(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    update_obj = MyModel(field1="Updated Test 1", field2=False)
    result = service_my_model.update(obj_id, update_obj, db)

    assert result is not None
    assert result.field1 == "Updated Test 1"
    assert result.field2 == False


def test_update_failure(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    update_obj = MyModel(field1="Updated Test 1", field2=False)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = service_my_model.update(obj_id, update_obj, db)

    assert result is None


def test_delete_success(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    result = service_my_model.delete(obj_id, db)

    assert result is True
    obj_from_db = db.query(MyModel).filter_by(id=obj_id).first()
    assert obj_from_db is None


def test_delete_failure(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = service_my_model.delete(obj_id, db)

    assert result is False
    obj_from_db = db.query(MyModel).filter_by(id=obj_id).first()
    assert obj_from_db is not None


def test_find_by_id_success(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    result = service_my_model.find_by_id(obj_id, db)

    assert result is not None
    assert result.id == obj_id
    assert result.field1 == "Test 1"
    assert result.field2 == True


def test_find_by_id_failure(db: Session):
    result = service_my_model.find_by_id(1, db)

    assert result is None
