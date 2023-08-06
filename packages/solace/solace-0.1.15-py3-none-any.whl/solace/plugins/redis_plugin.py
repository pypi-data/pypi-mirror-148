""" A Redis Plugin for Solace """
import redis

async def redis_plugin(ctx):
    """ A simple redis plugin provider """
    # TODO: add authentication support 
    # TODO: look into async redis support
    
    host = ctx.config.get('REDIS_HOST', 'localhost')
    port = ctx.config.get('REDIS_PORT', 6379)
    db = ctx.config.get('REDIS_DB', 0)
    r = redis.Redis(
        host = host,
        port = port,
        db = db
    )
    ctx.redis = r
    return ctx
