from unittest.mock import patch

import pytest
from fastapi import FastAPI

from helpers.lifespan import lifespan
from helpers.scheduler import scheduler


@pytest.mark.asyncio
@patch.object(scheduler, "shutdown")
@patch.object(scheduler, "start")
async def test_lifespan(mock_start, mock_shutdown):
    # verify lifespan starts and stops scheduler
    app = FastAPI()

    async with lifespan(app):
        mock_start.assert_called_once()

    mock_shutdown.assert_called_once()
