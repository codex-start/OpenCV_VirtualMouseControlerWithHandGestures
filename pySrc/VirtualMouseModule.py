import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

##############################
wCam , hCam = 640 , 400
frameR=100
smoothening = 7
##############################
plocX , plocY = 0 , 0
clocX , clocY = 0 , 0



cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)
cTime=0
pTime=0
detector = htm.handDetector(maxHands=1)
wScr , hScr = autopy.screen.size()
#print(wScr,hScr)

while True:
         #1. Find Hand Landmarks
         success , img = cap.read()
         img = detector.findHands(img)
         lmList , bbox = detector.findPosition(img)





         #2. Get the tip
         if len(lmList) != 0:
             x1, y1 = lmList[8][1:]
             x2, y2 = lmList[12][1:]
             #print(x1,y1,x2,y2)




            #3. which finger is up
             fingers = detector.fingersUp()
              #print(fingers)
             cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)



             #4. Only the index finger: Moving mode
             if fingers[1]==1 and fingers[2] == 0:
                     #5. Convert Coordinates

                     x3 = np.interp(x1,(frameR , wCam-frameR) , (0,wScr))
                     y3 = np.interp(y1,(frameR,  hCam-frameR), (0, hScr))



                     #6. Smoothen Values
                     clocX = plocX +(x3-plocX) / smoothening
                     clocY = plocY + (x3 - plocY) / smoothening



                     #7. Move Mouse
                     autopy.mouse.move(wScr-clocX,clocY)
                     cv2.circle(img, (x1, y1), 7, (255, 0, 255), cv2.FILLED)
                     plocX,plocY = clocX , clocY

             #8.Both index and middle finger is up clicking mode
             if fingers[1] == 1 and fingers[2] == 1:







                 # 9.Find didtance between fingers
                 length,img,lineInfo=detector.findDistance(8,12,img)
                 print(length)








                 # 10.click mouse if distance is short
                 if length<35:
                     cv2.circle(img, (lineInfo[4], lineInfo[5]), 7, (0, 255, 0), cv2.FILLED)
                     autopy.mouse.click()















         #11.Frame rate
         cTime=time.time()
         fps = 1/(cTime-pTime)
         pTime=cTime
         cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_SIMPLEX,2,(255,0,0),3)













         #12.display
         cv2.imshow("Capture",img)
         cv2.waitKey(1)