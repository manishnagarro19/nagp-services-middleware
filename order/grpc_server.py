import grpc
from concurrent import futures
from proto import order_pb2_grpc
from order_service import OrderService
from settings import GRPC_SERVER_PORT


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port(f"[::]:{GRPC_SERVER_PORT}")
    server.start()
    print("gRPC server is running on port 50051")
    server.wait_for_termination()


if __name__ == "__main__":
    run_server()
