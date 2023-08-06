from .env import *
# from .importer import import_from_string
# from .logging import logger
from .context import Context
from starlette.types import Scope, Send, Receive
# from starlette.requests import Request
# from starlette.routing import Router
from typing import Callable

# NOTE: ASGI applications should be a single async callable:

class Solace:
    """ Creates a Solace application instance. """

    def __init__(self,
        debug: bool = False,
    ):
        self.debug = debug
        self.stack = []
        self.routes = []

    def use(self, middleware: Callable):
        """ adds middlware handlers to the application stack """
        # TODO: check type of handler
        # if not proper type, we can throw an error
        self.stack.append(middleware)

    async def _stack(self, ctx: Context) -> Context:
        for middleware in self.stack:
            ctx = middleware(ctx)
        return ctx

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        scope["app"] = self
        ctx = Context(scope, receive, send)
        ctx = await self._stack(ctx)
        await ctx._final_response(scope, receive, send)
