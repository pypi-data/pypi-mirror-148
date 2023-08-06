from pika.exchange_type import ExchangeType
from pydantic import (
    BaseModel,
    Field,
)

from popug_sdk.conf.constants import (
    LOCALHOST,
    PortType,
)


class ExchangeSettings(BaseModel):
    type: ExchangeType = ExchangeType.topic
    name: str | None = None
    durable: bool = True


class QueueSettings(BaseModel):
    name: str | None = None


class AMQPSettings(BaseModel):
    host: str = LOCALHOST
    port: PortType = 5672
    username: str = "guest"
    password: str = "guest"
    virtual_host: str = "/"
    exchange: ExchangeSettings = Field(default_factory=ExchangeSettings)
    queue: QueueSettings = Field(default_factory=QueueSettings)
    routing_keys: list[str] = Field(default_factory=list)

    @property
    def url(self) -> str:
        amqp_url_template = 'amqp://{user}:{password}' \
                            '@{host}:{port}{virtual_host}'
        return amqp_url_template.format(
            username=self.username,
            password=self.password,
            host=self.host,
            port=self.port,
            virtualhost=self.virtual_host,
        )
