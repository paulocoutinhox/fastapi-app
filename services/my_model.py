from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.log import logging as l
from models.my_model import MyModel


async def create(obj: MyModel, db: AsyncSession) -> Optional[int]:
    obj.created_at = datetime.now()
    try:
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj.id
    except Exception as e:
        l.error(f"[my model : create] {e}")
        await db.rollback()
        return None


async def get_random_row(db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).order_by(MyModel.id.desc()).limit(1)
        result = await db.execute(stmt)
        random_row = result.scalar_one_or_none()
        return random_row
    except Exception as e:
        l.error(f"[my model : get random row] {e}")
        return None


async def update(id: int, obj: MyModel, db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            item.field1 = obj.field1
            item.field2 = obj.field2
            item.updated_at = datetime.now()
            await db.commit()
            await db.refresh(item)
            return item
        return None
    except Exception as e:
        l.error(f"[my model : update] {e}")
        await db.rollback()
        return None


async def delete(id: int, db: AsyncSession) -> bool:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        if item:
            await db.delete(item)
            await db.commit()
            return True
        return False
    except Exception as e:
        l.error(f"[my model : delete] {e}")
        await db.rollback()
        return False


async def find_by_id(id: int, db: AsyncSession) -> Optional[MyModel]:
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        result = await db.execute(stmt)
        item = result.scalar_one_or_none()
        return item
    except Exception as e:
        l.error(f"[my model : find by id] {e}")
        return None
