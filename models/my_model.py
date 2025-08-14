from typing import Optional

from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Boolean, Column, DateTime, String
from sqlalchemy.dialects import mysql, postgresql, sqlite

from helpers.db import Base

BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(postgresql.BIGINT(), "postgresql")
BigIntegerType = BigIntegerType.with_variant(mysql.BIGINT(), "mysql")
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), "sqlite")


class MyModel(Base):
    __tablename__ = "my_model"

    id = Column(BigIntegerType, primary_key=True, autoincrement=True)
    field1 = Column(String(255))
    field2 = Column(Boolean())
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    def __init__(self, field1, field2=False, **kwargs):
        self.field1 = field1
        self.field2 = field2
        super().__init__(**kwargs)

    def to_dict(self):
        return {
            "id": self.id,
            "field1": self.field1,
            "field2": self.field2,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class MyModelRequest(BaseModel):
    field1: str
    field2: bool
