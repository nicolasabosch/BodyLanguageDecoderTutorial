#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import websockets
import json



local="xxlocal"
visitante="xxvisitante"




async def chat_receive():
    msgReceived = False
    async with websockets.connect('ws://localhost:8000') as websocket:
        while msgReceived ==False:
            #message = input("Enter message: ")
            #await websocket.send(message)
            response = await websocket.recv()
            global local
            global visitante
            json_obj = json.loads(response)
            local= json_obj["local"]
            visitante= json_obj["visitante"]
            
            print(f"Received message: {response}")

        

            msgReceived =True



asyncio.run(chat_receive())

text = f"bienvenido a foul, la aplicacion encargada de revolucionar la industria del basket {local} y {visitante}  "
print (text)

        

