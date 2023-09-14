

def rightHand (results):
     if results.right_hand_landmarks is None:
          return 0
      
     suma = 0
     if results.right_hand_landmarks.landmark[19].y > results.right_hand_landmarks.landmark[20].y: 
        suma +=1 
     if results.right_hand_landmarks.landmark[15].y > results.right_hand_landmarks.landmark[16].y: 
        suma +=1    

     if results.right_hand_landmarks.landmark[11].y > results.right_hand_landmarks.landmark[12].y: 
        suma +=1        
     if results.right_hand_landmarks.landmark[7].y > results.right_hand_landmarks.landmark[8].y: 
        suma +=1           
     if results.right_hand_landmarks.landmark[4].x > results.right_hand_landmarks.landmark[5].x: 
        suma +=1               
 
     return suma       

def leftHand (results):
     if results.left_hand_landmarks is None:
          return 0
      
     suma = 0
     if results.left_hand_landmarks.landmark[19].y > results.left_hand_landmarks.landmark[20].y: 
        suma +=1 
     if results.left_hand_landmarks.landmark[15].y > results.left_hand_landmarks.landmark[16].y: 
        suma +=1    

     if results.left_hand_landmarks.landmark[11].y > results.left_hand_landmarks.landmark[12].y: 
        suma +=1        
     if results.left_hand_landmarks.landmark[7].y > results.left_hand_landmarks.landmark[8].y: 
        suma +=1           
     if results.left_hand_landmarks.landmark[4].x > results.left_hand_landmarks.landmark[5].x: 
        suma +=1               

     return suma
def leftArm(results):
    if results.pose_landmarks is None:
          return 'U'
    
    if results.pose_landmarks.landmark[15].y > results.pose_landmarks.landmark[23].y:
        return 'L'
    if results.pose_landmarks.landmark[15].y > results.pose_landmarks.landmark[11].y:
        
        return 'M'
    else:
         return 'H'
    
def rightArm(results):
    if results.pose_landmarks is None:
          return 'U'
    
    if results.pose_landmarks.landmark[16].y > results.pose_landmarks.landmark[24].y:
        return 'L'
    if results.pose_landmarks.landmark[16].y > results.pose_landmarks.landmark[12].y:
        
        return 'M'
    else:
         return 'H'
    
def Side(results):
            if results.pose_landmarks is None:
                return "Undefined"

            orejaDerecha= results.pose_landmarks.landmark[8].z
            orejaIzquierda= results.pose_landmarks.landmark[7].z
            
            #print(orejaDerecha)
            
            if orejaDerecha > orejaIzquierda:
                return "Local"
            else:
               return 'Visitante'
                
def getCurrentGesture(results):
    if results is None:
         return "Undefined"
    else:
         #"Equipo: "  + Side(results) + " BD: " + rightArm(results)  + " BI: "  + leftArm(results)  + " MD: "  +  str(rightHand(results)) + " MI: "  +  str(leftHand(results))
         #decision=[Side(results),rightArm(results),leftArm(results),rightHand(results),leftHand(results)]
         return [Side(results),rightArm(results),leftArm(results),rightHand(results),leftHand(results)]
    
def getGestureValue(CurrentGesture,matchStatus):
    rightArm=CurrentGesture[1]
    team =CurrentGesture[0]
    
    if rightArm=="L":
        return ["","",0]
    if rightArm=="H":
        rightHand=CurrentGesture[3]
        if  rightHand == 0:
            return ["MatchStatus","Falta",0]
        
        if  (matchStatus=="Falta") and rightHand >= 1 and rightHand <=2:
            return ['Tanto',team,rightHand]

        if  (matchStatus=="Jugando") and rightHand >= 2 and rightHand <=3:
            return ['Tanto',team,rightHand]

        if  rightHand == 5:
            match matchStatus:
               case "Falta":
                  return ['MatchStatus',"Jugando",0]
               case "No Comenzado":
                  return ['MatchStatus',"Jugando",0]
               case "Playing":
                  return ['MatchStatus',"Pausado",0]
               case "Pausado":
                  return ['MatchStatus',"Jugando",0]
               case _:
                  return ["","",0]
       
    
    return ["","",0]