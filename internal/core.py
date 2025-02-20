import logging
import sys
from typing import Generic, TypeVar


TIMESTAMP_FORMAT='%Y-%m-%dT%H:%M:%S.%f'
T = TypeVar(Generic())

def config_stdout_logger(logger, level):
    """ Takes an already created logger and configures it with the format for each line and the output stream that it will use (stdout)"""

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger