from helpers.scheduler import scheduler
from models.my_model import MyModel
from services import my_model as service_my_model


@scheduler.scheduled_job("cron", hour=0, minute=1)
async def job_create_my_model():
    # Import here to avoid circular imports and allow proper testing
    from helpers.db import AsyncSessionLocal

    async with AsyncSessionLocal() as session:
        data = {"field1": "Test Job", "field2": False}
        obj = MyModel(**data)
        id = await service_my_model.create(obj, session)
        print(f"Job Executed: {id}")
        return id
