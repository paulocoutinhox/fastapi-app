from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

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
        l.error(f"[my model : create] ${e}")
        db.rollback()
        return None


def get_random_row(db: Session):
    try:
        random_row = db.query(MyModel).order_by(func.random()).first()
        return random_row
    except Exception as e:
        l.error(f"[my model : get random row] ${e}")
        return None


def update(id, obj: MyModel, db: Session):
    try:
        item = db.query(MyModel).filter(MyModel.id == id).one()
        item.field1 = obj.field1
        item.field2 = obj.field2
        item.updated_at = datetime.now()
        db.commit()
        return item
    except Exception as e:
        l.error(f"[my model : update] ${e}")
        db.rollback()
    return None


def delete(id, db: Session):
    try:
        item = db.query(MyModel).filter(MyModel.id == id).one()
        db.delete(item)
        db.commit()
        return True
    except Exception as e:
        l.error(f"[my model : delete] ${e}")
        db.rollback()
        return False


def find_by_id(id, db: Session):
    try:
        item = db.query(MyModel).filter(MyModel.id == id).one()
        return item
    except Exception as e:
        l.error(f"[my model : find by id] ${e}")
        return None
