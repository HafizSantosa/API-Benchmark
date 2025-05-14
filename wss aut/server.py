import asyncio
import ssl
import websockets

MAX_CONNECTIONS = 3
VALID_TOKENS = {"secrettoken1", "secrettoken2"}
active_connections = set()

async def echo(websocket, path):
    print(f"📡 Incoming path: {path}")

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

    print("✅ Koneksi berhasil dengan token:", token)
    active_connections.add(websocket)

    try:
        while True:
            message = await asyncio.wait_for(websocket.recv(), timeout=30)
            print(f"📨 Diterima: {message}")
            await websocket.send("PONG from secured WSS server")
    except asyncio.TimeoutError:
        print("⚠️ Timeout: tidak ada data.")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"❌ Koneksi ditutup: {e}")
    finally:
        active_connections.remove(websocket)

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
