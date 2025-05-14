import asyncio
import ssl
import websockets

async def hello():
    uri = "wss://localhost:8002"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with websockets.connect(
            uri,
            ssl=ssl_context,
            ping_interval=10,  # kirim ping setiap 10 detik
            ping_timeout=5     # jika tidak ada pong dalam 5 detik, koneksi ditutup
        ) as websocket:
            while True:
                await websocket.send("PING from WSS client")
                print("✅ Sent: PING from WSS client")
                response = await asyncio.wait_for(websocket.recv(), timeout=30)
                print(f"📥 Received: {response}")
                await asyncio.sleep(10)
    except Exception as e:
        print(f"❌ Client error: {e}")

asyncio.run(hello())
