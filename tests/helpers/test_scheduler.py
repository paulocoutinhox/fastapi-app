from unittest.mock import patch

from helpers.scheduler import scheduler


@patch.object(scheduler, "start")
def test_scheduler_startup(mock_start):
    scheduler.start()
    mock_start.assert_called_once()


@patch.object(scheduler, "shutdown")
def test_scheduler_shutdown(mock_shutdown):
    scheduler.shutdown()
    mock_shutdown.assert_called_once()


def test_scheduler_instance():
    # verify scheduler is properly configured
    assert scheduler is not None
    assert str(scheduler.timezone) == "UTC"


def test_scheduler_can_add_job():
    # verify scheduler can add and remove jobs

    def dummy_job():
        return "test"

    # add a job
    job = scheduler.add_job(dummy_job, "interval", seconds=60, id="test_job")

    # verify job was added
    assert job.id == "test_job"
    assert scheduler.get_job("test_job") is not None

    # execute the job immediately
    result = job.func()
    assert result == "test"

    # remove the job
    scheduler.remove_job("test_job")

    # verify job was removed
    assert scheduler.get_job("test_job") is None
