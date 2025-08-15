from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.scheduler import scheduler
from jobs import my_model


@pytest.fixture(autouse=True)
def run_around_tests():
    scheduler.add_job(my_model.job_create_my_model)
    yield
    scheduler.remove_all_jobs()


@pytest.mark.asyncio
async def test_job_create_my_model(db: AsyncSession):
    with patch("services.my_model.create", return_value=1) as mock_create:
        result = await my_model.job_create_my_model()
        assert result == 1
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args[0][0].field1 == "Test Job"
        assert call_args[0][0].field2 == False

    with patch("services.my_model.create", return_value=1) as mock_create:
        with patch("builtins.print") as mocked_print:
            await my_model.job_create_my_model()
            print_arg = mocked_print.call_args[0][0]
            assert print_arg.startswith("Job Executed")
