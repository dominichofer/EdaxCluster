import logging
from rte import Server, GrpcServer

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    server = Server(task_timeout=30)
    grpc_server = GrpcServer(server, port=50051)
    grpc_server.start()
    grpc_server.wait_for_termination()
