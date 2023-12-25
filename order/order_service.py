import json
import uuid

from rabbitmq_publisher import RabbitMQPublisher
from proto import order_pb2, order_pb2_grpc
from pydantic import BaseModel
from settings import EXCHANGE_INFO, logger


class OrderEvent(BaseModel):
    """
    Represents an order event.

    Attributes:
        event_type (str): The type of the order event.
        order_id (int): The ID of the order associated with the event.
    """

    event_type: str
    product_id: int
    order_id: str


class OrderService(order_pb2_grpc.OrderServiceServicer):
    """
    gRPC service for handling order-related operations.

    Attributes:
        None

    Methods:
        get_exchange_info(event_type): Get exchange information based on the event type.
        __generate_order_id(): Generate a unique order ID.
        publish_order_event(exchange_info, event_type, order_id): Publish an order event to RabbitMQ.
        PlaceOrder(request, context): gRPC method for placing an order.
        UpdateOrder(request, context): gRPC method for updating an order.
    """

    def get_exchange_info(self, event_type):
        """
        Get exchange information based on the event type.

        Args:
            event_type (str): The type of the order event.

        Returns:
            dict: Exchange information.
        """
        return EXCHANGE_INFO.get(event_type)

    def __generate_order_id(self):
        """
        Generate a unique order ID.

        Returns:
            str: The generated order ID.
        """
        return str(uuid.uuid4())

    def publish_order_event(self, exchange_info, event_type, product_id, order_id):
        """
        Publish an order event to RabbitMQ.

        Args:
            exchange_info (dict): Exchange information.
            event_type (str): The type of the order event.
            product_id (int): The ID of the order associated with the event.
            order_id (str): The ID of the order associated with the event.

        Returns:
            None
        """
        order_event = OrderEvent(
            event_type=event_type, product_id=product_id, order_id=order_id
        )
        message_body = json.dumps(order_event.dict())

        publisher = RabbitMQPublisher(
            exchange_name=exchange_info.get("exchange_name"),
            exchange_type=exchange_info.get("exchange_type"),
            routing_key=exchange_info.get("routing_key"),
            message_body=message_body,
        )
        publisher.publish_message()

    def PlaceOrder(self, request, context):
        """
        gRPC method for placing an order.

        Args:
            request (order_pb2.OrderRequest): The order request.
            context (Any): gRPC context.

        Returns:
            order_pb2.OrderResponse: The order response.
        """
        exchange_info = self.get_exchange_info("order_place")
        event_name = exchange_info.get("event_name")
        product_id = request.product_id
        order_id = self.__generate_order_id()

        logger.info(
            f"Order is created successfully. Event name: {event_name}, Product ID: {product_id}, Order ID: {order_id}"
        )

        # Publish event for order creation
        self.publish_order_event(exchange_info, event_name, product_id, order_id)

        return order_pb2.OrderResponse(order_id=request.product_id)

    def UpdateOrder(self, request, context):
        """
        gRPC method for updating an order.

        Args:
            request (order_pb2.OrderRequest): The order request.
            context (Any): gRPC context.

        Returns:
            order_pb2.OrderResponse: The order response.
        """
        exchange_info = self.get_exchange_info("order_update")
        event_name = exchange_info.get("event_name")
        product_id = request.product_id
        order_id = request.order_id

        logger.info(
            f"Updating order. Event name: {event_name}, Order ID: {order_id} Product ID: {product_id}"
        )

        # Publish event for order update
        self.publish_order_event(exchange_info, event_name, product_id, order_id)

        return order_pb2.OrderResponse(order_id=order_id)
