from consumer_base import RabbitMQConsumerBase


class RabbitMQConsumer(RabbitMQConsumerBase):
    """
    A class for consuming messages from RabbitMQ.

    Attributes:
        queue_name (str): The name of the RabbitMQ queue to consume messages from.
        credentials (pika.PlainCredentials): RabbitMQ connection credentials.
        parameters (pika.ConnectionParameters): RabbitMQ connection parameters.
        connection (pika.BlockingConnection): RabbitMQ connection instance.
        channel (pika.channel.Channel): RabbitMQ channel instance.

    Methods:
        consume_messages(): Starts consuming messages from the RabbitMQ queue.
        callback(ch, method, properties, body): Callback function to process incoming messages.
    """

    def __init__(self):
        """
        Initializes the RabbitMQConsumer instance.

        Args:
            queue_name (str): The name of the RabbitMQ queue to consume messages from.
        """
        super(RabbitMQConsumer, self).__init__()

    def consume_messages_place_order_queue(self):
        """
        Starts consuming messages from the RabbitMQ queue.
        """
        self.consume_messages()


# Example usage:
if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.consume_messages_place_order_queue()
