#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets

async def echo(websocket, path):
    async for message in websocket:
        message = "Responding from the CodeTryout server.py: ", message
        await websocket.send(message)

start_server = websockets.serve(echo, "172.174.204.46", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()