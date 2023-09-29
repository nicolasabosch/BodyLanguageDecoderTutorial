#!/usr/bin/env python
# -*- coding: utf-8 -*-
import websockets
import asyncio
import mediapipe as mp # Import mediapipe
import time
import cv2 # Import opencv
import json
import time

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
print("1")
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
    local="local"
    visitante="visitante"
    startTime = time.time()
    jugadosTotal=0
    jugadoAhora=0
    msgReceived = False
    async with websockets.connect('ws://localhost:8000') as websocket:
        print("2")
        while msgReceived ==False:
            
            response = await websocket.recv()
            #global local
            #global visitante
            json_obj = json.loads(response)
            local= json_obj["local"]
            visitante= json_obj["visitante"]
            print(f"Received message: {response}")
            msgReceived =True
            text = f"bienvenido a foul, la aplicacion encargada de revolucionar la industria del basket {local} y {visitante}  "
            #engine.say(text)
            #engine.runAndWait()
            sendMessage(text,websocket)
            #await websocket.send(text)
            
            #response = await websocket.recv()

            with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    #print(results.right_hand_landmarks)
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # Recolor Feed
                    image.flags.writeable = False        
                    
                    # Make Detections
                    results = holistic.process(image)
                    #print(results.face_landmarks)
                    
                    # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
                    
                    # Recolor image back to BGR for rendering
                    image.flags.writeable = True   
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    
                    # 1. Draw face landmarks
                    #mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
                                            #mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                            #mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                            #)
                    
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
                                    
                    # Display Class
                # cv2.putText(image, 'CLASS', (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

                    
                    
                    currentTime = int(time.time()*1000.0)
                    currentGesture = getCurrentGesture(results)
                    flippedImage = cv2.flip(image, 1)
                    
                    nowTime = time.time()
                    timeElapsed = nowTime - startTime
                    
                    #jugadosTotal= jugadosTotal+timeElapsed
                    print(jugadoAhora)
                    #print(currentGesture)
                    if lastGesture != currentGesture:
                        lastGesture = currentGesture
                        lastTime = currentTime

                    if currentTime - lastTime > 500 and currentGesture == lastGesture:
                        if currentGesture!=lastPrintedGesture:
                            lastPrintedGesture = currentGesture
                            mensaje="Equipo: "  + str(currentGesture[0]) + " BD: " + str(currentGesture[1])  + " BI: "  + str(currentGesture[2])  + " MD: "  +  str(currentGesture[3]) + " MI: "  +  str(currentGesture[4])
                            print(mensaje)
                            
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

                                    sendMessage(eventName,websocket)                       
                                    #await websocket.send(eventName)
                                    #response = await websocket.recv()
                                case "Tanto":
                                    
                                    if eventName=="Local":    
                                        puntosLocal +=eventValue
                                
                                    else:
                                        puntosVisitante +=eventValue
                                    #engine.say(str(eventValue) + " para el " + eventName)
                                    #await websocket.send(str(eventValue) + " para el " + eventName)
                                    sendMessage(str(eventValue) + " para el " + eventName,websocket)
                                    #response = await websocket.recv()
                                    #messageStatus = currentMatchStatus +  local+ ": " +str(puntosLocal)  + ","+ visitante +": " +str(puntosVisitante)  
                                    #await websocket.send(messageStatus)
                                    #response = await websocket.recv()
                                    #engine.say("Ahora " + messageStatus)
                                    #engine.runAndWait()    
                                case "Amonestado":
                                    
                                    if eventName=="Local":
                                        nombreEquipo=local
                                    else:
                                        nombreEquipo=visitante
                                    
                                    sendMessage("Jugador amonestado del equipo " + nombreEquipo  + ", camiseta Número " + str(eventValue),websocket)
                                    #await websocket.send("Jugador amonestado del equipo " + nombreEquipo  + ", camiseta Número " + str(eventValue))
                                    #response = await websocket.recv()
                                    #engine.say("Jugador amonestado del equipo " + nombreEquipo  + ", camiseta Número " + str(eventValue))
                                    #engine.runAndWait()
                                            
                                
                            #cv2.putText(flippedImage, mensaje , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
                        
                    if currentMatchStatus=="Jugando":
                        jugadoAhora= jugadosTotal+timeElapsed

                    
                    messageStatus = currentMatchStatus + local+ ": "  +str(puntosLocal)  + visitante +": " +str(puntosVisitante) + "tiempo Jugado: " + str(jugadoAhora)  + " - " +str(jugadosTotal)
                    
                    cv2.putText(flippedImage, messageStatus , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

                    cv2.imshow('Raw Webcam Feed',flippedImage )
                    
                    if cv2.waitKey(10) & 0xFF == ord('q'):
                        break

            cap.release()
            cv2.destroyAllWindows()

asyncio.run(chat_receive())