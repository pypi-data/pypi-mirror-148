""" A Logging Plugin for Solace (powered by Loguru) """

from solace.context import Context
from loguru import logger
import sys

async def logging(ctx: Context):
    """ provides logging support via Loguru to the Context object """
    ctx.trace("start of logging plugin")
    handler = {
        "sink": ctx.config.get('LOG_SINK', sys.stderr),
        "level": ctx.config.get('LOG_LEVEL', "INFO").upper()
    }
    if ctx.config.get('LOG_FORMAT', None):
        handler["format"] = ctx.config.get('LOG_FORMAT')
    if ctx.config.get('LOG_TYPE', 'text') == 'json':
        handler["serialize"] = True
    logger.configure(handlers = [handler])
    ctx.logger = logger
    ctx.trace("end of logging plugin")
    return ctx
