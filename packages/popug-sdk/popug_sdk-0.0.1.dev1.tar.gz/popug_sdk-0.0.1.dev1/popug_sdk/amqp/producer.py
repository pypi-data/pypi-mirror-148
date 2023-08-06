import logging

import pika

from popug_sdk.amqp.utils import get_connection_params
from popug_sdk.conf import settings
from popug_sdk.conf.amqp import AMQPSettings


logger = logging.getLogger(settings.project)


class BaseProducer:
    def __init__(self, config: AMQPSettings, init_exchange: bool = False):
        self._config = config
        self._init_exchange = init_exchange

        self._connection = None
        self._channel = None

    @property
    def is_closed_connection(self) -> bool:
        return not self._connection or self._connection.is_closed

    @property
    def is_closed_channel(self) -> bool:
        return not self._channel or self._channel.is_closed

    def _open_connection(self):
        if self.is_closed_connection or self.is_closed_channel:

            if self.is_closed_connection:
                parameters = get_connection_params(self._config)
                logger.info(
                    f"Connecting to host={parameters.host} port={parameters.port} "
                    f"virtual_host={parameters.virtual_host}>"
                )
                self._connection = pika.BlockingConnection(parameters)

            if self.is_closed_channel:
                self.channel = self._connection.channel()

            if self._init_exchange is True:
                logger.info(
                    f"Creating a new exchange. "
                    f"Exchange: {self._config.exchange.name}"
                )
                self._channel.exchange_declare(
                    exchange=self._config.exchange.name,
                    exchange_type=self._config.exchange.type,
                    durable=self._config.exchange.durable,
                )
                self._init_exchange = False

    def publish_message(self, body, routing_key):
        if self.is_closed_connection or self.is_closed_channel:
            self._open_connection()

        logger.info(
            f"Publishing to routing_key {routing_key}, "
            f"exchange {self._config.exchange.name}, message {body}"
        )

        self.channel.basic_publish(
            exchange=self._config.exchange.name,
            routing_key=routing_key,
            body=body,
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2
            )
        )
