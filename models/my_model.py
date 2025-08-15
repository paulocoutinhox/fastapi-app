from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from helpers.db import Base


class MyModel(Base):
    __tablename__ = "my_model"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    field1: Mapped[str] = mapped_column(String(255), nullable=False)
    field2: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class MyModelRequest(BaseModel):
    field1: str
    field2: bool


class MyModelResponse(BaseModel):
    message: Optional[str] = None
    model: Optional[MyModel] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    @field_serializer("model")
    def serialize_model(self, model: Optional[MyModel]) -> Optional[dict]:
        if model is None:
            return None

        return {
            "id": model.id,
            "field1": model.field1,
            "field2": model.field2,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }
