#!/usr/bin/env python
# -*- coding: utf-8 -*-
import websockets
import asyncio
import mediapipe as mp # Import mediapipe
import time
import cv2 # Import opencv
import json



mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions

import pyttsx3
engine = pyttsx3.init()
voices =engine.getProperty('voices')
    
# Control the rate. Higher rate = more speed
engine.setProperty("rate", 180)
engine.setProperty('voice', voices[3].id)



#text = "bienvenido a foul, la aplicacion encargada de revolucionar la industria del basket"

from funciones import *
# Initiate holistic model
local="local"
visitante="visitante"

async def chat_receive():
    currentGesture =["","","",0,0]          
    lastGesture =["","","",0,0]
    lastTime = int(time.time()*1000.0)
    lastPrintedGesture= ["","","",0,0]
    puntosLocal= 0 
    puntosVisitante=0
    messageStatus=""
    currentMatchStatus="No Comenzado"
    cap = cv2.VideoCapture(0)
    startTime = time.time()
    jugadosTotal=0
    jugadoAhora=0
    msgReceived = False
    async with websockets.connect("ws://localhost:8000") as websocket:
    #async with websockets.connect("ws://172.174.204.46:8000") as websocket:
        print("Esperando configuración del partido")
        while msgReceived ==False:
            
            response = await websocket.recv()
            #global local
            #global visitante
            json_obj = json.loads(response)
            local= json_obj["local"]
            visitante= json_obj["visitante"]
            print(visitante)
            msgReceived =True
            
            json_obj["puntosLocal"]=puntosLocal
            json_obj["puntosVisitante"]=puntosVisitante

            json_obj["tiempoRestante"] ="10:00"
            json_obj["text"] = f"bienvenido a foul, la aplicacion revolucionaria del basket. Hoy jugarán: {local} y {visitante}  "
            await sendMessage(json_obj,websocket)
            json_obj["text"] =""
           
            with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False        
                    results = holistic.process(image)
                    image.flags.writeable = True   
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                  
                    # 2. Right hand
                    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                            )

                    # 3. Left Hand
                    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                            )

                    # 4. Pose Detections
                    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                            )
                    
                    currentTime = int(time.time()*1000.0)
                    currentGesture = getCurrentGesture(results)
                    flippedImage = cv2.flip(image, 1)
                    
                    nowTime = time.time()
                    timeElapsed = nowTime - startTime
                    m, s = divmod(int(600-jugadoAhora), 60)
                    h, m = divmod(m, 60)
                    
                    json_obj["tiempoRestante"] =f'{m:02d}:{s:02d}'
                    await sendMessage(json_obj,websocket)

                    if lastGesture != currentGesture:
                        lastGesture = currentGesture
                        lastTime = currentTime

                    if currentTime - lastTime > 500 and currentGesture == lastGesture:
                        if currentGesture!=lastPrintedGesture:
                            lastPrintedGesture = currentGesture
                            mensaje="Equipo: "  + str(currentGesture[0]) + " BD: " + str(currentGesture[1])  + " BI: "  + str(currentGesture[2])  + " MD: "  +  str(currentGesture[3]) + " MI: "  +  str(currentGesture[4])
                           
                            gestureValue = getGestureValue(currentGesture,currentMatchStatus)
                            eventType = gestureValue[0] 
                            eventName = gestureValue[1]
                            eventValue = gestureValue[2]
                            
                            match eventType:
                                
                                case "MatchStatus":    
                                    currentMatchStatus = eventName
                                    if currentMatchStatus=="Jugando":
                                        startTime = time.time()
                                    else:
                                        jugadosTotal= jugadosTotal+timeElapsed

                                    json_obj["text"] =eventName
                                    await sendMessage(json_obj,websocket)                       
                                    json_obj["text"] =""

                                case "Tanto":
                                    
                                    if eventName=="local":    
                                        puntosLocal +=eventValue
                                        nombreEquipo=local
                                    else:
                                        puntosVisitante +=eventValue
                                        nombreEquipo=visitante
                                    
                                    json_obj["puntosLocal"]=puntosLocal
                                    json_obj["puntosVisitante"]=puntosVisitante
                                    json_obj["text"] =str(eventValue) + " para " +  nombreEquipo
                                    await sendMessage(json_obj,websocket)                       
                                    json_obj["text"] =""
                                   
                                case "Amonestado":
                                    currentMatchStatus="Esperando"
                                    if eventName=="local":
                                        nombreEquipo=local
                                        
                                        for item in json_obj["localJugadores"]:
                                            if item["Camiseta"] == eventValue:
                                                item["Faltas"]=item["Faltas"]+1
                                    else:
                                        nombreEquipo=visitante
                                        for item in json_obj["visitanteJugadores"]:
                                            if item["Camiseta"] == eventValue:
                                                item["Faltas"]=item["Faltas"]+1
                                               
                                    json_obj["text"] ="Jugador amonestado del equipo " + nombreEquipo  + ", camiseta Número " + str(eventValue)                                                         
                                    await sendMessage( json_obj,websocket)
                                    json_obj["text"] =""
                                    
                    if currentMatchStatus=="Jugando":
                        jugadoAhora= jugadosTotal+timeElapsed
                    json_obj["currentMatchStatus"] = currentMatchStatus

                    messageStatus = currentMatchStatus + local + ": "  +str(puntosLocal)  + visitante +": " +str(puntosVisitante) + "tiempo Jugado: " + str(jugadoAhora)  + " - " +str(jugadosTotal)
                    cv2.putText(flippedImage, messageStatus , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                    cv2.imshow('Raw Webcam Feed',flippedImage )
                    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

asyncio.run(chat_receive())