import asyncio
import ssl
import websockets

async def echo(websocket):
    try:
        while True:
            message = await asyncio.wait_for(websocket.recv(), timeout=30)
            print(f"✅ Received: {message}")
            await websocket.send("PONG from WSS server")
    except asyncio.TimeoutError:
        print("⚠️ No message received in 30 seconds. Closing connection.")
        await websocket.close()
    except websockets.exceptions.ConnectionClosed:
        print("❌ Client disconnected.")
    except Exception as e:
        print(f"❌ Server error: {e}")

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    async with websockets.serve(
        echo,
        "localhost",
        8002,
        ssl=ssl_context,
        ping_interval=10,     # kirim ping setiap 10 detik
        ping_timeout=5        # jika tidak ada pong dalam 5 detik, koneksi ditutup
    ):
        print("✅ WSS server running on wss://localhost:8002")
        await asyncio.Future()  # Run forever

asyncio.run(main())
