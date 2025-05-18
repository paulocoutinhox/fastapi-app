import logging
from unittest.mock import patch

from helpers import log


def test_log_setup():
    with patch("logging.basicConfig") as mock_basicConfig:
        log.setup()
        mock_basicConfig.assert_called_once_with(level=logging.ERROR)
