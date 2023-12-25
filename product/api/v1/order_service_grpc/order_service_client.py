from grpc import insecure_channel
from proto.order_pb2_grpc import OrderServiceStub
from settings import GRPC_SERVER_INFO

# Replace with your actual gRPC server address
order_service_channel = insecure_channel(GRPC_SERVER_INFO)
order_service_stub = OrderServiceStub(order_service_channel)
