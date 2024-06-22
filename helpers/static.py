from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def setup(app: FastAPI):
    app.mount("/", StaticFiles(directory="public", html=True), name="public")
