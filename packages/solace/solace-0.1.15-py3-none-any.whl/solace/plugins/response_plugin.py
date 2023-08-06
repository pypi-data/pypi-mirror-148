""" A Response Plugin for Solace """

from starlette.responses import *
from solace.context import Context
from solace.templating import templates

def json_response(ctx: Context):
    ctx.trace("start json response plugin")
    def json_response_handler(data: dict = {}):
        """ provider to add json response type """
        return JSONResponse(
            content = data,
            status_code = ctx.code,
            headers = ctx.headers
        )
    # TODO: check if a json property already exists
    # and warn if this will overwrite it
    ctx.json_response = json_response_handler
    ctx.trace("end json response plugin")
    return ctx

def plain_text_response(ctx: Context):
    ctx.trace("start plain text response plugin")
    def plain_text_response_handler(text: str):
        """ provider to add text response type """
        return PlainTextResponse(
            content = text,
            status_code = ctx.code,
            headers = ctx.headers
        )
    # TODO: check if a json property already exists
    # and warn if this will overwrite it
    ctx.plain_text_response = plain_text_response_handler
    ctx.trace("end plain text response plugin")
    return ctx

async def render_template(ctx: Context):
    """ adds support for rendering Jinja2 Templates """
    ctx.trace("start template response plugin")
    async def render_template_handler(template: str, data: dict = {}):
        view = templates.TemplateResponse(
            name = template,
            context = data,
            headers = ctx.headers
        )
        return view
    if templates:
        ctx.render_template = render_template_handler
    ctx.trace("end template response plugin")
    return ctx

# TODO: add other response types
