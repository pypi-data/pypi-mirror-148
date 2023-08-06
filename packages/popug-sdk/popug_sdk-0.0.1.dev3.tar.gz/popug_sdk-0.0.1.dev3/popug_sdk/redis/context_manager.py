from contextlib import contextmanager

from redis import ConnectionPool

from popug_sdk.conf import settings
from popug_sdk.redis.redis_pool import (
    init_redis_pool,
    get_redis_pool,
)


@contextmanager
def redis_pool(config_name: str) -> ConnectionPool:
    init_redis_pool({config_name: settings.redis[config_name]})
    pool = get_redis_pool(config_name)

    try:
        yield pool
    finally:
        pool.disconnect()
