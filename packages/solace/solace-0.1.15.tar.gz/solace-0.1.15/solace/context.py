import os
from .env import *
from starlette.types import *
from starlette.requests import Request
from starlette.exceptions import HTTPException
from inspect import getframeinfo, stack
from box import Box

class ContextualHTTPException(HTTPException):
    line_number: int = None
    file_name: str = None
    function: str = None
    def __init__(self, status_code: int, detail: str = None, headers: dict = None) -> None:
        super().__init__(status_code, detail, headers)

class Context:
    
    debug: bool = False # TODO: add more debugging support
    body: str = ''
    code: int = 200
    charset = "utf-8"
    frames: list = []
    headers: dict = {}
    
    def __init__(self, scope: Scope, receive: Receive, send: Send):
        self.request = Request(scope = scope, receive = receive, send = send)
        self.config = Box({})
        self._populate_config()
    
    def _populate_config(self):
        """ populates the config object with default environment variable values """
        for v in os.environ:
            self.config[v] = os.environ.get(v)

    @property
    def url(self) -> str:
        return self.request.url
    
    @property
    def method(self) -> str:
        return self.request.method
    
    @property
    def params(self) -> dict:
        return self.request.path_params
    
    @property
    def args(self) -> dict:
        return dict(self.request.query_params)
    
    def error(self, message: str, code: int = 400):
        """ interrupt the flow, and return a proper http error """
        caller = getframeinfo(stack()[1][0])
        e = ContextualHTTPException(
            status_code = code,
            detail = message,
            headers = self.headers
        )
        e.file_name = caller.filename
        e.function = caller.function
        e.line_number = caller.lineno
        if hasattr(self, 'logger'):
            self.logger.error(message)
            self.logger.debug(f"Filename: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
        raise e
    
    def warn(self, message: str):
        """ display a warning message if a logger is configured """
        caller = getframeinfo(stack()[1][0])
        if hasattr(self, 'logger'):
            self.logger.warning(message)
            self.logger.debug(f"Filename: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
    
    def info(self, message: str):
        """ display a info message if a logger is configured """
        caller = getframeinfo(stack()[1][0])
        if hasattr(self, 'logger'):
            self.logger.info(message)
            self.logger.debug(f"Filename: {caller.filename}")
            self.logger.debug(f"Line Number: {caller.lineno}")
            self.logger.debug(f"Function: {caller.function}")
    
    def trace(self, label: str = None):
        """ trace the context """
        if TRACERS_ENABLED:
            caller = getframeinfo(stack()[1][0])
            frame = {
                "filename": caller.filename,
                "line_number": caller.lineno,
                "function": caller.function
            }
            if label:
                frame["label"] = label
            self.frames.append(frame)

    def _body(self) -> bytes:
        """ ensures the body is properly set """
        if self.body == '':
            return b""
        if isinstance(self.body, bytes):
            return self.body
        return self.body.encode(self.charset)

    def _headers(self):
        """ ensures that the headers are properly set """
        raw_headers = [
            (k.lower().encode("latin-1"), v.encode("latin-1"))
            for k, v in self.headers.items()
        ]
        keys = [h[0] for h in raw_headers]
        body = getattr(self, "body", None)
        populate_content_length = b"content-length" not in keys
        
        if (
            body is not None
            and populate_content_length
            and not (self.code < 200 or self.code in (204, 304))
        ):
            content_length = str(len(body))
            raw_headers.append((b"content-length", content_length.encode("latin-1")))
    
        return raw_headers

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await send(
            {
                "type": "http.response.start",
                "status": self.code,
                "headers": self._headers(),
            }
        )
        await send({"type": "http.response.body", "body": self._body()})
