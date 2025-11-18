# multi_ws_server.py
import asyncio
import json
import uuid
import websockets



# Keep track of connected clients
connected_clients = set()

async def handle_client(websocket, path):
    # Register client
    client_id = str(uuid.uuid4())
    connected_clients.add(websocket)
    print(f"[+] Client connected: {client_id} | Total: {len(connected_clients)}")
    
    try:
        async for message in websocket:
            # If you are sending JSON metadata + binary, handle accordingly
            # Here we just echo back JSON text messages
            try:
                data = json.loads(message)
                print(f"Received from {client_id}: {data}")
                response = {"status": "ok", "client_id": client_id}
                await websocket.send(json.dumps(response))
            except json.JSONDecodeError:
                print(f"Received raw message from {client_id}: {message}")
                await websocket.send(f"ACK: {message}")

    except websockets.exceptions.ConnectionClosedOK:
        print(f"[-] Client disconnected: {client_id}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client removed. Total: {len(connected_clients)}")

async def main():
    async with websockets.serve(handle_client, "0.0.0.0", 8765, max_size=2*1024*1024):
        print("WebSocket server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
