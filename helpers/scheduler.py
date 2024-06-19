from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

executors = {
    "default": ThreadPoolExecutor(10),
}

jobstores = {
    "default": MemoryJobStore(),
}

scheduler = AsyncIOScheduler(
    executors=executors,
    jobstores=jobstores,
    timezone="America/Sao_Paulo",
)


async def startup_event():
    scheduler.start()


async def shutdown_event():
    scheduler.shutdown()


def setup(app: FastAPI):
    app.add_event_handler("startup", startup_event)
    app.add_event_handler("shutdown", shutdown_event)
