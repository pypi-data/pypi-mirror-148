from pydantic import BaseModel

from popug_sdk.conf.constants import (
    LOCALHOST,
    PortType,
    BASE_NAME,
)


class DatabaseSettings(BaseModel):
    host: str = LOCALHOST
    port: PortType = 5432
    user: str = "postgres"
    password: str = "postgres"
    database_name: str = f"{BASE_NAME}_db"
