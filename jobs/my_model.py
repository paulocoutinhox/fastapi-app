from helpers import db
from helpers.scheduler import scheduler
from models.my_model import MyModel
from services import my_model as service_my_model


@scheduler.scheduled_job("cron", hour=6, minute=0)
def job_create_my_model_list():
    data = {"field1": "Test Job"}
    obj = MyModel(**data)
    id = service_my_model.create(obj, db.SessionLocal())
    print(f"Job Executed: {id}")
