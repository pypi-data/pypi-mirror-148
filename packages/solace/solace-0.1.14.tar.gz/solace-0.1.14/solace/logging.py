import sys
from .env import *

from loguru import logger

handler = {
    "sink": sys.stderr,
    "level": LOG_LEVEL
}

if LOG_FILE is not None:
    handler["sink"] = LOG_FILE

if LOG_FORMAT is not None:
    handler["format"] = LOG_FORMAT

if LOG_TYPE == "json":
    handler["serialize"] = True

logger_config = {
    "handlers": [handler],
}

logger.configure(**logger_config)
