from typing import Callable
from .env import *

from starlette.applications import Starlette
from starlette.types import ASGIApp
from .flow import SolaceFlow
from .validator import SolaceValidator as SolaceValidator
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

class Solace:
    """ creates an application instance """
    
    def __init__(self, **kwargs):
        
        self.debug = kwargs.get('debug', False)
        self.env_name = ENV_NAME
        self.env_type = ENV_TYPE
        self.handlers = []

        self.app = Starlette(
            debug = self.debug
        )
    
    def use(self, *handlers: Callable):
        for h in handlers:
            self.handlers.append(h)
    
    def _populate(self, path: str, method: str, *handlers:callable):
        flow = SolaceFlow()
        self.handlers.extend(handlers)
        for h in self.handlers:
            flow.stack.append(h)
        self.app.add_route(
            path = path, 
            route = flow,
            methods = [method]
        )

    def get(self, path: str, *handlers: Callable):
        """ adds a GET request flow handler """
        self._populate(path, 'GET', *handlers)
    
    def head(self, path: str, *handlers: Callable):
        """ adds a HEAD request flow handler """
        self._populate(path, 'HEAD', *handlers)
    
    def post(self, path: str, *handlers: Callable):
        """ adds a POST request flow handler """
        self._populate(path, 'POST', *handlers)
    
    def put(self, path: str, *handlers: Callable):
        """ adds a PUT request flow handler """
        self._populate(path, 'PUT', *handlers)
    
    def delete(self, path: str, *handlers: Callable):
        """ adds a DELETE request flow handler """
        self._populate(path, 'DELETE', *handlers)
    
    def connect(self, path: str, *handlers: Callable):
        """ adds a CONNECT request flow handler """
        self._populate(path, 'CONNECT', *handlers)
    
    def options(self, path: str, *handlers: Callable):
        """ adds a OPTIONS request flow handler """
        self._populate(path, 'OPTIONS', *handlers)
    
    def trace(self, path: str, *handlers: Callable):
        """ adds a TRACE request flow handler """
        self._populate(path, 'TRACE', *handlers)
    
    def patch(self, path: str, *handlers: Callable):
        """ adds a PATCH request flow handler """
        self._populate(path, 'PATCH', *handlers)
    
    def ws(self, path: str, *handlers: Callable):
        flow = SolaceFlow()
        self.handlers.extend(handlers)
        for h in self.handlers:
            flow.stack.append(h)
        self.app.add_websocket_route(
            path = path, 
            route = flow,
        )

    def __call__(self) -> ASGIApp:
        """ returns a configured ASGIApp instance """
        if STATIC_ASSETS_DIR is not None and STATIC_ASSETS_URL is not None:
            self.app.routes.append(
                Mount(
                    STATIC_ASSETS_URL, 
                    app = StaticFiles(directory=STATIC_ASSETS_DIR),
                    name="static"
                )
            )
        return self.app
