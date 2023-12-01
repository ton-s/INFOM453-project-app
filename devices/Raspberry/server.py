#!/usr/bin/env python

import asyncio
from websockets.server import serve

async def handle_message(message, websocket):
    print(f"Received message from client: {message}")
    response = f"Server received: {message}"
    response = "Message from the server"
    await websocket.send(response)

async def echo(websocket, path):
    async for message in websocket:
        await handle_message(message, websocket)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
