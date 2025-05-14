import time
import requests
import asyncio
import websockets
import grpc
import ping_pb2
import ping_pb2_grpc

# REST
def test_rest(n=100):
    start = time.time()
    for _ in range(n):
        requests.get("http://localhost:5000/ping")
    return (time.time() - start) / n

# WebSocket
async def test_ws(n=100):
    uri = "ws://localhost:8001/ws"
    async with websockets.connect(uri) as websocket:
        start = time.time()
        for _ in range(n):
            await websocket.send("ping")
            await websocket.recv()
        return (time.time() - start) / n

# gRPC
def test_grpc(n=100):
    channel = grpc.insecure_channel('localhost:8003')
    stub = ping_pb2_grpc.PingServiceStub(channel)
    start = time.time()
    for _ in range(n):
        stub.Ping(ping_pb2.PingRequest(message="ping"))
    return (time.time() - start) / n

# Run all
def run_tests(n=100):
    print(f"Testing with {n} requests each...")
    print("REST avg time:", test_rest(n))
    print("gRPC avg time:", test_grpc(n))
    print("WebSocket avg time:", asyncio.run(test_ws(n)))

run_tests(100)
