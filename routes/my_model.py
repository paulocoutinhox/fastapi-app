from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from helpers.db import get_db
from models.my_model import MyModel, MyModelRequest, MyModelResponse
from services import my_model as service_my_model

router = APIRouter()


@router.post("/api/my-model/create")
async def my_model_create(request: MyModelRequest, db: Session = Depends(get_db)):
    obj = MyModel(**request.model_dump())

    id = service_my_model.create(obj, db)
    if id is None:
        raise HTTPException(status_code=400, detail="Failed to create MyModel")

    obj = service_my_model.find_by_id(id, db)
    if obj is None:
        raise HTTPException(status_code=404, detail="MyModel not found after creation")

    response = MyModelResponse(message="created", model=obj.to_dict())

    return response


@router.post("/api/my-model/random")
async def my_model_random(db: Session = Depends(get_db)):
    obj = service_my_model.get_random_row(db)

    if obj is None:
        return {"message": "not-found"}

    response = MyModelResponse(message="random", model=obj.to_dict())

    return response


def setup(app: FastAPI):
    app.include_router(router)
