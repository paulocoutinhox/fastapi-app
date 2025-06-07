from contextlib import asynccontextmanager

from fastapi import FastAPI

from .scheduler import scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    scheduler.start()

    yield

    # shutdown
    scheduler.shutdown()
