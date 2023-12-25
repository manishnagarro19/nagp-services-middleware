from settings import (
    RABBIT_MQ_PORT,
    RABBIT_MQ_HOST,
    RABBIT_MQ_USERNAME,
    RABBIT_MQ_PASSWORD,
)
import pika


class RabbitMQPublisher:
    """
    A class for publishing messages to RabbitMQ.

    Attributes:
        exchange_name (str): The name of the RabbitMQ exchange.
        exchange_type (str): The type of the RabbitMQ exchange.
        routing_key (str): The routing key for the message.
        message_body (str): The body of the message to be published.
        credentials (pika.PlainCredentials): RabbitMQ connection credentials.
        parameters (pika.ConnectionParameters): RabbitMQ connection parameters.
        connection (pika.BlockingConnection): RabbitMQ connection instance.
        channel (pika.channel.Channel): RabbitMQ channel instance.

    Methods:
        publish_message(): Publishes the message to the RabbitMQ exchange.
    """

    def __init__(self, exchange_name, exchange_type, routing_key, message_body):
        """
        Initializes the RabbitMQPublisher instance.

        Args:
            exchange_name (str): The name of the RabbitMQ exchange.
            exchange_type (str): The type of the RabbitMQ exchange.
            routing_key (str): The routing key for the message.
            message_body (str): The body of the message to be published.
        """
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.routing_key = routing_key
        self.message_body = message_body

        self.credentials = pika.PlainCredentials(RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            host=RABBIT_MQ_HOST,
            port=RABBIT_MQ_PORT,
            virtual_host="/",
            credentials=self.credentials,
        )

        self.connection = None
        self.channel = None

    def publish_message(self):
        """
        Publishes the message to the RabbitMQ exchange.
        """
        with pika.BlockingConnection(self.parameters) as connection:
            self.connection = connection
            self.channel = self.connection.channel()

            self.channel.exchange_declare(
                exchange=self.exchange_name, exchange_type=self.exchange_type
            )
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=self.routing_key,
                body=self.message_body,
            )
