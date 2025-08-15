from unittest.mock import AsyncMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from helpers.db import get_session


@pytest.mark.asyncio
async def test_get_session_error_handling():
    mock_session = AsyncMock()
    mock_session.rollback = AsyncMock()

    with patch("helpers.db.AsyncSessionLocal") as mock_session_local:
        mock_session_local.return_value.__aenter__.return_value = mock_session
        mock_session_local.return_value.__aexit__.return_value = None

        session_gen = get_session()
        await session_gen.__anext__()

        with pytest.raises(SQLAlchemyError) as exc_info:
            await session_gen.athrow(SQLAlchemyError("Test error"))

        assert str(exc_info.value) == "Test error"

        mock_session.rollback.assert_called_once()
