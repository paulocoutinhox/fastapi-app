from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from helpers.log import logging as l
from models.my_model import MyModel


def create(obj: MyModel, db: Session):
    obj.created_at = datetime.now()
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj.id
    except Exception as e:
        l.error(f"[my model : create] {e}")
        db.rollback()
        return None


def get_random_row(db: Session):
    try:
        stmt = select(MyModel).order_by(MyModel.id.desc()).limit(1)
        random_row = db.execute(stmt).scalar_one_or_none()
        return random_row
    except Exception as e:
        l.error(f"[my model : get random row] {e}")
        return None


def update(id, obj: MyModel, db: Session):
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        item = db.execute(stmt).scalar_one_or_none()
        if item:
            item.field1 = obj.field1
            item.field2 = obj.field2
            item.updated_at = datetime.now()
            db.commit()
            return item
        return None
    except Exception as e:
        l.error(f"[my model : update] {e}")
        db.rollback()
    return None


def delete(id, db: Session):
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        item = db.execute(stmt).scalar_one_or_none()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False
    except Exception as e:
        l.error(f"[my model : delete] {e}")
        db.rollback()
        return False


def find_by_id(id, db: Session):
    try:
        stmt = select(MyModel).where(MyModel.id == id)
        item = db.execute(stmt).scalar_one_or_none()
        return item
    except Exception as e:
        l.error(f"[my model : find by id] {e}")
        return None
