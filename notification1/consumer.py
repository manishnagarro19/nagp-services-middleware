from consumer_base import RabbitMQConsumerBase


class RabbitMQConsumer(RabbitMQConsumerBase):
    """
    A class for consuming messages from RabbitMQ.

    Attributes:
        None

    Methods:
        __init__(): Initializes the RabbitMQConsumer instance.
        consume_messages_place_order_queue(): Starts consuming messages from the RabbitMQ 'order_place' queue.
    """

    def __init__(self):
        """
        Initializes the RabbitMQConsumer instance.
        """
        super(RabbitMQConsumer, self).__init__()

    def consume_messages_place_order_queue(self):
        """
        Starts consuming messages from the RabbitMQ 'order_place' queue.
        """
        self.consume_message("order_place")


# Example usage:
if __name__ == "__main__":
    consumer = RabbitMQConsumer()
    consumer.consume_messages_place_order_queue()
