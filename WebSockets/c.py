#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets

async def hello():
    async with websockets.connect("ws://172.174.204.46:8000") as websocket:
        await websocket.send("Hello, CodeTryout!")
        response = await websocket.recv()
        print(response)

asyncio.get_event_loop().run_until_complete(hello())