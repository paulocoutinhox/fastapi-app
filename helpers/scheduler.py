from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler

jobstores = {
    "default": MemoryJobStore(),
}

scheduler = AsyncIOScheduler(
    jobstores=jobstores,
    timezone="UTC",
)
