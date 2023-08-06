from redis import ConnectionPool

from popug_sdk.conf.redis import RedisSettings

_redis_pools = {}


def init_redis_pool(config: dict[str, RedisSettings]):
    close_redis_pool()
    _redis_pools.clear()

    for config_name, redis_pool_config in config.items():
        _redis_pools[config_name] = ConnectionPool(
            host=redis_pool_config.host,
            port=redis_pool_config.port,
            db=redis_pool_config.db,
        )


def close_redis_pool():
    for pool in _redis_pools.values():
        pool.disconnect()


def get_redis_pool(config_name: str = "default") -> ConnectionPool:
    if not _redis_pools:
        raise Exception("Call create_redis_pool() first")
    return _redis_pools[config_name]
