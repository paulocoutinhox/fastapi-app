from unittest.mock import patch

import pytest
from fastapi import FastAPI

from helpers.scheduler import scheduler, setup, shutdown_event, startup_event


def test_scheduler_startup_event():
    with patch.object(scheduler, "start", return_value=None) as mock_start:
        scheduler.start()
        mock_start.assert_called_once()


def test_scheduler_shutdown_event():
    with patch.object(scheduler, "shutdown", return_value=None) as mock_shutdown:
        scheduler.shutdown()
        mock_shutdown.assert_called_once()


def test_setup(app: FastAPI):
    with patch.object(
        app, "add_event_handler", wraps=app.add_event_handler
    ) as mock_add_event_handler:
        setup(app)

        mock_add_event_handler.assert_any_call("startup", startup_event)
        mock_add_event_handler.assert_any_call("shutdown", shutdown_event)


@pytest.mark.asyncio
async def test_scheduler_startup_and_shutdown(app: FastAPI):
    with patch.object(
        scheduler, "start", return_value=None
    ) as mock_start, patch.object(
        scheduler, "shutdown", return_value=None
    ) as mock_shutdown:
        setup(app)

        await startup_event()
        await shutdown_event()

        mock_start.assert_called_once()
        mock_shutdown.assert_called_once()
