import asyncio
import ssl
import websockets

MAX_CONNECTIONS = 2
VALID_TOKENS = {"secrettoken1", "secrettoken2", "secrettoken3"}
active_connections = set()

async def echo(websocket, path):
    print(f"📡 Incoming path: {path}")

    # Ambil dan validasi token (seperti sebelumnya)
    token = None
    if '?' in path:
        query = path.split('?')[1]
        params = dict(q.split('=') for q in query.split('&') if '=' in q)
        token = params.get("token")

    if token not in VALID_TOKENS:
        print("❌ Token tidak valid.")
        await websocket.close(code=1008, reason="Unauthorized")
        return

    if len(active_connections) >= MAX_CONNECTIONS:
        print("🚫 Terlalu banyak koneksi.")
        await websocket.close(code=1013, reason="Too many connections")
        return

    active_connections.add(websocket)
    print("✅ Client terhubung:", token)

    async def receive_loop():
        try:
            while True:
                message = await websocket.recv()
                print(f"📥 Client: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("❌ Client putus (recv loop)")

    async def send_loop():
        try:
            while True:
                await websocket.send("📢 Hello from server!")
                await asyncio.sleep(10)
        except websockets.exceptions.ConnectionClosed:
            print("❌ Client putus (send loop)")

    try:
        await asyncio.gather(receive_loop(), send_loop())
    finally:
        active_connections.remove(websocket)
        print("ℹ️ Client keluar.")

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    async with websockets.serve(
        echo,
        "localhost",
        8002,
        ssl=ssl_context,
        ping_interval=10,
        ping_timeout=5
    ):
        print("🚀 WSS server running on wss://localhost:8002")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())


# limit con, auth