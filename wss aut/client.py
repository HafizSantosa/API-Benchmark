import asyncio
import ssl
import websockets

async def hello():
    uri = "wss://localhost:8002?token=secrettoken1"

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            await websocket.send("PING")
            print("✅ Sent: PING")
            response = await websocket.recv()
            print(f"✅ Received: {response}")
    except Exception as e:
        print(f"❌ Client error: {e}")

if __name__ == "__main__":
    asyncio.run(hello())
