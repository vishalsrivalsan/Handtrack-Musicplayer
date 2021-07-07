import cv2
import numpy
import math
import time
import pyautogui
import handTracking as ht

detector = ht.handTrack(detectConf=0.85,trackConf=0.65)
cam = cv2.VideoCapture(0)

prevSlidePoint=0
prevPoint=0
openFist=False
closedFist=False
while True:
    success, frame = cam.read()
    if success:
        frame = detector.findHands(frame,draw=True)
        pointsList=detector.findPosition(frame,draw=False)
        #print(pointsList)
        tipPoints = [4,8,12,16,20]
        fingers=[]
        str=""
        thumb=index=middle=ring=pinky=False
        currSlidePoint=0
        currPoint=0
        if len(pointsList)!=0:
            for num in tipPoints:
                if num==4: #For thumb check x-axis
                    if pointsList[num][1]>pointsList[num-1][1]:
                        fingers.append(1)
                        thumb=True
                        continue
                    else:
                        fingers.append(0)
                        continue
                        
                if pointsList[num][2]<pointsList[num-1][2]:
                    if num==8:
                        index=True
                    elif num==12:
                        middle=True
                    elif num==16:
                        ring=True
                    elif num==20:
                        pinky=True
                    fingers.append(1)
                else:
                    fingers.append(0)
            count=fingers.count(1)
            
            if index and not (middle or ring or pinky or thumb):
                str="one"
            if middle and not (index or ring or pinky or thumb):
                str="ahem"
            if (index and pinky) and not (middle or index or thumb):
                str="Rock"
            if (index and pinky and thumb) and not (middle or ring):
                str="Spiderman"
            if pinky and not (middle or ring or index or thumb):
                str="Pink"
            if (thumb and pinky) and not (ring or middle or index ):
                str="Let's Go"
            if thumb and not (middle or ring or pinky or index):
                str="Thumbs Up"
            

            if count==0:                #Closed to Open
                closedFist=True
##                if prevPoint==0:
##                    prevPoint = int(pointsList[0][1])

                
            elif count==5 and closedFist:
                prevPoint=0
                currPoint=0
                openFist=False
                closedFist=False
                print("Open Motion")
                pyautogui.hotkey('ctrl','p')
                #time.sleep(2)
                continue
                
            if count==5:                #Slide
                if prevSlidePoint==0:
                    prevSlidePoint = pointsList[0][1]
                currSlidePoint=pointsList[0][1]
                #print('prevSlidePoint:',prevSlidePoint,' currSlidePoint: ',currSlidePoint)
            else:
                currSlidePoint=0
                prevSlidePoint=0

            
            if currSlidePoint-prevSlidePoint > 300:         #Slide Left
                    prevSlidePoint=0
                    currSlidePoint=0
                    print('Slide Left')
                    pyautogui.hotkey('ctrl','8')
                    #cv2.putText(frame, "Slide Left", (45,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 2)
#                   time.sleep(2)
                    continue
            elif prevSlidePoint-currSlidePoint > 300:       #Slide Right 
                    prevSlidePoint=0
                    currSlidePoint=0
                    #cv2.putText(frame, "Slide Right", (45,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 2)
                    print('Slide Right')
                    pyautogui.hotkey('ctrl','9')
#                    time.sleep(2)
                    continue
        else:
             closedFist=False
             openFist=False
             currSlidePoint=0
             prevSlidePoint=0
        '''if len(str)!=0:
            cv2.putText(frame, str, (45,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 2)'''
        
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break;
        
