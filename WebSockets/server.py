#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets
from websockets.legacy.client import connect as ws_connect

# create a dictionary to store connected clients
clients = {}

async def handler(websocket, path):
    # add client to dictionary
    clients[websocket] = None

    try:
        while True:
            # receive message from client
            message = await websocket.recv()

            # broadcast message to all clients
            for client in clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosed:
        # remove client from dictionary when connection is closed
        del clients[websocket]

async def start_server():
    async with websockets.serve(handler, "localhost", 8000):
        await asyncio.Future()  # run forever

asyncio.run(start_server())