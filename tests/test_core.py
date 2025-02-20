import pytest
import logging

from internal.core import config_stdout_logger


@pytest.mark.parametrize('level', [
    logging.INFO,
    logging.DEBUG
])
def test_logger_configurator(level):
    logger = logging.getLogger("test")

    config_stdout_logger(logger, level)

    assert logger.level == level