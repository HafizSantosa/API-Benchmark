import asyncio
import websockets
import ssl

async def heartbeat_client():
    uri = "wss://localhost:8002/?token=secrettoken2"
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE  # Hanya untuk testing!

    try:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            print("✅ Tersambung ke server.")
            while True:
                await websocket.send("PING")
                print("✅ Sent: PING")
                response = await websocket.recv()
                print(f"📥 Received: {response}")
                await asyncio.sleep(5)  # Kirim ping setiap 5 detik
    except Exception as e:
        print(f"❌ Client error: {e}")

if __name__ == "__main__":
    asyncio.run(heartbeat_client())
