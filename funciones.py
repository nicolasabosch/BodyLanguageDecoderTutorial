

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
     if results.right_hand_landmarks.landmark[5].y > results.right_hand_landmarks.landmark[4].y: 
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
     if results.left_hand_landmarks.landmark[5].y > results.left_hand_landmarks.landmark[4].y: 
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
            if results.pose_landmarks.landmark is None:
                return "Undefined"

            orejaDerecha= results.pose_landmarks.landmark[8].z
            orejaIzquierda= results.pose_landmarks.landmark[7].z
            
            #print(orejaDerecha)
            
            if orejaDerecha > orejaIzquierda:
                return "Derecha"
            else:
                if orejaDerecha < orejaIzquierda:
                    return 'Izquierda'
                else:
                      return 'Medio'

def getCurrentGesture(results):
    if results is None:
         return "Undefined"
    else:
         return "Equipo: "  + Side(results) + " BD: " + rightArm(results)  + " BI: "  + leftArm(results)  + " MD: "  +  str(rightHand(results)) + " MI: "  +  str(leftHand(results))