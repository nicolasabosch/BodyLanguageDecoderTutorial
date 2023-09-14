#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mediapipe as mp # Import mediapipe
import time
import cv2 # Import opencv
mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions

import pyttsx3
engine = pyttsx3.init()
voices =engine.getProperty('voices')
    
# Control the rate. Higher rate = more speed
engine.setProperty("rate", 180)
engine.setProperty('voice', voices[3].id)

text = "bienvenido a foul, la aplicacion encargada de revolucionar la industria del basket"
engine.say(text)
engine.runAndWait()

from funciones import *
currentGesture =["","","",0,0]          
lastGesture =["","","",0,0]
lastTime = int(time.time()*1000.0)
lastPrintedGesture= ["","","",0,0]
puntosLocal= 0 
puntosVisitante=0
messageStatus=""
currentMatchStatus="No Comenzado"
cap = cv2.VideoCapture(0)
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.8, min_tracking_confidence=0.8) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        #print(results.right_hand_landmarks)
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
                        engine.say(eventName)
                        engine.runAndWait()

                    case "Tanto":
                        if eventName=="Local":    
                            puntosLocal +=eventValue
                    
                        else:
                            puntosVisitante +=eventValue
                        engine.say(str(eventValue) + " para el " + eventName)
                        #engine.runAndWait()
                        
                if eventType !="":
                    messageStatus = currentMatchStatus + " Local: "  +str(puntosLocal)  + ", Visitante: " +str(puntosVisitante)  
                    engine.say("Ahora " + messageStatus)
                    engine.runAndWait()
                #cv2.putText(flippedImage, mensaje , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        

        else:
            messageStatus = currentMatchStatus + " Local: "  +str(puntosLocal)  + " Visitante: " +str(puntosVisitante)  
            v =1
            #cv2.putText(flippedImage, " - " , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            # Display Probability
        

        cv2.putText(flippedImage, messageStatus , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Raw Webcam Feed',flippedImage )
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

