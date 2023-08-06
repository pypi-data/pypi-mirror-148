""" 
SolaceFlow is an ASGI Application that provides
the ability to create composable "flows" that
share a common context object. Solace is heavily
inspired by the Koa.js framework, found here
https://koajs.com/

The reason for creating this is to enable what
I like to think of as "truly reusable code"
so that a developer can create flows made up of
generic functions and then compose those flows
into their applications to suit their needs.
"""

from .env import *
from .context import Context, ContextualHTTPException
import sys
import json
from starlette.types import Scope, Send, Receive, ASGIApp
from boltons.tbutils import ExceptionInfo
from starlette.routing import iscoroutinefunction_or_partial
from starlette.responses import *
from .templating import _TemplateResponse

VALID_RESPONSE_TYPES = (
    Response, 
    JSONResponse, 
    StreamingResponse, 
    PlainTextResponse,
    _TemplateResponse,
    HTMLResponse,
    RedirectResponse,
    FileResponse
)

class SolaceFlow:
    """ Creates a SolaceFlow application instance. """

    def __init__(self):
        self.stack = []

    async def _stack(self, ctx: Context) -> ASGIApp:
        try:
            for handler in self.stack:
                if iscoroutinefunction_or_partial(handler):
                    rv = await handler(ctx)
                else:
                    rv = handler(ctx)
                
                # # we have a return value...
                if rv is not None:
                    # NOTE: if we have a context object,
                    # then we need to update it before
                    # going into the next flow handler.
                    if isinstance(rv, Context):
                        ctx = rv
                    
                    # if the return value is a valid Response type,
                    # then we will immediately return, stopping any
                    # futher handlers in the flow from executing.
                    elif issubclass(type(rv), VALID_RESPONSE_TYPES):
                        return rv

        except ContextualHTTPException as e:
            exception_info = ExceptionInfo.from_exc_info(*sys.exc_info())
            ctx.code = 500
            ctx.body = "Internal Server Error"
            if HTTP_EXCEPTION_TYPE == "json":
                error = {"message": "Internal Server Error"}
                if ENV_TYPE == "dev":
                    error["error"] = e.detail
                    error["file_name"] = e.file_name
                    error["line_number"] = e.line_number
                    error["function"] = e.function
                    error["exception"] = exception_info.to_dict()
                ctx.body = json.dumps(error)
            else:
                if ENV_TYPE == "dev":
                    ctx.code = e.status_code
                    ctx.body += "-------------------------------------------------------------------------------\n"
                    ctx.body = "Error: " + e.detail
                    ctx.body += "\n"
                    ctx.body += "-------------------------------------------------------------------------------\n"
                    ctx.body += "Error Context:\n"
                    ctx.body += "File Name: " + e.file_name + "\n"
                    ctx.body += "Line Number: " + str(e.line_number) + "\n"
                    ctx.body += "Function: " + e.function + "\n"
                    ctx.body += "-------------------------------------------------------------------------------\n"
                    # TODO: add better debug support
                    # ctx.body += "Stack Trace:\n"
                    # ctx.body += TracebackInfo.from_frame().get_formatted()
                    # ctx.body += "\n"
                    # ctx.body += "-------------------------------------------------------------------------------\n"

            ctx.headers = e.headers

        return ctx

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        ctx = Context(scope, receive, send)
        app = await self._stack(ctx)
        await app(scope, receive, send)
