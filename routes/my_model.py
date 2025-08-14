from fastapi import APIRouter, Depends, FastAPI
from sqlalchemy.orm import Session

from helpers.db import get_db
from models.my_model import MyModel, MyModelRequest
from models.web_response import WebResponse
from services import my_model as service_my_model

router = APIRouter()


@router.post("/api/my-model/create")
async def my_model_create(request: MyModelRequest, db: Session = Depends(get_db)):
    obj = MyModel(**request.model_dump())

    id = service_my_model.create(obj, db)
    if id is None:
        return WebResponse.e("create-failed").r400()

    obj = service_my_model.find_by_id(id, db)
    if obj is None:
        return WebResponse.e("not-found").r404()

    return WebResponse.s("created", obj).r201()


@router.get("/api/my-model/random")
async def my_model_random(db: Session = Depends(get_db)):
    obj = service_my_model.get_random_row(db)

    if obj is None:
        return WebResponse.e("not-found").r404()

    return WebResponse.s("random", obj).r200()


def setup(app: FastAPI):
    app.include_router(router)
