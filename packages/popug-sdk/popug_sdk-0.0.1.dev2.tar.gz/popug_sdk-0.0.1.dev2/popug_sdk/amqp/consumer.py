import logging

import pika

from popug_sdk.amqp.utils import get_connection_params
from popug_sdk.conf import settings
from popug_sdk.conf.amqp import AMQPSettings

logger = logging.getLogger(settings.project)


class BaseConsumer:
    TIMEOUT = 5

    def __init__(self, config: AMQPSettings):
        self._config = config

        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._threads = []

    def _connect(self) -> pika.SelectConnection:
        parameters = get_connection_params(self._config)

        logger.info(
            f"Connecting to host={parameters.host} port={parameters.port} "
            f"virtual_host={parameters.virtual_host}>"
        )
        return pika.SelectConnection(parameters, self._on_connection_open)

    def _on_connection_open(self, _):
        logger.info("Connection opened")
        self._connection.add_on_close_callback(self._on_connection_closed)
        self._connection.channel(on_open_callback=self._on_channel_open)

    def _on_connection_closed(self, _, reason):
        if self._closing:
            self._connection.ioloop.stop()
        else:
            logger.warning(
                f"Connection closed, "
                f"reopen in {self.TIMEOUT} seconds: {reason}"
            )
            self._connection.add_timeout(self.TIMEOUT, self._reconnect)

    def _reconnect(self):
        self._connection.ioloop.stop()

        if not self._closing:
            self._connection = self._connect()
            self._connection.ioloop.start()

    def _on_channel_open(self, channel):
        logger.info("Channel opened")
        self._channel = channel
        self._channel.add_on_close_callback(
            lambda *_: self._connection.close
        )

        self._setup_exchange()

    def _setup_exchange(self):
        exchange_name = self._config.exchange.name
        logger.info(f"Declaring exchange {exchange_name}")

        self._channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=self._config.exchange.type,
            callback=self._setup_queue,
            durable=self._config.exchange.durable,
        )

    def _setup_queue(self, _):
        queue_name = self._config.queue.name
        logger.info("Declaring queue %s", queue_name)
        self._channel.queue_declare(
            queue=queue_name,
            callback=self._on_queue_declareok
        )

    def _on_queue_declareok(self, _):
        for routing_key in self._config.routing_keys:
            logger.info(
                f"Binding {self._config.exchange.name} to "
                f"{self._config.queue.name} with {routing_key}",
            )
            self._channel.queue_bind(
                queue=self._config.queue.name,
                exchange=self._config.exchange.name,
                routing_key=routing_key,
                callback=self._start_consuming,
            )

    def _start_consuming(self, _):
        logger.info("Issuing consumer related RPC commands")
        self._channel.add_on_cancel_callback(self._channel.close)
        self._consumer_tag = self._channel.basic_consume(
            queue=self._config.queue.name,
            on_message_callback=self.on_message,
        )

    def on_message(self, _, basic_deliver, properties, body):
        logger.debug(
            f"Received message # {basic_deliver.delivery_tag} "
            f"from {properties.app_id}: {body}"
        )
        self.process_message(basic_deliver, properties, body)
        self._channel.basic_ack(basic_deliver.delivery_tag)

    def process_message(self, basic_deliver, properties, message):
        pass

    def run(self):
        self._connection = self._connect()
        self._connection.ioloop.start()

    def stop(self):
        logger.info("Stopping")
        self._closing = True
        self._channel.basic_cancel(
            consumer_tag=self._consumer_tag,
            callback=lambda _: self._channel.close,
        )
        self._connection.ioloop.start()
        logger.info("Stopped")
