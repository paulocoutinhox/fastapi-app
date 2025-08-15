from fastapi import APIRouter, FastAPI, HTTPException

from helpers.db import AsyncSession
from models.my_model import MyModel, MyModelRequest, MyModelResponse
from services import my_model as service_my_model

router = APIRouter()


@router.post("/api/my-model/create")
async def my_model_create(request: MyModelRequest, db: AsyncSession):
    obj = MyModel(**request.model_dump())

    id = await service_my_model.create(obj, db)
    if id is None:
        raise HTTPException(status_code=400, detail="Failed to create MyModel")

    obj = await service_my_model.find_by_id(id, db)
    if obj is None:
        raise HTTPException(status_code=404, detail="MyModel not found after creation")

    return MyModelResponse(message="created", model=obj)


@router.get("/api/my-model/random")
async def my_model_random(db: AsyncSession):
    obj = await service_my_model.get_random_row(db)

    if obj is None:
        return {"message": "not-found"}

    return MyModelResponse(message="random", model=obj)


def setup(app: FastAPI):
    app.include_router(router)
