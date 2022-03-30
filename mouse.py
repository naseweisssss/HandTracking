import cv2.cv2 as cv2
import numpy as np
import HandModule as htm
import time
import pyautogui

#######################
wCam, hCam = 640, 480
wScr, hScr = pyautogui.size()
frameReduction = 100
smoothen = 4
#######################

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)

pTime = 0
coolingTime = 0

px,py = pyautogui.position()
cx,cy = pyautogui.position()

detector = htm.handDetector(maxHands=1)

while True:
    # find landmark
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # tip of index and middle finger
        x1, y1 = lmList[8][1:]
        print(x1,y1)
        x2, y2 = lmList[12][1:]

        # check finger
        fingers = detector.fingersUp()

        # moving mode
        if fingers[1]==1 and fingers[2]==0 and fingers[3]==0:
            # convert coordinate
            x3 = np.interp(x1,(frameReduction,wCam-frameReduction),(0,wScr-1))
            y3 = np.interp(y1,(frameReduction,hCam-frameReduction),(0,hScr-1))
            # smoothen values
            cx = px + (x3-px)/smoothen
            cy = py + (y3-py)/smoothen
            # move mouse
            if pyautogui.onScreen(cx,cy):
                pyautogui.moveTo(cx, cy)
            px,py = cx,cy
        
        # Left click
        if fingers[0]==0 and fingers[1]==1 and fingers[2]==0 and fingers[3]==0:
            length, unused = detector.findDistance(4,8,img)
            if (length<20):
                cv2.circle(img, (x1,y1), 15, (0,255,0), cv2.FILLED)
                if (cTime>coolingTime):
                    # print("Left click")
                    pyautogui.click()
                    coolingTime=cTime+0.5

        # Right click
        elif fingers[0]==0 and fingers[1]==1 and fingers[2]==1 and fingers[3]==0:
            length, unused = detector.findDistance(8,12,img)
            if (length<40):
                cv2.circle(img, (x1,y1), 15, (0,255,0), cv2.FILLED)
                if (cTime>coolingTime):
                    # print("Right click")
                    pyautogui.click(button='right')
                    coolingTime=cTime+1


    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}", (20,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    # display
    cv2.imshow("Display", img)
    if cv2.waitKey(1)&0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
