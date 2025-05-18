from fastapi import FastAPI
from fastapi.testclient import TestClient

from helpers import cors


def test_no_cors(app: FastAPI, client: TestClient):
    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    response = client.get("/")
    assert "access-control-allow-origin" not in response.headers


def test_with_cors(app: FastAPI):
    app = FastAPI()
    cors.setup(app)
    client = TestClient(app)

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    response = client.get("/", headers={"Origin": "http://myhost.com"})
    assert response.headers.get("access-control-allow-origin") == "*"
