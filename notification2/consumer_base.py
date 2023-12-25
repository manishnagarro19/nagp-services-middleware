import pika
import json
from settings import (
    RABBIT_MQ_PORT,
    RABBIT_MQ_HOST,
    RABBIT_MQ_USERNAME,
    RABBIT_MQ_PASSWORD,
    EXCHANGE_INFO,
    NOTIFICATION_2_QUEUE_NAME,
    logger,
)


class RabbitMQConsumerBase:
    """
    A class for consuming messages from RabbitMQ.

    Attributes:
        credentials (pika.PlainCredentials): RabbitMQ connection credentials.
        parameters (pika.ConnectionParameters): RabbitMQ connection parameters.
        connection (pika.BlockingConnection): RabbitMQ connection instance.
        channel (pika.channel.Channel): RabbitMQ channel instance.

    Methods:
        callback(ch, method, properties, body): Callback function to process incoming messages.
        consume_messages(): Starts consuming messages from the RabbitMQ queue.
    """

    PORT = RABBIT_MQ_PORT

    def __init__(self):
        """
        Initializes the RabbitMQConsumer instance.
        """
        self.credentials = pika.PlainCredentials(RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
        self.parameters = pika.ConnectionParameters(
            host=RABBIT_MQ_HOST,
            port=RABBIT_MQ_PORT,
            virtual_host="/",
            credentials=self.credentials,
        )
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def callback(self, ch, method, properties, body):
        """
        Callback function to process incoming messages.

        Args:
            ch (pika.channel.Channel): The RabbitMQ channel.
            method (pika.spec.Basic.Deliver): Delivery information.
            properties (pika.spec.BasicProperties): Message properties.
            body (bytes): The message body.
        """
        message_body = json.loads(body)
        event_name = message_body.get("event_type")
        order_id = message_body.get("order_id")
        product_id = message_body.get("product_id")
        logger.info(
            f"We received an order with the information: Event name: {event_name}, Order ID: {order_id}  "
            f"and Product ID: {product_id}"
        )

    def consume_messages(self):
        """
        Starts consuming messages from the RabbitMQ queue.
        """
        order_place_exchange_info = EXCHANGE_INFO.get("order_place")
        order_update_exchange_info = EXCHANGE_INFO.get("order_update")

        self.channel.exchange_declare(
            exchange=order_update_exchange_info.get("exchange_name"),
            exchange_type=order_update_exchange_info.get("exchange_type"),
        )

        result = self.channel.queue_declare(
            queue=NOTIFICATION_2_QUEUE_NAME, exclusive=False
        )
        queue_name = result.method.queue

        self.channel.queue_bind(
            exchange=order_place_exchange_info.get("exchange_name"),
            routing_key=order_place_exchange_info.get("routing_key"),
            queue=queue_name,
        )
        self.channel.queue_bind(
            exchange=order_update_exchange_info.get("exchange_name"),
            routing_key=order_update_exchange_info.get("routing_key"),
            queue=queue_name,
        )

        print("Waiting for messages. To exit press CTRL+C")

        self.channel.basic_consume(
            queue=queue_name, on_message_callback=self.callback, auto_ack=True
        )
        self.channel.start_consuming()
