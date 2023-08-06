from solace.context import Context
from solace.validator import SolaceValidator

async def is_valid_json(ctx: Context) -> Context:
    async def is_valid_json_handler(validator: SolaceValidator) -> bool:
        json_data = await ctx.request.json()
        return validator(json_data)
    ctx.is_valid_json = is_valid_json_handler
    return ctx

async def is_valid_form(ctx: Context) -> Context:
    async def is_valid_form_handler(validator: SolaceValidator) -> bool:
        form_data = await ctx.request.form()
        return validator(form_data)
    ctx.is_valid_form = is_valid_form_handler
    return ctx
