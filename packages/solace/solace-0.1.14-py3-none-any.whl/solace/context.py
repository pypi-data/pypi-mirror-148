from starlette.types import Scope, Send, Receive
from starlette.requests import Request
from starlette.responses import (
    Response, 
    FileResponse, 
    JSONResponse, 
    HTMLResponse, 
    StreamingResponse
)

from .templating import templates

class Context:

    body: str = None # the response body
    html: str = None # use for html based responses
    file: str = None # use for file based responses
    text: str = None # use for plain/text based responses
    json: dict = None # use for JSON based responses
    blob: str = None # use for Streaming Responses
    view: str = None # use for Template Responses
    data: dict = {} # use for Template Responses

    code: int = 200 # the status code
    headers: dict = {}

    def __init__(self, scope: Scope, receive: Receive, send: Send):
        self.request = Request(scope = scope, receive = receive, send = send)
    
    @property
    def path(self):
        """ the request path """
        return self.request.url
    
    @property
    def method(self):
        """ the request method """
        return self.request.method
    
    @property
    def _final_response(self):
        # TODO: check which of the response "types" are set
        # and create the appropriate "Response" object for it
        # as well as set proper headers, status codes, etc.

        # TODO: validate 'code' is within range for a proper 
        # http status code.
        
        if self.body is not None:
            return Response(
                content = self.body,
                status_code = self.code,
                headers = self.headers
            )

        elif self.html is not None:
            self.headers["Content-Type"] = "text/html"
            return HTMLResponse(
                content = self.html,
                status_code = self.code,
                headers = self.headers,
            )

        elif self.json is not None:
            return JSONResponse(
                content = self.json,
                status_code = self.code,
                headers = self.headers
            )

        elif self.file is not None:
            return FileResponse(
                path = self.file,
                status_code = self.code,
                headers = self.headers
            )
        
        elif self.blob is not None:

            return StreamingResponse(
                content = self.blob,
                status_code = self.code,
                headers = self.headers
            )
        
        elif self.view is not None:
            return templates.TemplateResponse(
                name = self.view,
                context = self.data,
                status_code = self.code,
                headers = self.headers
            )