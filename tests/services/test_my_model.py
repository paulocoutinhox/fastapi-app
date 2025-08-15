from unittest.mock import patch

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.my_model import MyModel
from services import my_model as service_my_model


def test_create_success(db: Session):
    obj = MyModel(field1="Test 1", field2=True)

    result = service_my_model.create(obj, db)

    assert result is not None
    stmt = select(MyModel).where(MyModel.id == result)
    obj_from_db = db.execute(stmt).scalar_one_or_none()
    assert obj_from_db is not None
    assert obj_from_db.field1 == "Test 1"
    assert obj_from_db.field2 == True


def test_create_failure(db: Session):
    obj = MyModel(field1="Test 1", field2=True)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = service_my_model.create(obj, db)

    assert result is None
    stmt = select(MyModel).where(MyModel.field1 == "Test 1")
    obj_from_db = db.execute(stmt).scalar_one_or_none()
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
    with patch.object(db, "execute", side_effect=Exception("DB Error")):
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
    stmt = select(MyModel).where(MyModel.id == obj_id)
    obj_from_db = db.execute(stmt).scalar_one_or_none()
    assert obj_from_db is None


def test_delete_failure(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = service_my_model.delete(obj_id, db)

    assert result is False
    stmt = select(MyModel).where(MyModel.id == obj_id)
    obj_from_db = db.execute(stmt).scalar_one_or_none()
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


def test_delete_exception_handling(db: Session):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = service_my_model.create(obj, db)

    with patch.object(db, "execute", side_effect=Exception("DB Error")):
        result = service_my_model.delete(obj_id, db)

    assert result is False


def test_find_by_id_exception_handling(db: Session):
    with patch.object(db, "execute", side_effect=Exception("DB Error")):
        result = service_my_model.find_by_id(1, db)

    assert result is None


def test_update_item_not_found(db: Session):
    update_obj = MyModel(field1="Updated Test 1", field2=False)

    result = service_my_model.update(999, update_obj, db)

    assert result is None


def test_delete_item_not_found(db: Session):
    result = service_my_model.delete(999, db)

    assert result is False
