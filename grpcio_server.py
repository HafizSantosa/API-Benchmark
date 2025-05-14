import grpc
from concurrent import futures
import ping_pb2
import ping_pb2_grpc

class PingService(ping_pb2_grpc.PingServiceServicer):
    def Ping(self, request, context):
        return ping_pb2.PingReply(message="pong")

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
ping_pb2_grpc.add_PingServiceServicer_to_server(PingService(), server)
server.add_insecure_port("[::]:8003")
server.start()
server.wait_for_termination()
