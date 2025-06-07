from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

executors = {
    "default": ThreadPoolExecutor(10),
}

jobstores = {
    "default": MemoryJobStore(),
}

scheduler = AsyncIOScheduler(
    executors=executors,
    jobstores=jobstores,
    timezone="UTC",
)
