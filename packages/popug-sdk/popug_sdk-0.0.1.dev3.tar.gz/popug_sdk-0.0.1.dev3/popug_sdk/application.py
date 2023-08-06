from datetime import datetime

from fastapi import (
    APIRouter,
    FastAPI,
)
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.openapi.utils import get_openapi

from popug_sdk.conf import settings
from popug_sdk.schemas.pong import Pong

__all__ = (
    "app",
)


def custom_openapi(app):
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.project,
        version=settings.version or "0.0.1",
        routes=app.routes,
    )
    openapi_schema["x-tagGroups"] = settings.tag_groups
    app.openapi_schema = openapi_schema
    return app.openapi_schema


healthcheck_router = APIRouter()


@healthcheck_router.get("/", response_model=Pong)
def ping():
    """Healthcheck endpoint"""

    return {
        "project": settings.project,
        "version": settings.version,
        "datetime": datetime.utcnow().isoformat()
    }


app = FastAPI(title=settings.project)


if settings.use_https:
    app.add_middleware(HTTPSRedirectMiddleware)

app.openapi = lambda: custom_openapi(app)
app.include_router(healthcheck_router, prefix="")


@app.on_event("startup")
def startup():
    if settings.database.enabled:
        from popug_sdk.db import init_db  # noqa
        init_db()

    if settings.redis:
        from popug_sdk.redis.redis_pool import init_redis_pool  # noqa
        init_redis_pool(settings.redis)


@app.on_event("shutdown")
def shutdown():
    if settings.redis:
        from popug_sdk.redis.redis_pool import close_redis_pool  # noqa
        close_redis_pool()
