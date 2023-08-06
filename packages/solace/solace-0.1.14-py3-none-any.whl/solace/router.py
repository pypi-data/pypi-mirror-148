import asyncio
import typing
import traceback
from .context import Context
from starlette.types import *
from starlette.responses import RedirectResponse, PlainTextResponse
from starlette.websockets import WebSocketClose
from starlette.datastructures import URL, URLPath
from starlette.exceptions import HTTPException
from starlette.routing import (
    Route,
    WebSocketRoute,
    BaseRoute, 
    _DefaultLifespan, 
    Match, 
    NoMatchFound
)

# majority borrowed from Starlette's router..
class SolaceRouter:
    def __init__(
        self,
        routes: typing.Optional[typing.Sequence[BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: typing.Optional[ASGIApp] = None,
        on_startup: typing.Optional[typing.Sequence[typing.Callable]] = None,
        on_shutdown: typing.Optional[typing.Sequence[typing.Callable]] = None,
        lifespan: typing.Optional[
            typing.Callable[[typing.Any], typing.AsyncContextManager]
        ] = None,
    ) -> None:
        self.routes = [] if routes is None else list(routes)
        self.redirect_slashes = redirect_slashes
        self.default = self.not_found if default is None else default
        self.on_startup = [] if on_startup is None else list(on_startup)
        self.on_shutdown = [] if on_shutdown is None else list(on_shutdown)

        if lifespan is None:
            self.lifespan_context: typing.Callable[
                [typing.Any], typing.AsyncContextManager
            ] = _DefaultLifespan(self)
        else:
            self.lifespan_context = lifespan

    async def not_found(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "websocket":
            websocket_close = WebSocketClose()
            await websocket_close(scope, receive, send)
            return

        # If we're running inside a starlette application then raise an
        # exception, so that the configurable exception handler can deal with
        # returning the response. For plain ASGI apps, just return the response.
        if "app" in scope:
            raise HTTPException(status_code=404)
        else:
            response = PlainTextResponse("Not Found", status_code=404)
        await response(scope, receive, send)

    def url_path_for(self, name: str, **path_params: typing.Any) -> URLPath:
        for route in self.routes:
            try:
                return route.url_path_for(name, **path_params)
            except NoMatchFound:
                pass
        raise NoMatchFound(name, path_params)

    async def startup(self) -> None:
        """
        Run any `.on_startup` event handlers.
        """
        for handler in self.on_startup:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def shutdown(self) -> None:
        """
        Run any `.on_shutdown` event handlers.
        """
        for handler in self.on_shutdown:
            if asyncio.iscoroutinefunction(handler):
                await handler()
            else:
                handler()

    async def lifespan(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        Handle ASGI lifespan messages, which allows us to manage application
        startup and shutdown events.
        """
        started = False
        app = scope.get("app")
        await receive()
        try:
            async with self.lifespan_context(app):
                await send({"type": "lifespan.startup.complete"})
                started = True
                await receive()
        except BaseException:
            exc_text = traceback.format_exc()
            if started:
                await send({"type": "lifespan.shutdown.failed", "message": exc_text})
            else:
                await send({"type": "lifespan.startup.failed", "message": exc_text})
            raise
        else:
            await send({"type": "lifespan.shutdown.complete"})

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """
        The main entry point to the Router class.
        """
        assert scope["type"] in ("http", "websocket", "lifespan")

        if "router" not in scope:
            scope["router"] = self

        if scope["type"] == "lifespan":
            await self.lifespan(scope, receive, send)
            return

        partial = None
        ctx = Context(scope = scope, receive = receive, send = send)
        for route in self.routes:
            # Determine if any route matches the incoming scope,
            # and hand over to the matching route if found.
            match, child_scope = route.matches(scope)
            if match == Match.FULL:
                scope.update(child_scope)
                await route.handle(scope, receive, send)
                return
            elif match == Match.PARTIAL and partial is None:
                partial = route
                partial_scope = child_scope

        if partial is not None:
            #  Handle partial matches. These are cases where an endpoint is
            # able to handle the request, but is not a preferred option.
            # We use this in particular to deal with "405 Method Not Allowed".
            scope.update(partial_scope)
            await partial.handle(scope, receive, send)
            return

        if scope["type"] == "http" and self.redirect_slashes and scope["path"] != "/":
            redirect_scope = dict(scope)
            if scope["path"].endswith("/"):
                redirect_scope["path"] = redirect_scope["path"].rstrip("/")
            else:
                redirect_scope["path"] = redirect_scope["path"] + "/"

            for route in self.routes:
                match, child_scope = route.matches(redirect_scope)
                if match != Match.NONE:
                    redirect_url = URL(scope=redirect_scope)
                    response = RedirectResponse(url=str(redirect_url))
                    await response(scope, receive, send)
                    return

        await self.default(scope, receive, send)

    def __eq__(self, other: typing.Any) -> bool:
        return isinstance(other, SolaceRouter) and self.routes == other.routes

    def add_route(
        self,
        path: str,
        endpoint: typing.Callable,
        methods: typing.Optional[typing.List[str]] = None,
        name: typing.Optional[str] = None,
        include_in_schema: bool = True,
    ) -> None:  # pragma: nocover
        route = Route(
            path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
        )
        self.routes.append(route)

    def add_websocket_route(
        self, path: str, endpoint: typing.Callable, name: typing.Optional[str] = None
    ) -> None:  # pragma: no cover
        route = WebSocketRoute(path, endpoint=endpoint, name=name)
        self.routes.append(route)

    def add_event_handler(
        self, event_type: str, func: typing.Callable
    ) -> None:  # pragma: no cover
        assert event_type in ("startup", "shutdown")

        if event_type == "startup":
            self.on_startup.append(func)
        else:
            self.on_shutdown.append(func)

    def on_event(self, event_type: str) -> typing.Callable:  # pragma: nocover
        def decorator(func: typing.Callable) -> typing.Callable:
            self.add_event_handler(event_type, func)
            return func

        return decorator
    
    def get(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['GET'])

    def head(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['HEAD'])

    def post(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['POST'])

    def put(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['PUT'])

    def delete(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['DELETE'])

    def connect(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['CONNECT'])

    def trace(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['TRACE'])

    def patch(self, path: str, handler: typing.Callable):
        self.add_route(path = path, endpoint = handler, methods = ['PATCH'])
