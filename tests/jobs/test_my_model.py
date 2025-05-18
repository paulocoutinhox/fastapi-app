from unittest.mock import patch

import pytest
from sqlalchemy.orm import Session

from helpers.scheduler import scheduler
from jobs import my_model
from models.my_model import MyModel


@pytest.fixture(autouse=True)
def run_around_tests():
    # setup: add job before test
    scheduler.add_job(my_model.job_create_my_model_list)
    yield
    # teardown: remove all jobs after tests
    scheduler.remove_all_jobs()


def test_job_create_my_model_list(db: Session):
    # patch db session to use the test database session
    with patch("helpers.db.SessionLocal", return_value=db):
        # execute job
        my_model.job_create_my_model_list()

        # verify the data was inserted
        obj_from_db = db.query(MyModel).filter_by(field1="Test Job").first()
        assert obj_from_db is not None
        assert obj_from_db.field1 == "Test Job"
        assert obj_from_db.field2 == False

        # verify output
        with patch("builtins.print") as mocked_print:
            my_model.job_create_my_model_list()
            print_arg = mocked_print.call_args[0][0]
            assert print_arg.startswith("Job Executed")
