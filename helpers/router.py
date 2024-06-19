from fastapi import FastAPI

from routes.my_model import router as router_my_model


def setup(app: FastAPI):
    app.include_router(router_my_model)
