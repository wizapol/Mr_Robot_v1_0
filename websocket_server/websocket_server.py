# websocket_server.py
import asyncio
import websockets
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('websocket_server')

connected_clients = set()

async def echo(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            logger.info(f"Received message: {message}")
            await asyncio.gather(*(client.send(message) for client in connected_clients))
    except websockets.ConnectionClosedError as e:
        logger.error(f"WebSocket connection closed with code {e.code} and reason '{e.reason}'")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        connected_clients.remove(websocket)

async def shutdown():
    tasks = []
    for client in connected_clients:
        tasks.append(client.close())
    await asyncio.gather(*tasks)

def signal_handler(sig, frame):
    logger.info("Shutting down server...")
    asyncio.ensure_future(shutdown())
    asyncio.get_event_loop().stop()

start_server = websockets.serve(echo, "localhost", 8765)

signal.signal(signal.SIGINT, signal_handler)

try:
    logger.info("Starting WebSocket server...")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    asyncio.get_event_loop().close()
    logger.info("WebSocket server stopped.")
