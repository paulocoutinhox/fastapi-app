from unittest.mock import patch

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.my_model import MyModel
from services import my_model as service_my_model


@pytest.mark.asyncio
async def test_create_success(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)

    result = await service_my_model.create(obj, db)

    assert result is not None
    stmt = select(MyModel).where(MyModel.id == result)
    result_exec = await db.execute(stmt)
    obj_from_db = result_exec.scalar_one_or_none()
    assert obj_from_db is not None
    assert obj_from_db.field1 == "Test 1"
    assert obj_from_db.field2 == True


@pytest.mark.asyncio
async def test_create_failure(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = await service_my_model.create(obj, db)

    assert result is None
    stmt = select(MyModel).where(MyModel.field1 == "Test 1")
    result_exec = await db.execute(stmt)
    obj_from_db = result_exec.scalar_one_or_none()
    assert obj_from_db is None


@pytest.mark.asyncio
async def test_get_random_row_success(db: AsyncSession):
    obj1 = MyModel(field1="Test 1", field2=True)
    obj2 = MyModel(field1="Test 2", field2=False)
    await service_my_model.create(obj1, db)
    await service_my_model.create(obj2, db)

    result = await service_my_model.get_random_row(db)

    assert result is not None
    assert result.field1 in ["Test 1", "Test 2"]


@pytest.mark.asyncio
async def test_get_random_row_failure(db: AsyncSession):
    with patch.object(db, "execute", side_effect=Exception("DB Error")):
        result = await service_my_model.get_random_row(db)

    assert result is None


@pytest.mark.asyncio
async def test_update_success(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    update_obj = MyModel(field1="Updated Test 1", field2=False)
    result = await service_my_model.update(obj_id, update_obj, db)

    assert result is not None
    assert result.field1 == "Updated Test 1"
    assert result.field2 == False


@pytest.mark.asyncio
async def test_update_failure(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    update_obj = MyModel(field1="Updated Test 1", field2=False)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = await service_my_model.update(obj_id, update_obj, db)

    assert result is None


@pytest.mark.asyncio
async def test_delete_success(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    result = await service_my_model.delete(obj_id, db)

    assert result is True
    stmt = select(MyModel).where(MyModel.id == obj_id)
    result_exec = await db.execute(stmt)
    obj_from_db = result_exec.scalar_one_or_none()
    assert obj_from_db is None


@pytest.mark.asyncio
async def test_delete_failure(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    with patch.object(db, "commit", side_effect=Exception("DB Error")):
        result = await service_my_model.delete(obj_id, db)

    assert result is False
    stmt = select(MyModel).where(MyModel.id == obj_id)
    result_exec = await db.execute(stmt)
    obj_from_db = result_exec.scalar_one_or_none()
    assert obj_from_db is not None


@pytest.mark.asyncio
async def test_find_by_id_success(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    result = await service_my_model.find_by_id(obj_id, db)

    assert result is not None
    assert result.id == obj_id
    assert result.field1 == "Test 1"
    assert result.field2 == True


@pytest.mark.asyncio
async def test_find_by_id_failure(db: AsyncSession):
    result = await service_my_model.find_by_id(1, db)

    assert result is None


@pytest.mark.asyncio
async def test_delete_exception_handling(db: AsyncSession):
    obj = MyModel(field1="Test 1", field2=True)
    obj_id = await service_my_model.create(obj, db)

    with patch.object(db, "execute", side_effect=Exception("DB Error")):
        result = await service_my_model.delete(obj_id, db)

    assert result is False


@pytest.mark.asyncio
async def test_find_by_id_exception_handling(db: AsyncSession):
    with patch.object(db, "execute", side_effect=Exception("DB Error")):
        result = await service_my_model.find_by_id(1, db)

    assert result is None


@pytest.mark.asyncio
async def test_update_item_not_found(db: AsyncSession):
    update_obj = MyModel(field1="Updated Test 1", field2=False)

    result = await service_my_model.update(999, update_obj, db)

    assert result is None


@pytest.mark.asyncio
async def test_delete_item_not_found(db: AsyncSession):
    result = await service_my_model.delete(999, db)

    assert result is False
